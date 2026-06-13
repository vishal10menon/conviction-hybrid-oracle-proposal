import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.verifier_agent.agent import VerifierAgent


def get_agent():
    return VerifierAgent(domain="defi-frontend", contract_path="examples/sample_manifest.json")


def test_all_checks_run():
    agent = get_agent()
    submission = {"id": "sub-1", "files": [], "outputs": []}
    report = agent.verify(submission)
    assert len(report["checks"]) == 3


def test_file_exists_passes():
    agent = get_agent()
    submission = {"id": "sub-2", "files": ["SwapForm.tsx"], "outputs": []}
    report = agent.verify(submission)
    file_check = [c for c in report["checks"] if c["type"] == "file_exists"][0]
    assert file_check["passed"] is True


def test_file_exists_fails():
    agent = get_agent()
    submission = {"id": "sub-3", "files": [], "outputs": []}
    report = agent.verify(submission)
    file_check = [c for c in report["checks"] if c["type"] == "file_exists"][0]
    assert file_check["passed"] is False


def test_manual_always_fails():
    agent = get_agent()
    submission = {"id": "sub-4", "files": ["SwapForm.tsx"], "outputs": ["0 failures"]}
    report = agent.verify(submission)
    manual_check = [c for c in report["checks"] if c["type"] == "manual"][0]
    assert manual_check["passed"] is False


def test_all_passed_false_when_manual_fails():
    agent = get_agent()
    submission = {"id": "sub-5", "files": ["SwapForm.tsx"], "outputs": ["0 failures"]}
    report = agent.verify(submission)
    assert report["all_passed"] is False


def test_por_generated_only_when_all_pass():
    agent = get_agent()
    submission = {"id": "sub-6", "files": [], "outputs": []}
    report = agent.verify(submission)
    assert report["proof_of_resolution"] is None
