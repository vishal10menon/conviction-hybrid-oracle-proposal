# MVP Parameters for the Narrow POC

This document defines a default operating configuration for the first narrow proof of concept.

The goal is not to present final token-economic values. The goal is to make the prototype concrete enough to implement, test, and critique.

## Design objective

The MVP should answer one practical question:

> Can a semantic verifier, combined with milestone gating and an optimistic challenge window, support capital release for a bounded class of software-verifiable tasks more reliably than price alone?

The parameters below are chosen for clarity, simplicity, and falsifiability, not for final production optimization.

## Default MVP configuration

| Parameter | Default MVP value | Why this value |
|---|---|---|
| Milestone class | Software-verifiable repository tasks | Evidence is inspectable, structured, and realistic for a first prototype |
| Verifier outputs | `SUCCESS`, `FAILURE`, `AMBIGUOUS` | Avoids forcing false certainty in edge cases |
| Liveness window | 24 hours | Long enough for review, short enough to keep settlement usable |
| Challenger bond | 100 USDC equivalent | Large enough to discourage spam, small enough to permit meaningful participation |
| Eligible challengers | Open in early test environments, reputation-gated in later deployments | Maximizes learning early, raises quality later |
| Assertion payload onchain | milestone ID, result, trace hash, timestamp, challenge deadline, settlement state | Keeps onchain state minimal while preserving auditability |
| Full reasoning trace | Offchain, content-addressed, hash-linked to onchain assertion | Cheaper and easier to iterate while keeping integrity guarantees |
| Evidence sources | GitHub PR metadata, changed file paths, CI status, timestamps, deployment transaction data where relevant | Bounded evidence types are easier to normalize and verify |
| Escalation trigger | Any valid challenge during liveness window, or verifier output of `AMBIGUOUS` | Preserves accountability in disputed or low-confidence cases |
| Final adjudication path | Simple human review, council, or reputation-weighted dispute layer depending on deployment stage | The MVP should not block on a fully mature court design |
| Payout condition | Capital unlocks only after unchallenged settlement or successful dispute resolution | Prevents automatic release on raw verifier output alone |

## Verifier output policy

The verifier should not be forced into binary judgments when the evidence is materially incomplete or conflicting.

### `SUCCESS`
Use when all required checks pass, evidence is sufficient, and no material ambiguity remains.

### `FAILURE`
Use when one or more fail-fast conditions are triggered, such as:

- required file missing
- forbidden file modified
- CI failed
- deadline missed
- PR not merged

### `AMBIGUOUS`
Use when the milestone may or may not be complete, but the evidence is incomplete, inconsistent, or not confidently interpretable.

Typical triggers include:

- missing CI record
- inconsistent timestamps
- partial or malformed metadata
- unclear mapping between evidence and contract criteria
- evidence that suggests likely completion but does not prove it cleanly

The `AMBIGUOUS` state exists to avoid false confidence and to route edge cases into review.

## Why the liveness window is 24 hours

The liveness window is the conceptual center of the narrow POC.

A positive verifier result should not trigger immediate capital release. The system needs a bounded period in which:

- the assertion becomes visible
- the reasoning trace can be inspected
- challengers can dispute if necessary
- the protocol can distinguish default-path settlement from exceptional-path escalation

A 24-hour default is a reasonable first benchmark. It is easy to understand, operationally simple, and short enough for early milestone markets.

This should later be stress-tested against:

- challenge frequency
- settlement latency
- false positives that escape challenge
- curator and challenger workload

## Why the challenger bond is 100 USDC equivalent

The bond should be large enough to make frivolous disputes costly, but not so large that only wealthy actors can challenge obviously bad assertions.

For the MVP, 100 USDC equivalent is a practical placeholder. It is not sacred. The point is to establish a meaningful economic threshold while gathering data on challenge quality.

Later versions may tune bond size based on:

- milestone value
- historical challenger accuracy
- dispute frequency
- reputation score
- market liquidity conditions

## Open versus reputation-gated challengers

The narrow POC should not overfit to a mature governance system that does not yet exist.

A sensible progression is:

### Early prototype
Open challengers, simple bond requirement, manual or semi-structured adjudication.

### Later prototype
Reputation-weighted challenger eligibility, differentiated bond sizing, and clearer routing into a formal dispute layer.

This lets the MVP test the core primitive first, without pretending that the final governance design is already solved.

## Onchain and offchain boundary

The MVP should keep intelligence offchain and accountability onchain.

### Onchain responsibilities
- assertion state
- timestamps
- challenge deadline
- bond posting
- settlement state
- payout gating

### Offchain responsibilities
- evidence collection
- evidence normalization
- semantic evaluation
- reasoning trace generation
- ambiguity assessment
- artifact linking

This split keeps the prototype implementable while preserving enough integrity for real testing.

## What these parameters are trying to optimize

The MVP is not optimizing for maximum decentralization or maximum automation on day one.

It is optimizing for:

- interpretability
- bounded scope
- adversarial legibility
- implementation realism
- useful failure discovery

If these parameters produce clear traces, meaningful challenges, and tolerable settlement latency, the system is worth iterating further.

## What should be measured during testing

The MVP should be judged on operational metrics, not narrative appeal.

Suggested metrics:

- false positive rate
- false negative rate
- frequency of `AMBIGUOUS` outputs
- challenge frequency
- proportion of successful challenges
- average settlement latency
- curator effort per milestone
- reviewer effort per disputed milestone
- percentage of milestones that remain cleanly machine-checkable

## Parameters most likely to change later

The following values should be treated as adjustable:

- liveness window duration
- challenger bond amount
- challenger eligibility criteria
- trace standardization requirements
- when `AMBIGUOUS` is mandatory
- adjudication forum design
- mapping between reputation and challenge rights

The MVP should not try to lock these down prematurely.

## Bottom line

These parameters make the narrow POC concrete enough to build without pretending the final system design is finished.

That is the correct level of ambition for this stage.
