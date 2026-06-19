"""
Reputation-Weighted Scoring: Tracks participant reputation and uses it
to weight challenge power, oracle influence, and bond requirements.
This is the economic backbone of the HAOO challenge game.
"""

import json
from datetime import datetime
from typing import Optional


class ReputationLedger:
    """
    Maintains reputation scores for participants in the conviction market.
    Scores update based on verification accuracy, challenge outcomes,
    and bonding behavior.
    """

    INITIAL_REPUTATION = 100.0
    CHALLENGE_SUCCESS_BONUS = 15.0
    CHALLENGE_FAILURE_PENALTY = -25.0
    VERIFICATION_BONUS = 5.0
    BOND_SLASH_PENALTY = -40.0

    def __init__(self, ledger_path: Optional[str] = None):
        self.participants: dict = {}
        self.ledger_path = ledger_path
        if ledger_path:
            self._load()

    def _load(self):
        try:
            with open(self.ledger_path, "r") as f:
                self.participants = json.load(f)
        except FileNotFoundError:
            self.participants = {}

    def _save(self):
        if self.ledger_path:
            with open(self.ledger_path, "w") as f:
                json.dump(self.participants, f, indent=2)

    def get_reputation(self, participant_id: str) -> float:
        return self.participants.get(participant_id, {}).get("reputation", self.INITIAL_REPUTATION)

    def get_history(self, participant_id: str) -> list:
        return self.participants.get(participant_id, {}).get("history", [])

    def record_event(self, participant_id: str, event_type: str, details: dict) -> dict:
        """Record a reputation event and update the score."""
        if participant_id not in self.participants:
            self.participants[participant_id] = {
                "reputation": self.INITIAL_REPUTATION,
                "history": [],
            }

        entry = self.participants[participant_id]

        delta = self._compute_delta(event_type, details)
        entry["reputation"] = max(0, entry["reputation"] + delta)

        event_record = {
            "type": event_type,
            "delta": delta,
            "new_score": entry["reputation"],
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
        }
        entry["history"].append(event_record)
        self._save()

        return event_record

    def _compute_delta(self, event_type: str, details: dict) -> float:
        if event_type == "challenge_success":
            return self.CHALLENGE_SUCCESS_BONUS
        elif event_type == "challenge_failure":
            return self.CHALLENGE_FAILURE_PENALTY
        elif event_type == "verification_complete":
            return self.VERIFICATION_BONUS
        elif event_type == "bond_slashed":
            return self.BOND_SLASH_PENALTY
        return 0.0

    def get_challenge_weight(self, participant_id: str) -> float:
        """
        Compute the conviction-weighted stake for challenge power.
        Weight = reputation / 100, clamped between 0.1 and 5.0.
        """
        rep = self.get_reputation(participant_id)
        weight = rep / 100.0
        return max(0.1, min(5.0, weight))

    def get_bond_requirement(self, participant_id: str, base_bond: float) -> float:
        """
        Bond requirement scales inversely with reputation.
        Higher reputation = lower bond required.
        """
        weight = self.get_challenge_weight(participant_id)
        return base_bond / weight

    def to_dict(self) -> dict:
        return self.participants
