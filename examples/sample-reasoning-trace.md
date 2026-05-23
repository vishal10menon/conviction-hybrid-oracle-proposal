# Sample Reasoning Trace
## Milestone ID: cm-demo-001

### Submitted evidence
- Repository URL: https://github.com/example/oracle-demo
- PR URL: https://github.com/example/oracle-demo/pull/142
- Merge commit hash: 0xabc123demo
- CI run URL: https://github.com/example/oracle-demo/actions/runs/987654321
- Merge timestamp: 2026-06-14T18:42:11Z

---

## Contract checks

### Check 1: PR merged into main
- Result: PASS
- Evidence: PR metadata confirms merge state = merged, base branch = main

### Check 2: Required file `contracts/AssertionGate.sol` modified
- Result: PASS
- Evidence: file appears in PR diff

### Check 3: Required file `README.md` modified
- Result: PASS
- Evidence: file appears in PR diff

### Check 4: Forbidden files under `tokenomics/` untouched
- Result: PASS
- Evidence: no path beginning with `tokenomics/` appears in PR diff

### Check 5: CI status passed
- Result: PASS
- Evidence: linked CI run completed successfully on merge commit

### Check 6: Deadline satisfied
- Result: PASS
- Evidence: merge timestamp precedes 2026-06-15T23:59:59Z

---

## Final result
**SUCCESS**

## Confidence
High

## Ambiguities detected
None material.

## Summary
The submission satisfies all declared success criteria. No forbidden changes were detected, CI passed, and the merge occurred before the milestone deadline.

## Trace hash
0xtrace123demo
