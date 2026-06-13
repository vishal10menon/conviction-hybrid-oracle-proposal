"""
Semantic Contract Parser: Reads and validates the structured manifest
that defines what 'done' means for a given conviction market bounty.
"""

import json
from pathlib import Path
from typing import Optional


REQUIRED_FIELDS = ["manifest_id", "domain", "bounty_id", "criteria", "version"]
CRITERION_FIELDS = ["id", "type", "description"]


class SemanticContract:
    """Represents a parsed semantic contract (manifest)."""

    def __init__(self, manifest: dict):
        self.manifest = manifest
        self.manifest_id = manifest.get("manifest_id")
        self.domain = manifest.get("domain")
        self.bounty_id = manifest.get("bounty_id")
        self.criteria = manifest.get("criteria", [])
        self.version = manifest.get("version", "0.1")

    @classmethod
    def from_file(cls, path: str) -> "SemanticContract":
        with open(path, "r") as f:
            manifest = json.load(f)
        return cls(manifest)

    def validate(self) -> list:
        """Return list of validation errors (empty = valid)."""
        errors = []
        for field in REQUIRED_FIELDS:
            if field not in self.manifest:
                errors.append(f"Missing required field: {field}")

        for i, criterion in enumerate(self.criteria):
            for field in CRITERION_FIELDS:
                if field not in criterion:
                    errors.append(f"Criterion {i}: missing field '{field}'")
        return errors

    def to_dict(self) -> dict:
        return self.manifest
