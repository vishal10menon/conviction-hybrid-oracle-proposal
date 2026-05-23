# Hybrid Agentic-Optimistic Oracle for Conviction Markets: Resolving Reflexivity in Long-Tail Coordination

**Author:** Vishal Menon (@vmcrypta)  
**Date:** April 24, 2026, updated May 2026  
**Submitted to:** Conviction Markets Request for Builders  
**Repository:** https://github.com/vishal10menon/conviction-hybrid-oracle-proposal

## Follow-up analysis

- [Failure Modes and Toy Model for Hybrid Agentic-Optimistic Oracles](./failure-modes-and-toy-model.md)
- [Narrow Onchain POC](./narrow-poc.md)
- To make the first implementation path more concrete, example artifact shapes are included under `/examples`, including a sample semantic contract and a sample reasoning trace.


## TL;DR

Conviction Markets only works if capital can move when work is actually complete.

The problem is that in thin, early, or long-tail markets, price is often too weak to act as the only verification layer. It can reflect speculation, low liquidity, or strategic suppression more than whether the builder really delivered.

That creates a reflexivity problem. A builder can do the work, submit valid evidence, and still fail to get paid because the market signal never cleanly catches up to reality.

This repo proposes a **Hybrid Agentic-Optimistic Oracle (HAOO)**. The core idea is to separate:

- **semantic verification of work**, handled by a verifier agent using a curated semantic contract
- **economic finality**, handled by an optimistic challenge window and dispute process

This updated version also narrows the idea into a first milestone-gated onchain POC and adds concrete prior art from live oracle systems and recent research. A more detailed implementation path is outlined in [Narrow Onchain POC](./narrow-poc.md).

## Abstract

Conviction Markets aims to create an onchain coordination system where capital is released only when work has been verified. Pure Futarchy-style verification, where market price acts as the oracle, runs into a basic problem in low-liquidity or long-tail markets. Speculation, timing mismatches, or adversarial capital can suppress the price signal, which means a builder may complete useful work and still fail to get paid. This weakens the core promise of the protocol.

This paper proposes a **Hybrid Agentic-Optimistic Oracle (HAOO)**, or "Agent-in-the-Middle" architecture. The design separates **semantic verification of work** from **economic finality**. A verifier agent checks whether submitted work satisfies a curated semantic contract, while an optimistic challenge window gives the broader system a chance to dispute bad assertions before payout. The goal is to turn verification into an auditable process rather than a speculative voting game.

The proposal is designed to plug into Conviction Markets’ reputation, conviction, and curation layers. This updated version also narrows the first implementation to milestone-gated verification for bounded, software-verifiable tasks.

## 1. Introduction: The Reflexivity Problem in Futarchy

The central claim of Conviction Markets is that sustained commitment should compound into ownership of outcomes, with capital released only upon verified completion of work. To do that well, the protocol needs a verification primitive that can satisfy three competing constraints:

- **Velocity**: it must be fast enough to support machine-speed coordination
- **Security**: it must resist manipulation, collusion, and weak evidence
- **Decentralization**: it must avoid collapsing into a centralized review process

Pure Futarchy, as used in systems like MetaDAO, makes price the oracle. In theory that is elegant. In practice, it breaks down in thin or early markets for at least three reasons:

- **Reflexive veto**: if the market expects failure, price drops, and the builder may fail to get paid even if the work is later completed
- **Speculative manipulation**: in thin markets, a well-capitalized actor can suppress price even when delivery quality is real
- **Semantic gap**: price is too coarse to distinguish actual non-delivery from macro conditions, timing noise, or liquidity shocks

These problems are most severe in the "Zero-to-Many" stage, when a market is still early and participation is thin.

The point is not just that price is noisy. It is that **verification itself becomes reflexive**. The protocol stops merely observing outcomes and starts affecting whether builders can survive long enough to complete them.

## 2. The Proposed Primitive: Agent-in-the-Middle (AiM) Architecture

The proposal introduces an **Agent-in-the-Middle** design that places a domain-specific **Verifier Agent** between the builder’s submission and the market’s repricing mechanism. This creates a hybrid system where semantic verification happens first, while finality remains subject to an optimistic challenge process.

### 2.1 Formal Workflow

Let a conviction market be defined by a semantic contract C = (P, E, V), where:

- **P**: problem statement and success criteria  
- **E**: required evidence schema, such as GitHub commit hash, onchain transaction, or signed attestation  
- **V**: verification logic manifest  

