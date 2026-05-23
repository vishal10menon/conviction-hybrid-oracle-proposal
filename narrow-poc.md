# Narrow Onchain POC
## A bounded first implementation for Hybrid Agentic-Optimistic Oracle (HAOO)

## 1. Purpose

This document narrows the broader HAOO proposal into a first implementation path that is intellectually serious, technically bounded, and economically testable.

The objective is not to prove that all forms of human work can be verified by an agentic oracle. That would be too broad, too ambiguous, and too easy to dismiss as speculative.

The objective is much narrower:

> Can a semantic verifier, combined with milestone gating and an optimistic challenge window, support capital release for a bounded class of software-verifiable tasks more reliably than price alone?

This is the smallest version of the proposal that still tests the real thesis.

If the answer is yes, the model can later expand into more complex categories of work. If the answer is no, that failure will also be informative, because it will reveal whether the bottleneck lies in semantic contract design, verifier quality, or dispute economics.

---

## 2. Why a narrow POC is the correct first step

The broad HAOO proposal makes a large claim: that long-tail coordination markets need a stronger verification primitive than pure price signals.

That claim should not be tested first in the hardest possible environment.

A sensible first implementation should have:

- relatively explicit success criteria
- evidence that can be structured and inspected
- disputes that are rare but meaningful
- milestone outcomes that can plausibly be reduced to binary or near-binary resolution
- enough ambiguity to make verification non-trivial, but not so much ambiguity that every case becomes governance by default

Software-verifiable milestones satisfy these constraints better than other categories of work.

They are not perfectly objective, but they are bounded enough to support:
- semantic contracts
- machine-assisted verification
- auditable evidence trails
- optimistic dispute windows

This makes them the right first environment for testing the primitive.

---

## 3. The core thesis being tested

The narrow POC is built to test four linked claims:

### Claim 1
A semantic contract can express milestone completion more richly than market price alone.

### Claim 2
A verifier agent can produce a useful first-pass judgment against that contract.

### Claim 3
Milestone gating can prevent agent outputs from becoming final without review.

### Claim 4
An optimistic challenge window can preserve decentralized accountability without forcing every resolution into slow governance.

The POC succeeds if these four claims hold together in practice for a bounded class of tasks.

---

## 4. What the POC is, and what it is not

### The POC is:
- a test of a **verification primitive**
- a milestone-gated release mechanism for structured tasks
- a hybrid architecture with offchain semantic verification and onchain economic finality
- a bounded experiment in resolver design

### The POC is not:
- a full general-purpose oracle for all work
- a fully permissionless verifier market from day one
- a final token-economic design
- a replacement for all human judgment
- proof that arbitrary real-world work can be reduced to binary machine verdicts

This distinction matters. The value of the POC comes from being narrow enough to be falsifiable.

---

## 5. Design principles

The narrow POC should be built around five principles.

### 5.1 Verifiable before scalable
The first version should optimize for correctness and legibility, not throughput.

### 5.2 Semantic before economic
The system should first decide whether the work appears complete according to the contract, before deciding whether capital should move.

### 5.3 Optimistic before adjudicated
The default path should assume honest verification, but preserve a path to challenge.

### 5.4 Gated before final
A positive verifier result should not release funds instantly. There must be an intermediate gating period.

### 5.5 Narrow before general
The first version should prove one bounded primitive, not overclaim a universal oracle.

---

## 6. Scope of the first milestone classes

The initial milestone types should be constrained to tasks where evidence is inspectable and the success criteria can be formalized with reasonable precision.

## Recommended first classes

### A. GitHub merge milestone
Example:
- PR merged into a specified branch
- required files modified
- tests green
- merge completed before deadline

### B. Testnet deployment milestone
Example:
- contract deployed to a specified testnet
- deployment address matches expected metadata
- verification artifact uploaded
- basic interaction check succeeds

### C. Signed artifact publication milestone
Example:
- a report, config, spec, or output file published
- signature matches expected identity
- hash matches submission claim
- required fields present

### D. Deterministic repo change milestone
Example:
- config or documentation update satisfying explicit structural requirements
- file diff conforms to a bounded rule set
- no forbidden files modified

These classes are useful because they preserve real ambiguity while remaining auditable.

---

## 7. Semantic contract schema

Each milestone should be instantiated as a semantic contract:

