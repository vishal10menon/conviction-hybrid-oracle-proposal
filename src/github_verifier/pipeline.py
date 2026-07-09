"""
End-to-End Pipeline: Connects GitHub PR checks to the verifier agent
and challenge window. One command runs the full verification flow.
"""

import json
from src.github_verifier.github_checks import GitHubChecker, PRVerifier
from src.verifier_agent.agent import VerifierAgent
from src.challenge_game.window import ChallengeWindow
from src.reputation.weighting import ReputationLedger


class VerificationPipeline:
    """
    Runs the full HAOO verification flow on a GitHub PR:
    1. GitHub checks (CI, files, deadline, merge status)
    2. Verifier agent (semantic criteria via manifest)
    3. Challenge window (open if all checks pass)
    4. Post result as GitHub comment
    """

    def __init__(self, github_token: str = None):
        self.github = GitHubChecker(token=github_token)
        self.pr_verifier = PRVerifier(self.github)
        self.ledger = ReputationLedger()

    def run(self, owner: str, repo: str, pr_number: int, manifest_path: str) -> dict:
        """Execute the full pipeline and return a combined report."""
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        # Step 1: GitHub-level checks
        pr_report = self.pr_verifier.verify_pr(owner, repo, pr_number, manifest)

        # Step 2: Semantic verification via agent
        pr_data = self.github.get_pr(owner, repo, pr_number)
        files = self.github.get_pr_files(owner, repo, pr_number)

        submission = {
            "id": f"pr-{pr_number}",
            "files": [f["filename"] for f in files],
            "outputs": self._extract_ci_outputs(owner, repo, pr_data["head"]["sha"]),
            "pr_url": pr_data.get("html_url", ""),
            "author": pr_data.get("user", {}).get("login", "unknown"),
        }

        agent = VerifierAgent(
            domain=manifest.get("domain", "general"),
            contract_path=manifest_path,
            use_llm=False,
        )
        agent_report = agent.verify(submission)

        # Step 3: Combine results
        all_passed = pr_report["all_passed"] and agent_report["all_passed"]

        combined = {
            "pr_number": pr_number,
            "repo": f"{owner}/{repo}",
            "all_passed": all_passed,
            "github_checks": pr_report["checks"],
            "agent_checks": agent_report["checks"],
            "challenge_window": None,
        }

        # Step 4: Open challenge window if verified
        if all_passed:
            window = ChallengeWindow(
                verification_report=combined,
                reputation_ledger=self.ledger,
            )
            combined["challenge_window"] = {
                "status": window.status.value,
                "closes_at": window.closes_at.isoformat(),
                "window_hours": window.window_hours,
            }

        # Step 5: Post comment
        comment = self._format_comment(combined, manifest)
        self.github.post_comment(owner, repo, pr_number, comment)

        return combined

    def _extract_ci_outputs(self, owner, repo, sha):
        """Extract CI check results as output strings."""
        try:
            ci = self.github.get_check_runs(owner, repo, sha)
            outputs = []
            for run in ci.get("check_runs", []):
                status = run.get("conclusion", "pending")
                name = run.get("name", "unknown")
                outputs.append(f"{name}: {status}")
            return outputs if outputs else ["No CI checks found"]
        except Exception:
            return ["CI check failed"]

    def _format_comment(self, report, manifest):
        """Format a GitHub comment with the verification result."""
        title = manifest.get("title", "Untitled Bounty")

        if report["all_passed"]:
            status_line = "**Verification PASSED** - Challenge window is open."
        else:
            status_line = "**Verification FAILED** - See checks below."

        comment = f"""## HAOO Verification Result

**Bounty:** {title}
**PR:** #{report['pr_number']}
**Status:** {status_line}

### GitHub Checks
"""
        for check in report["github_checks"]:
            icon = "PASS" if check["passed"] else "FAIL"
            comment += f"- {icon} **{check['type']}**: {check['details']}\n"

        comment += "\n### Semantic Agent Checks\n"
        for check in report["agent_checks"]:
            icon = "PASS" if check["passed"] else "FAIL"
            details = check.get("details", check.get("reasoning", "no details"))
            comment += f"- {icon} **{check.get('type', 'unknown')}**: {details}\n"

        if report["challenge_window"]:
            comment += f"\n### Challenge Window\n"
            comment += f"- Status: {report['challenge_window']['status']}\n"
            comment += f"- Closes at: {report['challenge_window']['closes_at']}\n"
            comment += f"- Anyone may challenge within the window by commenting with a reason and bond.\n"

        comment += "\n---\n*Verified by HAOO - Hybrid Agentic-Optimistic Oracle*"
        return comment
