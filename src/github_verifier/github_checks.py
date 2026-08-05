import json
import os
import requests
from datetime import datetime


class GitHubChecker:
    GITHUB_API = "https://api.github.com"

    def __init__(self, token=None):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_pr(self, owner, repo, pr_number):
        url = f"{self.GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"
        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_pr_files(self, owner, repo, pr_number):
        url = (
            f"{self.GITHUB_API}/repos/{owner}/"
            f"{repo}/pulls/{pr_number}/files"
        )
        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_ci_status(self, owner, repo, sha):
        url = (
            f"{self.GITHUB_API}/repos/{owner}/"
            f"{repo}/commits/{sha}/status"
        )
        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_check_runs(self, owner, repo, sha):
        url = (
            f"{self.GITHUB_API}/repos/{owner}/"
            f"{repo}/commits/{sha}/check-runs"
        )
        response = requests.get(
            url,
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def post_comment(self, owner, repo, pr_number, body):
        url = (
            f"{self.GITHUB_API}/repos/{owner}/"
            f"{repo}/issues/{pr_number}/comments"
        )
        response = requests.post(
            url,
            headers=self.headers,
            json={"body": body},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


class PRVerifier:
    def __init__(self, github):
        self.github = github

    def verify_pr(self, owner, repo, pr_number, manifest):
        checks = []

        pr = self.github.get_pr(
            owner,
            repo,
            pr_number,
        )

        files = self.github.get_pr_files(
            owner,
            repo,
            pr_number,
        )

        sha = pr["head"]["sha"]

        ci = self.github.get_check_runs(
            owner,
            repo,
            sha,
        )

        checks.append(self._check_merge_status(pr))
        checks.append(self._check_ci_status(ci))
        checks.append(self._check_files(files, manifest))
        checks.append(self._check_deadline(manifest))

        all_passed = all(
            check["passed"]
            for check in checks
        )

        return {
            "pr_number": pr_number,
            "repo": f"{owner}/{repo}",
            "sha": sha,
            "all_passed": all_passed,
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _check_merge_status(self, pr):
        state = pr.get("state", "")
        merged = pr.get("merged", False)

        reviewable = state == "open" and not merged

        return {
            "criterion_id": "pr_reviewable",
            "type": "github_pr",
            "passed": reviewable,
            "details": (
                f"PR state: {state}, "
                f"merged: {merged}, "
                f"reviewable: {reviewable}"
            ),
        }

    def _check_ci_status(self, ci):
        total = ci.get("total_count", 0)

        if total == 0:
            return {
                "criterion_id": "ci_passing",
                "type": "github_ci",
                "passed": False,
                "details": "No check runs found",
            }

        all_passed = all(
            run.get("conclusion") == "success"
            for run in ci.get("check_runs", [])
        )

        return {
            "criterion_id": "ci_passing",
            "type": "github_ci",
            "passed": all_passed,
            "details": (
                f"{total} check run(s), "
                f"all passed: {all_passed}"
            ),
        }

    def _check_files(self, files, manifest):
        required_files = manifest.get(
            "required_files",
            [],
        )

        if not required_files:
            return {
                "criterion_id": "files_changed",
                "type": "github_files",
                "passed": True,
                "details": "No required files specified",
            }

        changed_names = [
            file["filename"]
            for file in files
        ]

        missing = [
            required
            for required in required_files
            if not any(
                required in changed
                for changed in changed_names
            )
        ]

        return {
            "criterion_id": "files_changed",
            "type": "github_files",
            "passed": len(missing) == 0,
            "details": (
                f"Missing: {missing}"
                if missing
                else "All required files present"
            ),
        }

    def _check_deadline(self, manifest):
        deadline_str = manifest.get("deadline")

        if not deadline_str:
            return {
                "criterion_id": "deadline",
                "type": "time",
                "passed": True,
                "details": "No deadline specified",
            }

        deadline = datetime.fromisoformat(deadline_str)
        now = datetime.utcnow()

        return {
            "criterion_id": "deadline",
            "type": "time",
            "passed": now <= deadline,
            "details": (
                f"Deadline: {deadline_str}, "
                f"now: {now.isoformat()}"
            ),
        }