$$
C = (P, E, V)
$$

where:

- $$P$$ = problem statement and success criteria
- $$E$$ = evidence schema
- $$V$$ = verification logic manifest

## Suggested schema fields

### 7.1 Milestone metadata
- milestone ID
- market ID
- title
- description
- deadline
- curator identity

### 7.2 Success criteria
- explicit completion conditions
- required outputs
- allowed tolerances
- prohibited substitutions

### 7.3 Evidence schema
- repo URL
- PR number
- commit hash
- deployment transaction
- contract address
- signed artifact hash
- attestation source

### 7.4 Verification logic manifest
- required checks
- ordering of checks
- confidence thresholds
- ambiguity triggers
- fail-fast conditions
- escalation conditions

### 7.5 Challenge parameters
- liveness period
- bond size
- eligible challengers
- dispute forum
- final adjudicator path

The point of the semantic contract is not to eliminate judgment. It is to make judgment inspectable.

---

## 8. Actors in the system

The narrow POC should model four actors clearly.

### 8.1 Curator
Defines the milestone and semantic contract.

### 8.2 Builder
Submits the work artifact and evidence of completion.

### 8.3 Verifier Agent
Evaluates the submission against the semantic contract and emits a structured result.

### 8.4 Challenger
Reviews the verifier output during the gating window and disputes if necessary.

Optionally, a fifth role can exist:

### 8.5 Final adjudicator
A slower human or reputation-weighted resolution layer that only activates when disputes occur.

---

## 9. The proposed lifecycle

## Step 1: Curator defines the milestone

The curator writes the milestone in a way that is interpretable by both humans and machines.

This is where the system’s real quality begins. Weak milestones produce weak verification. Strong milestones produce high-quality machine assistance and low dispute frequency.

The milestone must define:
- what counts as completion
- what evidence is admissible
- what the verifier should check
- what conditions require human escalation

## Step 2: Builder submits evidence

The builder submits:
- the work artifact
- the evidence package
- proof of authorship or provenance
- optional explanatory context

This package should be sufficient for an informed third party to inspect the claim.

## Step 3: Verifier agent evaluates

The verifier agent performs:
- evidence collection
- evidence normalization
- rule checking
- semantic interpretation
- conflict detection
- ambiguity scoring

It returns one of the following:

- `SUCCESS`
- `FAILURE`
- `AMBIGUOUS` (optional in early prototypes)

Alongside that result, it emits a reasoning trace.

## Step 4: Reasoning trace generation

The reasoning trace is critical.

It should include:
- evidence references
- explicit checks passed or failed
- rule-to-evidence mapping
- unresolved ambiguities
- confidence assessment
- citations or linked artifacts

Without the trace, the verifier becomes opaque.
With the trace, it becomes inspectable.

## Step 5: Onchain assertion

The verifier result is posted onchain in minimal form.

The assertion contract should record:
- milestone ID
- claimed result
- hash of the reasoning trace
- timestamp
- challenge deadline
- challenger bond amount
- settlement state

The full trace can remain offchain if it is content-addressed and hash-linked to the assertion.

## Step 6: Milestone gating window

This is the crucial “middle gating” stage.

Even if the agent says `SUCCESS`, the system should not release funds immediately.

Instead:
- the result becomes visible
- the trace becomes inspectable
- challengers can review and dispute
- the protocol waits through the liveness period

This stage is what prevents automation from becoming unaccountable.

## Step 7: Challenge or settlement

If no challenge is raised:
- the result finalizes
- milestone payment unlocks

If a challenge is raised:
- the claim enters a slower dispute path
- the dispute forum reviews the trace, evidence, and challenge
- final resolution overrides the provisional assertion if necessary

---

## 10. Diagram

```mermaid
flowchart TD
    A[Curator defines milestone and semantic contract] --> B[Builder submits work artifact and evidence]
    B --> C[Verifier Agent evaluates submission]
    C --> D[Structured reasoning trace produced]
    D --> E[Onchain assertion posted]
    E --> F[Milestone gating window opens]

    F --> G{Challenge raised?}
    G -->|No| H[Assertion finalizes]
    H --> I[Milestone payment unlocks]

    G -->|Yes| J[Dispute escalates to adjudication layer]
    J --> K[Final resolution]
    K --> L[Payment unlocks or remains blocked]
