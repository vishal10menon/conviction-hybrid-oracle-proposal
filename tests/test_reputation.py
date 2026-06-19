import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.reputation.weighting import ReputationLedger


def test_initial_reputation():
    ledger = ReputationLedger()
    assert ledger.get_reputation("alice") == 100.0


def test_challenge_success_increases():
    ledger = ReputationLedger()
    ledger.record_event("alice", "challenge_success", {"market": "test"})
    assert ledger.get_reputation("alice") == 115.0


def test_challenge_failure_decreases():
    ledger = ReputationLedger()
    ledger.record_event("bob", "challenge_failure", {"market": "test"})
    assert ledger.get_reputation("bob") == 75.0


def test_reputation_floor():
    ledger = ReputationLedger()
    for _ in range(20):
        ledger.record_event("carol", "bond_slashed", {"market": "test"})
    assert ledger.get_reputation("carol") >= 0.0


def test_challenge_weight():
    ledger = ReputationLedger()
    ledger.record_event("alice", "challenge_success", {"market": "test"})
    weight = ledger.get_challenge_weight("alice")
    assert weight == 1.15


def test_challenge_weight_clamped():
    ledger = ReputationLedger()
    for _ in range(27):
        ledger.record_event("dave", "challenge_success", {"market": "test"})
    weight = ledger.get_challenge_weight("dave")
    assert weight == 5.0



def test_bond_requirement_inversely_scales():
    ledger = ReputationLedger()
    ledger.record_event("alice", "challenge_success", {"market": "test"})
    bond_alice = ledger.get_bond_requirement("alice", 100.0)
    bond_bob = ledger.get_bond_requirement("bob", 100.0)
    assert bond_alice < bond_bob


def test_history_recorded():
    ledger = ReputationLedger()
    ledger.record_event("alice", "challenge_success", {"market": "test"})
    history = ledger.get_history("alice")
    assert len(history) == 1
    assert history[0]["type"] == "challenge_success"
