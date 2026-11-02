import json


SYSTEM_ID = "acme-support-agent"
SYSTEM_URL = "https://docs.example.com/acme-support-agent"
DEPLOYMENT_URL = "https://deploy.example.com/acme-support-agent/terms"

PROVIDER = 1
DEPLOYER = 2


def _mock_evidence(vm, payload):
    vm.mock_web(
        r".*docs\.example\.com/acme-support-agent.*",
        {"status": 200, "body": "Official system documentation."},
    )
    vm.mock_web(
        r".*deploy\.example\.com/acme-support-agent/terms.*",
        {"status": 200, "body": "Deployment context and intended purpose."},
    )
    vm.mock_llm(
        r".*AI ACT RISK CLASSIFICATION SCREEN.*",
        json.dumps(payload),
    )


def _evidence(
    tier="minimal",
    prohibited=False,
    annex="none",
    transparency=False,
    consistency="consistent",
    summary="Evidence matches.",
):
    return {
        "risk_tier": tier,
        "prohibited_practice": prohibited,
        "annex_iii_domain": annex,
        "transparency_required": transparency,
        "source_consistency": consistency,
        "summary": summary,
    }


def _register(contract, vm, publisher, role=PROVIDER):
    vm.sender = publisher
    contract.register_system(SYSTEM_ID, SYSTEM_URL, DEPLOYMENT_URL, role)


