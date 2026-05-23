# Hybrid Agentic-Optimistic Oracle for Conviction Markets: Resolving Reflexivity in Long-Tail Coordination

**Author:** Vishal Menon (@vmcrypta)  
**Date:** April 24, 2026, updated May 2026  
**Submitted to:** Conviction Markets Request for Builders  
**Repository:** https://github.com/vishal10menon/conviction-hybrid-oracle-proposal

## Follow-up analysis

- [Failure Modes and Toy Model for Hybrid Agentic-Optimistic Oracles](./failure-modes-and-toy-model.md)

## TL;DR

Conviction Markets aims to release capital only when work is actually verified.

The problem is that in low-liquidity or long-tail coordination markets, market price is often too weak to serve as the sole verification layer. It can reflect speculation, liquidity constraints, or strategic suppression more than whether a builder actually completed the milestone.

This creates a reflexivity trap: a builder can ship real work, submit valid evidence, and still fail to get paid because the market signal never cleanly converges on reality.

This repository proposes a **Hybrid Agentic-Optimistic Oracle (HAOO)**, an agent-in-the-middle architecture that separates:

- **semantic verification of work**, performed by a specialized verifier agent operating against a curated semantic contract
- **economic finality**, enforced through an optimistic challenge window and decentralized dispute process

This updated version also narrows the proposal toward a first **milestone-gated onchain POC** and adds concrete **prior art and evidence** from live oracle systems and recent research.

## Abstract

Conviction Markets seeks to create an onchain coordination infrastructure in which capital is released only upon verified completion of work. Pure Futarchy-based verification, which uses market price as the oracle, suffers from a fundamental **reflexivity trap**: in low-liquidity or long-tail markets, speculative volatility or adversarial capital can suppress price signals, preventing legitimate builders from receiving payment even after successful delivery. This creates a self-fulfilling failure mode that undermines the protocol’s core thesis.

This paper proposes a **Hybrid Agentic-Optimistic Oracle (HAOO)**, or "Agent-in-the-Middle" architecture. The design decouples **semantic verification of work** (performed by a specialized Verifier Agent operating against a curated semantic contract) from **economic finality** (enforced through an optimistic challenge window weighted by the protocol’s reputation and conviction modules). By transforming verification into an automated, auditable trail rather than a speculative voting game, HAOO resolves the Resolver Trilemma for long-tail coordination while preserving economic security and decentralization.

The proposal integrates directly with Conviction Markets’ reputation, conviction, and curation layers, positioning **curation** as the primary intellectual moat of the protocol. This updated version also scopes a narrow first implementation focused on milestone gating for bounded, software-verifiable tasks.

## 1. Introduction: The Reflexivity Problem in Futarchy

The central claim of Conviction Markets is that sustained commitment should compound into fractionalized ownership of outcomes, with capital released only upon verified completion of work. This requires a verification primitive that satisfies three competing constraints, the **Resolver Trilemma**:

- **Velocity**: Must operate at machine speed to support autonomous agents.
- **Security**: Must resist collusion, semantic subversion, and manipulation.
- **Decentralization**: Must avoid reliance on centralized curators or trusted oracles.

Pure Futarchy, as pioneered by MetaDAO, uses market price as the oracle. While elegant in theory, this model fails in practice for long-tail markets due to **reflexivity** and **liquidity-bound truth**:

- **Reflexive Veto**: If the market anticipates failure, token price drops. This makes it impossible for the builder to be paid even if the work is later delivered, creating a self-fulfilling prophecy.
- **Speculative Manipulation**: In thin markets, a single capital-heavy actor can suppress price regardless of actual delivery quality.
- **Semantic Gap**: Market prices are a coarse aggregate signal. They cannot reliably distinguish between failed execution and macro downturn, or between genuine non-delivery and liquidity shock.

These failure modes are especially acute in the "Zero-to-Many" phase of new conviction markets, where liquidity is thin and the verification primitive is most needed.

The key point is not simply that price is imperfect. It is that **verification itself becomes reflexive**. A builder can complete the work, submit valid proof, and still fail to receive payout because the market never expresses that truth clearly enough. At that point, the protocol is no longer only pricing outcomes, it is actively shaping whether builders can survive long enough to deliver them.

## 2. The Proposed Primitive: Agent-in-the-Middle (AiM) Architecture

