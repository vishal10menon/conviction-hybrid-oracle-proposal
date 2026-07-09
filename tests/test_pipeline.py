import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.github_verifier.pipeline import VerificationPipeline
from src.github_verifier.github_checks import GitHubChecker


def test_format_comment_passed():
    pipeline = VerificationPipeline(github_token="")
    report = {
        "pr_number": 42,
        "repo": "test/repo",
        "all_passed": True,
        "github_checks": [
            {"type": "github_pr", "passed": True, "details": "merged"},
            {"type": "github_ci", "passed": True, "details": "3 checks passed"},
        ],
        "agent_checks": [
            {"type": "file_exists", "passed": True, "details": "file found"},
        ],
        "challenge_window": {"status": "open", "closes_at": "2026-07-10T00:00:00", "window_hours": 24},
    }
    manifest = {"title": "Build swap UI"}
    comment = pipeline._format_comment(report, manifest)
    assert "PASSED" in comment
    assert "Challenge Window" in comment


def test_format_comment_failed():
    pipeline = VerificationPipeline(github_token="")
    report = {
        "pr_number": 43,
        "repo": "test/repo",
        "all_passed": False,
        "github_checks": [
            {"type": "github_ci", "passed": False, "details": "CI failing"},
        ],
        "agent_checks": [],
        "challenge_window": None,
    }
    manifest = {"title": "Build API"}
    comment = pipeline._format_comment(report, manifest)
    assert "FAILED" in comment