A builder submits a claim (w, π), where w is the work artifact and π is proof of authorship or provenance.

The **Verifier Agent** A_v computes:

A_v(C, w, π) → (b, τ)

where b ∈ {SUCCESS, FAILURE} and τ is a verifiable Proof of Reasoning (PoR) trace.

This assertion is posted onchain and enters an **Optimistic Liveness Window** L, typically 12 to 48 hours.

### 2.2 Optimistic Challenge Game with Reputation Weighting

During L, any participant with sufficient **Conviction-Weighted Stake** w_c, derived from reputation and staked conviction in the relevant market, may challenge the assertion by posting a bond B.

- **Passive path**: if no valid challenge is raised, the assertion is accepted and capital is released according to the milestone tranche
- **Active path**: if challenged, the case escalates to a **Reputation-Weighted Social Court** or equivalent dispute layer. The court evaluates the reasoning trace, the evidence, and the challenge itself. Incorrect challengers lose their bond. Dishonest agents lose trust and future influence

This keeps the market in the role of monitor rather than first-pass judge.

### 2.3 Security Properties

- **Against reflexivity**: builder payout is tied to semantic verification, not immediate token price
- **Against collusion**: reputation slashing and challenge bonds raise the cost of bad behavior
- **Against semantic ambiguity**: the verifier agent checks work against an explicit manifest rather than relying on raw price movement
- **For auditability**: the reasoning trace provides a structured record that can be inspected and challenged

### 2.4 Milestone Gating

Milestone gating is the practical center of the design.

Even when the verifier agent returns **SUCCESS**, the protocol should not unlock capital immediately. Instead, the result enters a liveness window in which:

- the assertion is visible
- the reasoning trace can be reviewed
- challengers can dispute the verdict
- capital stays locked until the window closes

This matters because without gating, the verifier agent becomes an unchecked oracle. With gating, the system can move fast by default while staying accountable when something looks wrong.

Put differently, the design is not "AI decides and funds move." It is "AI proposes a structured verification result, and the protocol uses optimistic review before payout."

## 3. Integration with Conviction Markets Modules

The HAOO primitive is meant to compose directly with core Conviction Markets modules:

- **Reputation & conviction weighting**: challenge power and verifier selection can be influenced by a participant’s conviction score and historical accuracy
- **Curation as moat**: high-quality curation now includes not only the problem framing but also the semantic manifest C. Over time, a library of good manifests becomes a reusable coordination asset
- **Transparent audit trail**: verification becomes a reproducible process rather than a market mood signal

## 4. Narrow Onchain POC

The full design is broad, but the first implementation should be narrow.

The initial goal is **not** to solve all forms of work verification. The initial goal is to test whether a semantic verifier plus optimistic challenge flow can support milestone-gated capital release for **bounded, software-verifiable tasks**.

### First milestone classes

The first POC should focus on milestones such as:

1. GitHub PR merged into a specified branch
2. contract deployed to a target testnet address
3. test suite passing under declared conditions
4. signed artifact or attestation published
5. deterministic documentation or configuration updates

These tasks are narrow by design. They are structured enough to support semantic contracts without pretending that all work is equally machine-verifiable.

### Narrow POC flow

1. **Curator defines milestone**
   - success criteria
   - evidence schema
   - verifier instructions
   - challenge window settings

2. **Builder submits work**
   - repo / PR / commit hash
   - deployment proof or attestation
   - optional context

3. **Verifier agent evaluates**
   - checks submission against the contract
   - emits SUCCESS / FAILURE / possibly AMBIGUOUS in early prototypes
   - outputs a structured reasoning trace

4. **Onchain assertion**
   - contract stores milestone ID
   - result
   - hash of reasoning trace
   - timestamp
   - challenge deadline

5. **Challenge window**
   - watchers inspect the trace
   - challengers dispute by bonding capital
   - dispute escalates if needed

6. **Settlement**
   - if undisputed, milestone payment unlocks
   - if disputed, the case enters slower adjudication

### What this POC proves

If successful, the narrow POC would validate that:

- semantic contracts are usable in bounded coordination settings
- verifier agents can reduce ambiguity in milestone resolution
- milestone gating protects against over-trusting automation
- payout can be tied to auditable delivery rather than price movement alone

## 5. Prior Art & Evidence

This proposal is not purely theoretical. Several close analogs already exist.

### 5.1 UMA’s Optimistic Truth Bot

