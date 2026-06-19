import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.cli import cmd_verify
import argparse


def test_verify_runs(capsys):
    args = argparse.Namespace(
        manifest="examples/sample_manifest.json",
        files=["SwapForm.tsx"],
        outputs=["0 failures"],
        llm=False,
        window=24,
    )
    cmd_verify(args)
    output = capsys.readouterr().out
    assert "Verification FAILED" in output or "Verification PASSED" in output
