import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.github_verifier.github_checks import PRVerifier, GitHubChecker


def test_check_deadline_no_deadline():
    verifier = PRVerifier(GitHubChecker(token=""))
    result = verifier._check_deadline({})
    assert result["passed"] is True


def test_check_deadline_past():
    verifier = PRVerifier(GitHubChecker(token=""))
    manifest = {"deadline": "2020-01-01T00:00:00"}
    result = verifier._check_deadline(manifest)
    assert result["passed"] is False


def test_check_deadline_future():
    verifier = PRVerifier(GitHubChecker(token=""))
    manifest = {"deadline": "2099-12-31T23:59:59"}
    result = verifier._check_deadline(manifest)
    assert result["passed"] is True


def test_check_files_no_requirements():
    verifier = PRVerifier(GitHubChecker(token=""))
    result = verifier._check_files([], {})
    assert result["passed"] is True


def test_check_files_all_present():
    verifier = PRVerifier(GitHubChecker(token=""))
    files = [{"filename": "src/SwapForm.tsx"}, {"filename": "src/slippage.ts"}]
    manifest = {"required_files": ["SwapForm.tsx", "slippage"]}
    result = verifier._check_files(files, manifest)
    assert result["passed"] is True


def test_check_files_missing():
    verifier = PRVerifier(GitHubChecker(token=""))
    files = [{"filename": "src/other.ts"}]
    manifest = {"required_files": ["SwapForm.tsx"]}
    result = verifier._check_files(files, manifest)
    assert result["passed"] is False


def test_check_ci_no_runs():
    verifier = PRVerifier(GitHubChecker(token=""))
    result = verifier._check_ci_status({"total_count": 0, "check_runs": []})
    assert result["passed"] is False


def test_check_ci_all_passing():
    verifier = PRVerifier(GitHubChecker(token=""))
    ci = {"total_count": 2, "check_runs": [{"conclusion": "success"}, {"conclusion": "success"}]}
    result = verifier._check_ci_status(ci)
    assert result["passed"] is True


def test_check_ci_one_failing():
    verifier = PRVerifier(GitHubChecker(token=""))
    ci = {"total_count": 2, "check_runs": [{"conclusion": "success"}, {"conclusion": "failure"}]}
    result = verifier._check_ci_status(ci)
    assert result["passed"] is False