We propose an **Agent-in-the-Middle** design that places a domain-specific **Verifier Agent** between the builder’s submission and the market’s repricing mechanism. This creates a hybrid system where semantic verification is performed at machine speed, while economic finality remains decentralized through an optimistic challenge game.

### 2.1 Formal Workflow

Let M be a conviction market defined by a semantic contract C = (P, E, V), where:

- **P**: Problem statement and success criteria  
- **E**: Required evidence schema, for example GitHub commit hash, onchain transaction, signed attestation  
- **V**: Verification logic manifest  

A builder submits a claim (w, π), where w is the work artifact and π is cryptographic proof of authorship.

The **Verifier Agent** A_v computes:

A_v(C, w, π) → (b, τ)

where b ∈ {SUCCESS, FAILURE} and τ is a verifiable Proof of Reasoning (PoR) trace.

This assertion is posted onchain and enters an **Optimistic Liveness Window** L, typically 12 to 48 hours.

### 2.2 Optimistic Challenge Game with Reputation Weighting

During L, any participant with sufficient **Conviction-Weighted Stake** w_c, derived from their reputation score and staked conviction in the specific market, may issue a challenge by posting a bond B.

- **Passive Path**: If no valid challenge is raised, the assertion is accepted as final and capital is released according to the milestone tranche.
- **Active Path**: A challenge escalates the dispute to a **Reputation-Weighted Social Court**. The court resolves using the agent’s PoR trace, additional evidence, and stake-weighted voting. Incorrect challenges result in bond slashing; dishonest agents lose "Trust Weight."

This design ensures that the market acts as a **monitor**, not the primary judge, significantly reducing the attack surface for liquidity manipulation.

### 2.3 Security Properties

- **Against Reflexivity**: Builder payoff is tied to semantic verification, not instantaneous token price.
- **Against Collusion**: Reputation slashing and bond requirements raise the cost of coordinated attacks.
- **Semantic Richness**: The Verifier Agent closes the semantic gap by interpreting unstructured work against a formally defined manifest.
- **Verifiability**: The PoR trace, combined with execution in a TEE or ZK-proof wrapper, provides an auditable computational record.

### 2.4 Milestone Gating

Milestone gating is the operational core of the design.

Even when the verifier agent returns **SUCCESS**, the system does **not** immediately unlock capital. Instead, the result enters a liveness window during which:

- the assertion is publicly visible
- the reasoning trace can be inspected
- challengers can post a bond and dispute the verdict
- capital remains gated until the window closes

This matters because without gating, the verifier agent would become an unchecked oracle. With gating, the system preserves machine-speed verification while keeping decentralized accountability intact.

In other words, the proposal is not "AI decides and funds move." It is "AI proposes a structured verification result, and the protocol uses optimistic review before capital unlocks."

## 3. Integration with Conviction Markets Modules

The HAOO primitive is designed for direct composability with existing Conviction Markets components:

- **Reputation & Conviction Weighting**: Challenge power and oracle selection are gated by a participant’s conviction score and historical accuracy. This creates a self-improving "Oracle Market" where reliable agents rise in influence.
- **Curation as Moat**: High-quality curation now includes not only the problem statement but the semantic manifest C. The library of verified manifests becomes a public good that any conviction market can fork, making curation the protocol’s primary intellectual moat.
- **Automated Audit Trail**: Verification becomes a transparent, reproducible process rather than a speculative voting game, aligning with the protocol’s goal of "capital only moves when work is verified."

## 4. Narrow Onchain POC

The full design is broad, but the first implementation should be narrow.

The initial goal is **not** to solve all categories of work verification. The initial goal is to test whether a semantic verifier plus optimistic challenge window can support milestone-gated capital release for **bounded, software-verifiable tasks**.

### First milestone classes

The narrow POC should focus on milestones such as:

1. GitHub PR merged into a specified branch
2. contract deployed to a target testnet address
3. test suite passing under declared conditions
4. signed artifact or attestation published
5. deterministic documentation or configuration updates

These milestone types are intentionally constrained. They are structured enough to support semantic contracts without pretending that every kind of work can be reduced to machine-verifiable rules immediately.

### Narrow POC flow

1. **Curator defines milestone**
   - success criteria
   - evidence schema
   - verifier instructions
   - challenge window parameters

2. **Builder submits work**
   - repo / PR / commit hash
   - deployment proof or attestation
   - optional explanatory context

