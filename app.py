import os
import hmac
import hashlib
import traceback

from flask import Flask, request, jsonify

from src.github_verifier.pipeline import VerificationPipeline
from src.github_verifier.github_checks import GitHubChecker


app = Flask(__name__)

WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")

pipeline = VerificationPipeline()
github = GitHubChecker()


def verify_signature(payload, signature):
    if not WEBHOOK_SECRET or not signature:
        return False

    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


@app.get("/")
def health():
    return jsonify({
        "status": "ok",
        "service": "HAOO verification webhook",
    })


@app.post("/webhook")
def webhook():
    signature = request.headers.get("X-Hub-Signature-256", "")

    if not verify_signature(request.data, signature):
        return jsonify({"error": "Invalid webhook signature"}), 401

    event = request.headers.get("X-GitHub-Event", "")

    if event != "pull_request":
        return jsonify({
            "status": "ignored",
            "event": event,
        })

    payload = request.get_json(silent=True) or {}
    action = payload.get("action", "")

    if action not in ["opened", "synchronize", "reopened"]:
        return jsonify({
            "status": "ignored",
            "action": action,
        })

    try:
        repository = payload["repository"]
        pull_request = payload["pull_request"]

        owner = repository["owner"]["login"]
        repo_name = repository["name"]
        pr_number = pull_request["number"]

        report = pipeline.run(
            owner,
            repo_name,
            pr_number,
            "examples/sample_manifest.json",
        )

        comment = format_comment(report)

        github.post_comment(
            owner,
            repo_name,
            pr_number,
            comment,
        )

        return jsonify({
            "status": "verified",
            "pr": f"#{pr_number}",
            "all_passed": report["all_passed"],
        })

    except Exception as error:
        traceback.print_exc()
        return jsonify({
            "error": str(error),
        }), 500


def format_comment(report):
    status = "PASSED" if report["all_passed"] else "FAILED"

    lines = [
        f"## HAOO Verification Report: {status}",
        "",
        f"**PR:** #{report['pr_number']}",
        f"**Repository:** {report['repo']}",
        "",
        "### GitHub checks",
        "",
        "| Check | Status | Details |",
        "|---|---|---|",
    ]

    for check in report["github_checks"]:
        result = "PASS" if check["passed"] else "FAIL"

        lines.append(
            f"| `{check['criterion_id']}` | {result} | "
            f"{check['details']} |"
        )

    lines.extend([
        "",
        "### Agent checks",
        "",
    ])

    for check in report["agent_checks"]:
        result = "PASS" if check["passed"] else "FAIL"

        lines.append(
            f"- `{check['criterion_id']}`: {result} "
            f"({check['details']})"
        )

    lines.extend([
        "",
        "---",
        "*Verified by HAOO, Hybrid Agentic-Optimistic Oracle*",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
