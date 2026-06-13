# Hybrid Agentic-Optimistic Oracle for Conviction Markets

A proposal for milestone verification in thin or long-tail coordination markets.

**Author:** Vishal Menon (@vmcrypta)  
**Date:** April 24, 2026, updated May 2026  
**Submitted to:** Conviction Markets Request for Builders  
**Repository:** https://github.com/vishal10menon/conviction-hybrid-oracle-proposal

## MVP Implementation

This repository contains both the original proposal and a working prototype of the core verification pipeline.

### Project Structure

src/
verifier_agent/       # Agent that checks submissions against contracts
agent.py            # Core VerifierAgent class
proof_of_resolution.py
semantic_contract/    # Manifest parser and validator
parser.py           # SemanticContract class
validator.py
challenge_game/       # Optimistic challenge window logic
window.py           # ChallengeWindow class
resolver.py
reputation/           # Reputation-weighted scoring (pending token design)
weighting.py
utils/
config.py
contracts/              # Solidity or on-chain components (future)
tests/
examples/
sample_manifest.json


### Current Status

- [x] Verifier Agent skeleton with criterion-based checks
- [x] Semantic Contract parser with validation
- [x] Optimistic Challenge Window with expiry logic
- [ ] Reputation-weighted scoring (awaiting token design)
- [ ] On-chain integration
- [ ] Full test coverage

## TL;DR

Conviction Markets only works if capital can move when work is actually complete.

The problem is that in thin, early, or long-tail markets, price is often too weak to act as the only verification layer. It can reflect speculation, low liquidity, or strategic suppression more than whether the builder really delivered.

That creates a reflexivity problem. A builder can do the work, submit valid evidence, and still fail to get paid because the market signal never cleanly catches up to reality.

This repository proposes a **Hybrid Agentic-Optimistic Oracle (HAOO)**. The core idea is to separate:

- **semantic verification of work**, handled by a verifier agent using a curated semantic contract
- **economic finality**, handled by an optimistic challenge window and dispute process

The claim is intentionally narrow:

> For bounded classes of milestone-based work, especially software-verifiable tasks, a semantic verifier plus optimistic challenge layer may outperform price alone as the first-pass verification primitive.

This is not a claim to have solved the oracle problem in full. It is a narrower proposal for a more credible milestone-resolution primitive.

## The problem

Conviction Markets wants capital to move when work is actually completed.

That requires a verification primitive. If milestone completion is inferred mainly from market price, the mechanism can break in exactly the cases where coordination markets are hardest:

- thin liquidity
- weak price discovery
- semantically rich work
- adversarial or distorted sentiment
- milestones where completion matters more than short-term market expectations

In those settings, price can become a poor proxy for whether the builder actually delivered.

This creates a reflexive failure mode:

1. the market expects failure  
2. price moves against the builder  
3. payout becomes harder or impossible  
4. the builder is penalized even if the work is later delivered  
5. the market's expectation becomes self-fulfilling  

The point is not just that price is noisy. It is that verification itself becomes reflexive.

## The proposal

The proposed primitive is a **Hybrid Agentic-Optimistic Oracle**.

It separates two functions that should not be collapsed into one signal.

### 1. Semantic verification

A verifier evaluates submitted work against a curated milestone contract.

That contract defines:

- **P**: problem statement and success criteria
- **E**: evidence schema
- **V**: verification logic manifest

The verifier produces a provisional result such as:

- `SUCCESS`
- `FAILURE`
- `AMBIGUOUS`

It also emits a structured reasoning trace that maps evidence to checks.

### 2. Economic finality

The verifier result does not settle immediately.

Instead, the protocol posts a minimal assertion and opens an optimistic challenge window. During that period:

- the result is visible
- the trace is inspectable
- challengers can dispute
- settlement remains pending

If no valid challenge is raised, the result finalizes and capital unlocks.

If a challenge is raised, the claim enters a slower dispute path.

The verifier is therefore a high-speed proposer, not a final unquestionable judge.

## Why hybrid?

Each existing approach solves only part of the problem.

| Approach | Strength | Weakness |
|---|---|---|
| Pure price oracle / futarchy | Fast, decentralized signal aggregation | Reflexive, liquidity-sensitive, weak at interpreting complex work |
| Optimistic oracle only | Strong accountability and challengeability | Weak native semantic interpretation |
| AI verifier only | Rich semantic reasoning and fast first-pass evaluation | No credible decentralized backstop if wrong |
| HAOO | Semantic first pass plus challengeable settlement | More system complexity, requires curation and dispute design |

The point of HAOO is not to replace markets, optimistic dispute systems, or human judgment.

The point is to combine:

- semantic interpretation
- inspectability
- challengeability
- payout gating

into a single milestone-resolution flow.

## Why not just use optimism plus curation?

Because optimism alone does not solve the semantic gap.