The closest live analog is UMA’s **Optimistic Truth Bot (OTB)**. OTB is a modular system designed to propose answers to UMA’s optimistic oracle with evidence gathering, layered routing, and oversight before final submission. Its architecture includes a router, specialized solvers, and an overseer module that filters and audits outputs.

This is directionally very close to HAOO:
- an agent produces a first-pass semantic resolution
- an optimistic system handles challenge and economic review
- humans remain the final safety net

### 5.2 Polymarket + UMA

Polymarket uses UMA’s optimistic oracle to resolve real-money prediction markets:
- a proposer submits an outcome
- a challenge window opens
- if undisputed, the answer finalizes
- if disputed, it escalates to UMA’s DVM

This validates the optimistic settlement layer of the HAOO design at real scale. HAOO does not replace this logic. It strengthens the proposal layer by adding structured semantic verification before settlement.

### 5.3 Hybrid AI-governance oracle research

Recent oracle research increasingly argues that AI should function as a **complementary layer of inference and filtering**, not a replacement for trust assumptions. Hybrid systems that combine AI, staking/slashing, governance escalation, and human review are no longer just hypothetical.

### 5.4 What is new here

The novelty here is not simply "AI + oracle."

The novelty is applying a hybrid semantic-plus-optimistic structure specifically to **milestone-gated capital release in reflexive coordination markets**, where the core failure is not just truth reporting but payout under conditions where price is a weak proxy for delivery.

## 6. Threat Model and Incentive Compatibility

**Primary threats**:
- adversarial builder submits low-quality work that passes the agent
- adversarial challenger raises frivolous disputes to delay valid payout
- verifier agent is compromised or systematically biased

**Mitigations**:
- bond requirements and reputation slashing make bad behavior expensive
- the reasoning trace makes agent decisions legible and auditable
- curation-defined manifests reduce ambiguity in what counts as success
- milestone gating ensures positive agent outputs are never final without a chance to challenge

**Incentive alignment**:
- builders are rewarded for producing verifiable work
- challengers are rewarded only when they challenge with strong evidence
- the protocol improves as better curation produces better manifests, which support better agents and cleaner markets

## 7. Comparison to Existing Approaches

- **Pure Futarchy (MetaDAO)**: elegant but vulnerable to reflexivity in thin markets
- **Optimistic Oracles (UMA)**: strong on economic finality, but weaker on first-pass semantic interpretation
- **Pure AI Oracles**: fast, but weak on accountability and decentralized backstop

The HAOO model tries to combine the strengths of all three while addressing their most obvious weaknesses.

## 8. Conclusion and Next Steps

The Hybrid Agentic-Optimistic Oracle addresses the reflexivity problem in long-tail conviction markets by turning verification into an auditable process grounded in curated contracts rather than short-term price movement.

Its purpose is simple: protect builders from weak market signals without giving up decentralized accountability.

### Practical next steps

Rather than jumping straight into maximal design complexity, the next steps should be:

1. formalize a narrow semantic contract schema
2. build an offchain verifier for software-verifiable milestones
3. deploy a minimal onchain assertion contract on testnet
4. test milestone gating and challenge flow in a bounded environment
5. expand only after the primitive is validated

### Open questions

- How strict should semantic contracts be without becoming brittle?
- When should ambiguity be surfaced rather than forced into binary resolution?
- Should challenge rights be fully open, reputation-gated, or hybrid?
- Which classes of work should never be verifier-agent-first?
- What incentive design best deters spam challenges and bad proposals?

This design is submitted as an open contribution. I am available to iterate on the architecture, contribute implementation design, or explore this as a research sprint or grant-funded collaboration.

## References

- MetaDAO Futarchy Design
- UMA Optimistic Oracle Protocol
- UMA, *AI Is Helping Us Find the Truth. Here's How.*  
  https://blog.uma.xyz/articles/ai-is-helping-us-find-the-truth
- UMA, *Can AI Agents Enhance the Optimistic Oracle?*  
  https://blog.uma.xyz/articles/experiment-can-ai-agents-enhance-uma-oracle
- UMA, *Inside UMA's Optimistic Truth Bot*  
  https://blog.uma.xyz/articles/inside-umas-optimistic-truth-bot
- Giulio Caldarelli, *Can Artificial Intelligence Solve the Blockchain Oracle Problem? Unpacking the Challenges and Possibilities*  
  https://doi.org/10.3389/fbloc.2025.1682623
- Kleros Decentralized Court
- Conviction Markets Whitepaper (2026)
