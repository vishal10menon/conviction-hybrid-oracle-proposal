"""
Verifier Agent: Domain-specific agent that validates builder submissions
against a semantic contract. This is the core of the Agent-in-the-Middle
architecture proposed in HAOO.
"""

import json
from datetime import datetime
from typing import Optional


class VerifierAgent:
    """
    Runs proof-of-resolution checks against a semantic contract.
    Returns a structured verification report.
    """

    def __init__(self, domain: str, contract_path: str):
        self.domain = domain
        self.contract_path = contract_path
        self.contract = self._load_contract(contract_path)

    def _load_contract(self, path: str) -> dict:
        with open(path, "r") as f:
            return json.load(f)

    def verify(self, submission: dict) -> dict:
        """
        Evaluate a builder's submission against the semantic contract.
        Returns a VerificationReport dict.
        """
        checks = []
        all_passed = True

        for criterion in self.contract.get("criteria", []):
            result = self._check_criterion(criterion, submission)
            checks.append(result)
            if not result["passed"]:
                all_passed = False

        report = {
            "agent_id": self.domain,
            "submission_id": submission.get("id", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "all_passed": all_passed,
            "checks": checks,
            "proof_of_resolution": self._generate_por(checks) if all_passed else None,
        }
        return report

    def _check_criterion(self, criterion: dict, submission: dict) -> dict:
        """Check a single criterion against the submission."""
        criterion_id = criterion.get("id", "unknown")
        criterion_type = criterion.get("type", "manual")

        if criterion_type == "file_exists":
            passed = criterion.get("expected_path", "") in str(submission.get("files", []))
        elif criterion_type == "code_output":
            passed = criterion.get("expected_output", "") in str(submission.get("outputs", []))
        elif criterion_type == "manual":
            passed = False  # Requires human attestation
        else:
            passed = False

        return {
            "criterion_id": criterion_id,
            "type": criterion_type,
            "passed": passed,
            "details": criterion.get("description", ""),
        }

    def _generate_por(self, checks: list) -> dict:
        """Generate a proof-of-resolution record."""
        return {
            "status": "verified",
            "checks_passed": len([c for c in checks if c["passed"]]),
            "checks_total": len(checks),
            "generated_at": datetime.utcnow().isoformat(),
        }
