"""
LLM Judge: Evaluates manual/subjective criteria using an LLM.
This replaces the default 'always False' behavior for manual checks
in the VerifierAgent.
"""

import json
import os
from typing import Optional


class LLMJudge:
    """
    Uses an LLM to evaluate whether a submission satisfies a manual criterion.
    Works with any OpenAI-compatible API endpoint.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model

    def evaluate(self, criterion: dict, submission: dict, contract: dict) -> dict:
        """
        Ask the LLM to judge whether the submission meets the criterion.
        Returns a dict with passed (bool) and reasoning (str).
        """
        prompt = self._build_prompt(criterion, submission, contract)

        if not self.api_key:
            return {
                "passed": False,
                "reasoning": "No API key configured. Set OPENAI_API_KEY environment variable.",
            }

        try:
            import requests

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a verification judge for a conviction market. "
                                "Evaluate whether the builder's submission satisfies the given criterion. "
                                "Respond ONLY with valid JSON: {\"passed\": true/false, \"reasoning\": \"...\"}"
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.0,
                },
                timeout=30,
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return json.loads(content)

        except Exception as e:
            return {"passed": False, "reasoning": f"LLM call failed: {str(e)}"}

    def _build_prompt(self, criterion: dict, submission: dict, contract: dict) -> str:
        return f"""Criterion to evaluate:
- Description: {criterion.get('description', 'N/A')}
- Type: {criterion.get('type', 'manual')}

Bounty context:
- Domain: {contract.get('domain', 'N/A')}
- Title: {contract.get('title', 'N/A')}

Builder submission:
{json.dumps(submission, indent=2)}

Does this submission satisfy the criterion? Respond with JSON: {{"passed": true/false, "reasoning": "your reasoning"}}"""
