# Adversarial Case: When the Verifier Is Wrong or the Evidence Is Incomplete

This document shows why the narrow POC needs both a semantic verifier and an optimistic challenge path.

A happy-path example is not enough. A serious verification primitive must also show how it behaves under ambiguity, incomplete evidence, or verifier error.

## Purpose of this example

This scenario is designed to test three things:

1. whether the verifier can detect material ambiguity
2. whether a bad or incomplete verifier judgment can be challenged
3. whether the challenge path can correct a provisional result before capital is released

The objective is not to prove that the verifier is perfect.

The objective is to prove that the system remains accountable when the verifier is imperfect.

## Milestone

**Milestone ID:** `cm-demo-002`

**Title:** Merge bounded assertion-flow update without touching restricted configuration

### Success criteria

The milestone is considered complete only if all of the following conditions hold:

1. PR #187 is merged into `main`
2. `contracts/AssertionGate.sol` is modified
3. `README.md` is modified
4. CI passes on the merge commit
5. no files under `tokenomics/` are modified
6. no files under `config/production/` are modified
7. merge occurs before `2026-06-20T23:59:59Z`

### Required evidence

- repository URL
- PR URL
- merge commit hash
- changed file list
- CI run URL
- merge timestamp

## Submission

The builder submits the following evidence:

- Repository URL: `https://github.com/example/oracle-demo`
- PR URL: `https://github.com/example/oracle-demo/pull/187`
- Merge commit hash: `0xdef456demo`
- CI run URL: `https://github.com/example/oracle-demo/actions/runs/123456789`
- Merge timestamp: `2026-06-20T18:11:02Z`

The builder also includes a short note claiming that the PR only updates the assertion flow and supporting documentation.

## What actually happened

The PR did modify:

- `contracts/AssertionGate.sol`
- `README.md`

However, it also changed:

- `config/production/release.json`

This path should have triggered failure under the milestone contract.

In addition, the linked CI run is incomplete in the exported metadata because one required status check did not appear in the verifier’s first-pass evidence fetch.

## Faulty verifier result

Suppose the verifier produces the following provisional result:

- **Result:** `SUCCESS`
- **Confidence:** medium
- **Trace hash:** `0xtrace456demo`
- **Notes:** required files detected, no forbidden tokenomics changes detected, CI appears successful, deadline satisfied

This is a bad result.

Even if the verifier missed the production config change because of an evidence-normalization bug, the protocol should still be able to catch and correct the error before payout.

## Why the verifier got it wrong

This scenario illustrates two realistic failure modes.

### Failure mode 1: Incomplete forbidden-path checking

The verifier checks for forbidden changes under `tokenomics/`, but fails to inspect `config/production/` correctly because the path filter used by the parser is incomplete.

### Failure mode 2: Partial CI evidence

The verifier sees a green status from one CI source and incorrectly treats the merge as fully successful, even though the required check set is incomplete in the fetched metadata.

Neither error is exotic. Both are the kind of bounded implementation mistakes that a realistic POC should expect.

## What the challenge window is for

After the verifier posts the provisional assertion onchain, the system enters the liveness window.

During this period:

- the result is visible
- the reasoning trace is inspectable
- the evidence can be reviewed
- challengers can dispute before capital is released

A challenger inspects the PR diff and sees that `config/production/release.json` was modified.

The challenger also notices that the trace references only partial CI evidence and does not prove that the full required CI set passed.

## Challenge

The challenger submits a dispute with bond.

### Challenger claim

The verifier result should not settle because:

1. the PR modified a forbidden path under `config/production/`
2. the CI evidence is incomplete, so successful completion is not established
3. the verifier’s reasoning trace does not justify a clean `SUCCESS`

## Expected dispute outcome

The dispute reviewer inspects:

- the PR diff
- the changed file list
- the reasoning trace
- the CI evidence references
- the milestone contract

The reviewer determines:

- the milestone contract was violated because a forbidden production config path changed
- the verifier trace did not adequately support the CI conclusion
- the provisional `SUCCESS` assertion was incorrect

### Final resolution

- provisional assertion overturned
- milestone result set to `FAILURE` or returned for resubmission, depending on protocol design
- challenger bond returned, and challenger rewarded if the system uses reward sharing
- verifier trust weight reduced, if verifier accountability is implemented
- payout remains locked

## Why this example matters

This case demonstrates the actual purpose of the hybrid design.

If the protocol trusted the verifier blindly, capital would have moved incorrectly.

If the protocol relied on price alone, the dispute would be indirect and noisy.

In the hybrid model:

- the verifier provides the default-path interpretation
- the trace makes the interpretation inspectable
- the liveness window creates a real review period
- the challenge mechanism prevents bad automation from becoming final settlement

That is the point of the system.

## Alternative handling: `AMBIGUOUS` instead of bad `SUCCESS`

A stronger verifier would not output `SUCCESS` here.

It would output `AMBIGUOUS`.

A better provisional result would be:

- **Result:** `AMBIGUOUS`
- **Confidence:** low
- **Notes:** production config path may have changed; CI evidence set appears incomplete; manual review recommended

This is a healthier system behavior.

The narrow POC should not be judged only on whether it can produce correct positive verdicts. It should also be judged on whether it can avoid false confidence.

## What this adversarial case tests

This example is useful because it tests:

- forbidden-path detection
- evidence completeness checks
- reasoning trace quality
- challenger usability
- dispute override logic
- whether payout gating actually works under verifier error

## Design lesson

The verifier should not be trusted because it is intelligent.

It should be trusted only to the extent that it is inspectable, challengeable, and overrideable.

That is why the optimistic layer is not a bolt-on component. It is the accountability layer that makes semantic automation usable in the first place.

## Bottom line

A serious milestone-verification system should be evaluated not only by its happy-path accuracy, but by how safely it fails.

This adversarial case is intended to make that standard explicit.
