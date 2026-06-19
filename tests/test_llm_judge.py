import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.verifier_agent.llm_judge import LLMJudge


def test_judge_without_api_key():
    judge = LLMJudge(api_key="")
    criterion = {"id": "c1", "type": "manual", "description": "UI renders correctly"}
    submission = {"id": "sub-1", "files": [], "outputs": []}
    contract = {"domain": "test", "title": "test bounty"}
    result = judge.evaluate(criterion, submission, contract)
    assert result["passed"] is False
    assert "No API key" in result["reasoning"]


def test_judge_builds_prompt():
    judge = LLMJudge(api_key="")
    criterion = {"id": "c1", "type": "manual", "description": "Deployed to testnet"}
    submission = {"id": "sub-1", "files": ["deploy.py"], "outputs": []}
    contract = {"domain": "defi", "title": "Token launch"}
    prompt = judge._build_prompt(criterion, submission, contract)
    assert "Deployed to testnet" in prompt
    assert "defi" in prompt
