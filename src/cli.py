"""
CLI Entry Point: Run the full verification pipeline from terminal.

Usage:
  python -m src.cli verify examples/sample_manifest.json --files SwapForm.tsx --outputs "0 failures"
  python -m src.cli verify examples/sample_manifest.json --files SwapForm.tsx --outputs "0 failures" --llm
  python -m src.cli challenge examples/sample_manifest.json --challenger user1 --reason "wrong output" --bond 100
"""

import argparse
import json
import sys

from src.verifier_agent.agent import VerifierAgent
from src.semantic_contract.parser import SemanticContract
from src.challenge_game.window import ChallengeWindow


def cmd_verify(args):
    contract = SemanticContract.from_file(args.manifest)
    errors = contract.validate()
    if errors:
        print(f"Invalid manifest: {errors}")
        sys.exit(1)

    agent = VerifierAgent(
        domain=contract.domain,
        contract_path=args.manifest,
        use_llm=args.llm,
    )

    submission = {
        "id": "cli-submission",
        "files": args.files or [],
        "outputs": args.outputs or [],
    }

    report = agent.verify(submission)

    print(json.dumps(report, indent=2))

    if report["all_passed"]:
        window = ChallengeWindow(report, window_hours=args.window)
        print(f"\nVerification PASSED. Challenge window open for {args.window}h.")
        print(f"Window closes at: {window.closes_at}")
    else:
        failed = [c for c in report["checks"] if not c["passed"]]
        print(f"\nVerification FAILED. {len(failed)} criterion(s) not met:")
        for c in failed:
            print(f"  - [{c['type']}] {c.get('details', c.get('reasoning', 'unknown'))}")


def cmd_challenge(args):
    report = {"all_passed": True}
    window = ChallengeWindow(report, window_hours=args.window)

    result = window.challenge(args.challenger, args.reason, args.bond)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Conviction Markets HAOO CLI")
    sub = parser.add_subparsers(dest="command")

    verify = sub.add_parser("verify", help="Run verification against a manifest")
    verify.add_argument("manifest", help="Path to semantic contract JSON")
    verify.add_argument("--files", nargs="*", help="Files in the submission")
    verify.add_argument("--outputs", nargs="*", help="Outputs from the submission")
    verify.add_argument("--llm", action="store_true", help="Use LLM judge for manual criteria")
    verify.add_argument("--window", type=int, default=24, help="Challenge window in hours")

    challenge = sub.add_parser("challenge", help="Raise a challenge against a verification")
    challenge.add_argument("manifest", help="Path to semantic contract JSON")
    challenge.add_argument("--challenger", required=True, help="Challenger ID")
    challenge.add_argument("--reason", required=True, help="Reason for challenge")
    challenge.add_argument("--bond", type=float, required=True, help="Bond amount")
    challenge.add_argument("--window", type=int, default=24, help="Challenge window in hours")

    args = parser.parse_args()

    if args.command == "verify":
        cmd_verify(args)
    elif args.command == "challenge":
        cmd_challenge(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