A dispute layer can accept or reject claims, but it does not itself provide a strong first-pass interpretation of milestone evidence.

In this design:

- curation defines what counts as success
- the verifier evaluates the evidence
- the optimistic layer allows challenge and override
- capital moves only if the result survives review

## Why not just trust the verifier?

Because that would reduce the system to a centralized oracle with better language.

The verifier should be:

- fast
- inspectable
- challengeable
- overrideable

The goal is not to eliminate social review.

The goal is to reduce how often full social review is needed while preserving a credible path for escalation when the verifier is wrong.

## Narrow POC

The first implementation path is intentionally narrow.

It focuses on **software-verifiable milestones**, because these are bounded enough to support:

- structured evidence
- machine-assisted verification
- auditable traces
- meaningful disputes

Examples include:

- PR merged into a specified branch
- required files modified
- forbidden paths untouched
- CI passing at merge time
- contract deployment matching declared conditions

This is not a general-purpose oracle for all work.

It is a bounded test of whether a stronger milestone verification primitive can outperform price alone in a narrow but important class of tasks.

For the full implementation path, see [narrow-poc.md](./narrow-poc.md).

## Repository guide

### Core proposal
- [README.md](./README.md)  
  Top-level thesis, mechanism design, and positioning

### Bounded implementation path
- [narrow-poc.md](./narrow-poc.md)  
  First implementation path for software-verifiable milestones

### Default MVP settings
- [parameters.md](./parameters.md)  
  Default settings for liveness windows, bond sizing, verifier outputs, onchain payload, and settlement assumptions

### Failure-path analysis
- [adversarial-case.md](./adversarial-case.md)  
  Worked example showing how verifier error or incomplete evidence should be handled before payout

### Follow-up analysis
- [failure-modes-and-toy-model.md](./failure-modes-and-toy-model.md)  
  Failure modes and toy model for the hybrid oracle design

### Example artifacts
- [examples/sample-semantic-contract.json](./examples/sample-semantic-contract.json)  
  Example semantic contract for a bounded software milestone

- [examples/sample-reasoning-trace.md](./examples/sample-reasoning-trace.md)  
  Example verifier output showing checks, evidence, and final judgment

## What success looks like

This proposal should not be judged by whether it solves the entire oracle problem.

It should be judged by narrower criteria:

- can milestones be encoded clearly enough for machine-assisted evaluation?
- can evidence be ingested and normalized reliably?
- can the verifier emit legible, auditable traces?
- can challenge windows catch bad or ambiguous outputs before payout?
- can settlement remain usable without forcing every case into slow governance?

If the answer is yes, then Conviction Markets gets a more credible milestone-resolution primitive for long-tail coordination.

## Scope

### In scope

- milestone-gated resolution for bounded classes of work
- software-verifiable tasks as the first proving ground
- semantic contracts
- verifier-generated reasoning traces
- optimistic challenge windows
- minimal onchain assertion and payout gating

### Not in scope

- a universal oracle for all forms of work
- a final token-economic design
- a fully permissionless verifier market from day one
- proof that arbitrary real-world labor can be reduced to binary machine verdicts
- a complete final dispute court architecture

Narrowness is a feature here.

The point is to test a falsifiable mechanism, not to overclaim a finished system.

## Why this matters for Conviction Markets

If Conviction Markets wants capital to move when work is actually verified, then milestone resolution cannot rely only on market price in environments where price is thin, noisy, or strategically distortable.

This repository proposes a more credible alternative:

- curation defines the contract
- the verifier performs first-pass semantic evaluation
- the optimistic layer preserves accountability
- capital moves only after provisional truth survives challenge

That is the mechanism claim.

## Practical next steps

A sensible implementation sequence is:

1. formalize milestone templates and evidence schemas  
2. build an offchain verifier for software-verifiable milestones  
3. deploy a minimal onchain assertion contract on testnet  
4. test liveness windows, challenge flow, and payout gating  
5. refine parameters based on error cases, dispute frequency, and settlement latency  

## Open questions

- How strict should semantic contracts be without becoming brittle?
- When should ambiguity be surfaced rather than forced into binary resolution?
- Should challenge rights be fully open, reputation-gated, or hybrid?
- Which classes of work should never be verifier-agent-first?
- What incentive design best deters spam challenges and bad proposals?

## Bottom line

This repository proposes a narrower alternative to pure price-based milestone verification.

Instead of asking price to do all interpretive work, it separates:

- semantic verification of milestone completion
- economic finality through optimistic, challengeable settlement

If this bounded approach works for software-verifiable tasks, it could provide a stronger verification primitive for long-tail coordination markets.

## Contact

This is an open contribution.

If this direction is useful, I would be happy to iterate on the architecture, tighten the bounded POC, or explore an implementation-oriented research sprint around milestone verification for Conviction Markets.