3. **Verifier agent evaluates**
   - compares submission against contract
   - emits SUCCESS / FAILURE / possibly AMBIGUOUS in early prototypes
   - outputs structured reasoning trace

4. **Onchain assertion**
   - contract stores milestone id
   - result
   - hash of reasoning trace
   - timestamp
   - challenge deadline

5. **Challenge window**
   - watchers inspect the trace
   - challengers dispute by bonding capital
   - dispute escalates if necessary

6. **Settlement**
   - if undisputed, milestone payment unlocks
   - if disputed, the case enters slower adjudication

### What this POC proves

If successful, the narrow POC would validate:

- semantic contracts are usable in bounded coordination settings
- verifier agents can reduce ambiguity in milestone resolution
- milestone gating protects against over-trusting automation
- payout can be tied to auditable delivery rather than price movement alone

## 5. Prior Art & Evidence

This proposal is not purely theoretical. Several close analogs already exist.

### 5.1 UMA’s Optimistic Truth Bot

The closest live analog is UMA’s **Optimistic Truth Bot (OTB)**. OTB is a modular agentic system designed to propose answers to UMA’s optimistic oracle with clear reasoning, evidence gathering, and human dispute backstop. Its architecture includes a router, specialized solvers, and an overseer module that filters and audits outputs before they ever reach the oracle.

This is directionally very close to HAOO:
- agent generates first-pass semantic resolution
- optimistic system handles economic challenge
- humans remain the safety net

### 5.2 Polymarket + UMA

Polymarket uses UMA’s optimistic oracle to resolve real-money prediction markets:
- a proposer submits an outcome
- a challenge window opens
- if undisputed, the answer finalizes
- if disputed, it escalates to UMA’s DVM

This validates the optimistic layer of the HAOO design at real economic scale. HAOO does not replace this logic. It strengthens the proposal layer by adding a semantic verifier before optimistic settlement.

### 5.3 Hybrid AI-governance oracle research

Recent oracle research increasingly argues that AI should function as a **complementary layer of inference and filtering**, not as a replacement for trust assumptions. Hybrid architectures combining AI, staking/slashing, governance escalation, and human-in-the-loop review are now a recognized design pattern rather than a speculative novelty.

### 5.4 What is new here

The novelty here is not simply "AI + oracle."

The novelty is applying a hybrid semantic-plus-optimistic structure specifically to **milestone-gated capital release in reflexive coordination markets**, where the main failure is not only truth reporting, but payout under conditions where price is a weak proxy for truth.

## 6. Threat Model and Incentive Compatibility

**Primary Threats**:
- Adversarial builder submitting low-quality work that passes the agent.
- Adversarial challenger using frivolous disputes to suppress valid work.
- Compromised or biased Verifier Agent.

**Mitigations**:
- Bond requirements and reputation slashing make bad behavior expensive.
- The PoR trace makes agent decisions reproducible and auditable.
- Curation-defined manifests reduce ambiguity in what constitutes "success."
- Milestone gating prevents agent outputs from becoming final without an opportunity for challenge.

**Incentive Alignment**:
- Builders are incentivized to produce high-quality, verifiable work.
- Challengers are incentivized to challenge only with strong evidence.
- The protocol benefits from a flywheel where better curation leads to better agents, which leads to higher-quality markets and increased participation.

## 7. Comparison to Existing Approaches

- **Pure Futarchy (MetaDAO)**: Elegant but vulnerable to reflexivity in thin markets.
- **Optimistic Oracles (UMA)**: Provides economic finality but lacks native semantic understanding at the proposal layer.
- **Pure AI Oracles**: High velocity but lack economic accountability and decentralized backstop.

The proposed HAOO model combines the strengths of all three while addressing their respective weaknesses.

## 8. Conclusion and Next Steps

The Hybrid Agentic-Optimistic Oracle resolves the reflexivity trap in long-tail conviction markets by turning verification into an automated, semantically rich audit trail grounded in curated contracts. It protects builders from short-term market noise while preserving the economic security of a decentralized social layer.

This primitive is the necessary infrastructure for a true Agentic Coordination Layer, where sustained commitment compounds into ownership, grounded in verifiable reality rather than speculative vibes.

### Practical next steps

Rather than jumping immediately to maximal design complexity, the next steps should be:

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

