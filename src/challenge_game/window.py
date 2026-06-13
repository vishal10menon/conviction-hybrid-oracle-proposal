"""
Optimistic Challenge Window: After a Verifier Agent marks a submission as
verified, there is a time window during which anyone can challenge the
result. If unchallenged, capital is released automatically.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


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

    def __init__(self, verification_report: dict, window_hours: int = DEFAULT_WINDOW_HOURS):
        self.verification_report = verification_report
        self.window_hours = window_hours
        self.opened_at = datetime.utcnow()
        self.closes_at = self.opened_at + timedelta(hours=window_hours)
        self.status = ChallengeStatus.OPEN
        self.active_challenge: Optional[dict] = None

    def challenge(self, challenger_id: str, reason: str, bond_amount: float) -> dict:
        """Raise a challenge against the verification."""
        if self.status != ChallengeStatus.OPEN:
            return {"error": f"Window is {self.status.value}, cannot challenge"}

        if datetime.utcnow() > self.closes_at:
            self.status = ChallengeStatus.EXPIRED
            return {"error": "Challenge window has expired"}

        self.active_challenge = {
            "challenger_id": challenger_id,
            "reason": reason,
            "bond_amount": bond_amount,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.status = ChallengeStatus.CHALLENGED
        return {"status": "challenged", "details": self.active_challenge}

    def resolve(self, ruling: str) -> dict:
        """Resolve the challenge. Ruling: 'uphold' or 'overturn'."""
        if self.status != ChallengeStatus.CHALLENGED:
            return {"error": "No active challenge to resolve"}

        self.status = ChallengeStatus.RESOLVED
        return {
            "status": "resolved",
            "ruling": ruling,
            "bond_slashed": ruling == "uphold" if self.active_challenge else False,
            "capital_released": ruling == "uphold",
        }

    def check_expiry(self) -> dict:
        """Check if window has expired (capital auto-released)."""
        if self.status == ChallengeStatus.OPEN and datetime.utcnow() > self.closes_at:
            self.status = ChallengeStatus.EXPIRED
            return {"status": "expired", "capital_released": True}
        return {"status": self.status.value, "capital_released": False}
