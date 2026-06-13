import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.challenge_game.window import ChallengeWindow


def test_challenge_window_lifecycle():
    report = {"all_passed": False}
    window = ChallengeWindow(report)
    assert window.status.value == "open"
    window.challenge("user1", "bug", 100.0)
    assert window.status.value == "challenged"
    window.resolve("overturn")
    assert window.status.value == "resolved"
