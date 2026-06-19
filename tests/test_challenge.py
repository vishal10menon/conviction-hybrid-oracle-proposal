import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.challenge_game.window import ChallengeWindow
from src.reputation.weighting import ReputationLedger


def test_challenge_window_lifecycle():
    report = {"all_passed": False}
    window = ChallengeWindow(report)
    assert window.status.value == "open"
    window.challenge("user1", "bug", 100.0)
    assert window.status.value == "challenged"
    window.resolve("overturn")
    assert window.status.value == "resolved"


def test_bond_too_low_rejected():
    report = {"all_passed": False}
    window = ChallengeWindow(report)
    result = window.challenge("user1", "bug", 10.0)
    assert "error" in result
    assert "Bond too low" in result["error"]


def test_reputation_updates_on_resolve():
    ledger = ReputationLedger()
    report = {"all_passed": False}
    window = ChallengeWindow(report, reputation_ledger=ledger)
    window.challenge("alice", "wrong output", 100.0)
    window.resolve("uphold")
    assert ledger.get_reputation("alice") == 115.0


def test_reputation_decreases_on_overturn():
    ledger = ReputationLedger()
    report = {"all_passed": False}
    window = ChallengeWindow(report, reputation_ledger=ledger)
    window.challenge("bob", "bad challenge", 100.0)
    window.resolve("overturn")
    assert ledger.get_reputation("bob") == 75.0