def test_minimal_risk_is_clear(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(direct_vm, _evidence())

    contract.assess(SYSTEM_ID)

    result = contract.get_assessment(SYSTEM_ID)
    assert result["state"] == 1
    assert result["decision"] == 1
    assert result["decision_name"] == "clear"
    assert result["risk_tier"] == 1
    assert result["risk_tier_name"] == "minimal"
    assert result["round"] == 1
    assert result["obligations"] == []
    assert contract.is_clear(SYSTEM_ID) is True
    assert contract.is_admissible(SYSTEM_ID) is True


def test_limited_risk_requires_disclosure(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(direct_vm, _evidence(tier="limited", transparency=True))

    contract.assess(SYSTEM_ID)

    result = contract.get_assessment(SYSTEM_ID)
    assert result["decision"] == 2
    assert result["risk_tier"] == 2
    assert result["decision_name"] == "disclosure_required"
    assert "ai_interaction_disclosure" in result["obligations"]
    assert contract.is_clear(SYSTEM_ID) is False
    assert contract.is_admissible(SYSTEM_ID) is True


def test_transparency_flag_upgrades_minimal_tier(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        _evidence(tier="minimal", transparency=True),
    )

    contract.assess(SYSTEM_ID)

    assert contract.get_assessment(SYSTEM_ID)["decision"] == 2
    assert contract.is_admissible(SYSTEM_ID) is True


def test_high_risk_provider_is_conditional(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice, role=PROVIDER)
    _mock_evidence(
        direct_vm,
        _evidence(tier="high", annex="employment"),
    )

    contract.assess(SYSTEM_ID)

    result = contract.get_assessment(SYSTEM_ID)
    assert result["decision"] == 3
    assert result["risk_tier"] == 3
    assert result["role_name"] == "provider"
    assert "risk_management_system" in result["obligations"]
    assert "conformity_assessment" in result["obligations"]
    assert "eu_database_registration" in result["obligations"]
    assert contract.is_admissible(SYSTEM_ID) is False


def test_high_risk_deployer_gets_deployer_obligations(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice, role=DEPLOYER)
    _mock_evidence(
        direct_vm,
        _evidence(tier="high", annex="essential_services"),
    )

    contract.assess(SYSTEM_ID)

    result = contract.get_assessment(SYSTEM_ID)
    assert result["role_name"] == "deployer"
    assert "fundamental_rights_impact_assessment" in result["obligations"]
    assert "risk_management_system" not in result["obligations"]


def test_prohibited_tier_is_blocked(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        _evidence(tier="prohibited", prohibited=True),
    )

    contract.assess(SYSTEM_ID)

    result = contract.get_assessment(SYSTEM_ID)
    assert result["decision"] == 4
    assert result["risk_tier"] == 4
    assert result["decision_name"] == "blocked"
    assert result["obligations"] == ["not_permitted"]
    assert contract.is_clear(SYSTEM_ID) is False
    assert contract.is_admissible(SYSTEM_ID) is False


def test_prohibited_flag_overrides_minimal_tier(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        _evidence(tier="minimal", prohibited=True),
    )

    contract.assess(SYSTEM_ID)

    assert contract.get_assessment(SYSTEM_ID)["decision"] == 4


def test_conflicting_sources_require_review(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        _evidence(tier="high", annex="employment", consistency="conflicting"),
    )

    contract.assess(SYSTEM_ID)

    result = contract.get_assessment(SYSTEM_ID)
    assert result["decision"] == 5
    assert result["source_consistency"] == "conflicting"
    assert contract.is_admissible(SYSTEM_ID) is False


def test_unknown_tier_requires_review(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(direct_vm, _evidence(tier="unknown"))

    contract.assess(SYSTEM_ID)

    assert contract.get_assessment(SYSTEM_ID)["decision"] == 5


def test_high_risk_without_annex_domain_requires_review(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        _evidence(tier="high", annex="none"),
    )

    contract.assess(SYSTEM_ID)

    assert contract.get_assessment(SYSTEM_ID)["decision"] == 5


def test_non_high_tier_with_annex_domain_requires_review(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        _evidence(tier="limited", annex="biometrics", transparency=True),
    )

    contract.assess(SYSTEM_ID)

    assert contract.get_assessment(SYSTEM_ID)["decision"] == 5


def test_rejects_duplicate_system_id(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)

    with direct_vm.expect_revert("system_id already registered"):
        contract.register_system(SYSTEM_ID, SYSTEM_URL, DEPLOYMENT_URL, PROVIDER)


def test_rejects_non_https_system_url(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("system_url must be an https URL"):
        contract.register_system(
            SYSTEM_ID,
            "http://docs.example.com/acme-support-agent",
            DEPLOYMENT_URL,
            PROVIDER,
        )


def test_rejects_identical_evidence_urls(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("evidence URLs must differ"):
        contract.register_system(
            SYSTEM_ID,
            SYSTEM_URL,
            SYSTEM_URL,
            PROVIDER,
        )


def test_rejects_invalid_role(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    direct_vm.sender = direct_alice

    with direct_vm.expect_revert("role must be 1 (provider) or 2 (deployer)"):
        contract.register_system(SYSTEM_ID, SYSTEM_URL, DEPLOYMENT_URL, 3)


def test_only_publisher_can_withdraw(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)

    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only the publisher can withdraw"):
        contract.withdraw(SYSTEM_ID)

    direct_vm.sender = direct_alice
    contract.withdraw(SYSTEM_ID)
    assert contract.get_assessment(SYSTEM_ID)["state"] == 2
    assert contract.is_clear(SYSTEM_ID) is False


def test_unknown_system_is_not_admissible(direct_deploy):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")

    assert contract.is_clear("unknown-system") is False
    assert contract.is_admissible("unknown-system") is False
    assert contract.get_assessment("unknown-system") == {}
    assert contract.required_obligations("unknown-system") == []


def test_validator_accepts_matching_evidence(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(
        direct_vm,
        _evidence(tier="high", annex="employment"),
    )

    contract.assess(SYSTEM_ID)

    assert direct_vm.run_validator() is True


def test_validator_rejects_changed_tier(direct_vm, direct_deploy, direct_alice):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(direct_vm, _evidence(tier="minimal"))
    contract.assess(SYSTEM_ID)

    direct_vm.clear_mocks()
    _mock_evidence(direct_vm, _evidence(tier="high", annex="employment"))

    assert direct_vm.run_validator() is False


def test_validator_rejects_changed_prohibited_flag(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(direct_vm, _evidence(tier="minimal", prohibited=True))
    contract.assess(SYSTEM_ID)

    direct_vm.clear_mocks()
    _mock_evidence(direct_vm, _evidence(tier="minimal", prohibited=False))

    assert direct_vm.run_validator() is False


def test_validator_rejects_changed_annex_domain(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(direct_vm, _evidence(tier="high", annex="employment"))
    contract.assess(SYSTEM_ID)

    direct_vm.clear_mocks()
    _mock_evidence(direct_vm, _evidence(tier="high", annex="education"))

    assert direct_vm.run_validator() is False


def test_validator_rejects_changed_transparency_flag(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(direct_vm, _evidence(tier="limited", transparency=True))
    contract.assess(SYSTEM_ID)

    direct_vm.clear_mocks()
    _mock_evidence(direct_vm, _evidence(tier="limited", transparency=False))

    assert direct_vm.run_validator() is False


def test_validator_ignores_summary_wording(
    direct_vm, direct_deploy, direct_alice
):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")
    _register(contract, direct_vm, direct_alice)
    _mock_evidence(direct_vm, _evidence(summary="Leader wording."))
    contract.assess(SYSTEM_ID)

    direct_vm.clear_mocks()
    _mock_evidence(direct_vm, _evidence(summary="Different validator wording."))

    assert direct_vm.run_validator() is True


def test_policy_catalog_exposes_fixed_rubric(direct_deploy):
    contract = direct_deploy("contracts/ai_act_risk_gate.py")

    policy = contract.policy_catalog()
    assert policy["policy_version"] == "eu-ai-act-2024-1689-v1"
    assert policy["clear"] == 1
    assert policy["disclosure_required"] == 2
    assert policy["conditional"] == 3
    assert policy["blocked"] == 4
    assert policy["review_required"] == 5
    assert "employment" in policy["annex_iii_domains"]
    assert "risk_management_system" in policy["provider_high_obligations"]
    assert "fundamental_rights_impact_assessment" in policy["deployer_high_obligations"]
