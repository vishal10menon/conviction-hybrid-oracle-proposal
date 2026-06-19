"""
Optimistic Challenge Window: After a Verifier Agent marks a submission as
verified, there is a time window during which anyone can challenge the
result. If unchallenged, capital is released automatically.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from src.reputation.weighting import ReputationLedger


class ChallengeStatus(Enum):
    OPEN = "open"
    CHALLENGED = "challenged"
    RESOLVED = "resolved"
    EXPIRED = "expired"


class ChallengeWindow:
    """
    Manages the optimistic window after verification.
    Default window: 24 hours.
    """

    DEFAULT_WINDOW_HOURS = 24
    BASE_BOND_REQUIREMENT = 100.0

    def __init__(
        self,
        verification_report: dict,
        window_hours: int = DEFAULT_WINDOW_HOURS,
        reputation_ledger: Optional[ReputationLedger] = None,
    ):
        self.verification_report = verification_report
        self.window_hours = window_hours
        self.opened_at = datetime.utcnow()
        self.closes_at = self.opened_at + timedelta(hours=window_hours)
        self.status = ChallengeStatus.OPEN
        self.active_challenge: Optional[dict] = None
        self.reputation_ledger = reputation_ledger or ReputationLedger()

    def challenge(self, challenger_id: str, reason: str, bond_amount: float) -> dict:
        """Raise a challenge against the verification."""
        if self.status != ChallengeStatus.OPEN:
            return {"error": f"Window is {self.status.value}, cannot challenge"}

        if datetime.utcnow() > self.closes_at:
            self.status = ChallengeStatus.EXPIRED
            return {"error": "Challenge window has expired"}

        required_bond = self.reputation_ledger.get_bond_requirement(
            challenger_id, self.BASE_BOND_REQUIREMENT
        )
        if bond_amount < required_bond:
            return {
                "error": f"Bond too low. Required: {required_bond:.1f}, provided: {bond_amount:.1f}"
            }

        weight = self.reputation_ledger.get_challenge_weight(challenger_id)

        self.active_challenge = {
            "challenger_id": challenger_id,
            "reason": reason,
            "bond_amount": bond_amount,
            "challenge_weight": weight,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.status = ChallengeStatus.CHALLENGED
        return {"status": "challenged", "details": self.active_challenge}

    def resolve(self, ruling: str) -> dict:
        """Resolve the challenge. Ruling: 'uphold' or 'overturn'."""
        if self.status != ChallengeStatus.CHALLENGED:
            return {"error": "No active challenge to resolve"}

        challenger_id = self.active_challenge["challenger_id"]

        if ruling == "uphold":
            self.reputation_ledger.record_event(
                challenger_id, "challenge_success", {"bond": self.active_challenge["bond_amount"]}
            )
        elif ruling == "overturn":
            self.reputation_ledger.record_event(
                challenger_id, "challenge_failure", {"bond": self.active_challenge["bond_amount"]}
            )

        self.status = ChallengeStatus.RESOLVED
        return {
            "status": "resolved",
            "ruling": ruling,
            "bond_slashed": ruling == "uphold",
            "capital_released": ruling == "uphold",
        }

    def check_expiry(self) -> dict:
        """Check if window has expired (capital auto-released)."""
        if self.status == ChallengeStatus.OPEN and datetime.utcnow() > self.closes_at:
            self.status = ChallengeStatus.EXPIRED
            return {"status": "expired", "capital_released": True}
        return {"status": self.status.value, "capital_released": False}
