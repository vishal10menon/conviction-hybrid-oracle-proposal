import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.semantic_contract.parser import SemanticContract


def test_valid_contract():
    contract = SemanticContract.from_file("examples/sample_manifest.json")
    errors = contract.validate()
    assert len(errors) == 0


def test_criteria_loaded():
    contract = SemanticContract.from_file("examples/sample_manifest.json")
    assert len(contract.criteria) == 3


def test_manifest_id():
    contract = SemanticContract.from_file("examples/sample_manifest.json")
    assert contract.manifest_id == "manifest-001"


def test_domain():
    contract = SemanticContract.from_file("examples/sample_manifest.json")
    assert contract.domain == "defi-frontend"


def test_missing_required_field():
    contract = SemanticContract({"criteria": [{"id": "x", "type": "manual", "description": "test"}]})
    errors = contract.validate()
    assert any("manifest_id" in e for e in errors)


def test_to_dict():
    contract = SemanticContract.from_file("examples/sample_manifest.json")
    d = contract.to_dict()
    assert "manifest_id" in d
    assert "criteria" in d
