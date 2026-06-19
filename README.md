# Hybrid Agentic-Optimistic Oracle for Conviction Markets

**Author:** Vishal Menon (@vmcrypta)  
**Date:** April 24, 2026  
**Submitted to:** Conviction Markets Request for Builders  
**Repository:** https://github.com/vishal10menon/conviction-hybrid-oracle-proposal

---

## Abstract

Conviction Markets seeks to create an on-chain coordination infrastructure in which capital is released only upon verified completion of work. Pure Futarchy-based verification suffers from a fundamental **reflexivity trap**: in low-liquidity or long-tail markets, speculative volatility can suppress price signals, preventing builders from receiving payment even after successful delivery.

This paper proposes a **Hybrid Agentic-Optimistic Oracle (HAOO)**. The design decouples **semantic verification of work** (performed by a Verifier Agent operating against a curated semantic contract) from **economic finality** (enforced through an optimistic challenge window weighted by reputation and conviction modules).

---

## MVP Implementation

This repository contains both the original proposal and a working prototype of the core verification pipeline.

### Project Structure

```plaintext
conviction-hybrid-oracle-proposal/
│
├── README.md
│   └── Research proposal + architecture overview
│
├── requirements.txt
│   └── Python dependencies
│
├── src/
│   │
│   ├── cli.py
│   │   └── CLI entry point for running verification
│   │
│   ├── verifier_agent/
│   │   ├── agent.py
│   │   │   └── Core VerifierAgent logic
│   │   ├── llm_judge.py
│   │   │   └── LLM evaluation for subjective/manual criteria
│   │   └── proof_of_resolution.py
│   │       └── Proof-of-Reasoning trace generation
│   │
│   ├── semantic_contract/
│   │   ├── parser.py
│   │   │   └── Parse manifest JSON into SemanticContract
│   │   └── validator.py
│   │       └── Validate contract schema
│   │
│   ├── challenge_game/
│   │   ├── window.py
│   │   │   └── ChallengeWindow expiry and dispute lifecycle
│   │   └── resolver.py
│   │       └── Final challenge resolution logic
│   │
│   ├── reputation/
│   │   └── weighting.py
│   │       └── Reputation scoring and conviction-weighted bonds
│   │
│   └── utils/
│       └── config.py
│           └── Environment variables and constants
│
├── contracts/
│   └── (planned)
│       ├── AssertionRegistry.sol
│       ├── ChallengeManager.sol
│       └── ReputationOracle.sol
│
├── tests/
│   ├── test_agent.py
│   ├── test_parser.py
│   ├── test_validator.py
│   ├── test_window.py
│   ├── test_reputation.py
│   └── test_cli.py
│
├── examples/
│   └── sample_manifest.json
│       └── Example semantic contract input
│
├── .gitignore
└── LICENSE
```

### Current Status

- [x] Semantic contract parser with validation
- [x] Verifier agent with criterion-based checks
- [x] LLM-backed judge for manual/subjective criteria
- [x] Optimistic challenge window with expiry logic
- [x] Reputation-weighted scoring and bond mechanics
- [x] CLI entry point for terminal-based verification
- [x] 28 passing tests across all modules
- [ ] On-chain assertion contract on testnet (planned)
- [ ] ZK-PoR integration for verifiable agent reasoning (future)

### Quick Start

```bash
git clone https://github.com/vishal10menon/conviction-hybrid-oracle-proposal.git

cd conviction-hybrid-oracle-proposal

pip install -r requirements.txt

# Run verification
python -m src.cli verify examples/sample_manifest.json \
--files SwapForm.tsx \
--outputs "0 failures"

# Run with LLM judge
export OPENAI_API_KEY=your_key

python -m src.cli verify examples/sample_manifest.json \
--files SwapForm.tsx \
--outputs "0 failures" \
--llm

# Run tests
python -m pytest tests/ -v
```

---

## 1. The Reflexivity Problem in Futarchy

Conviction Markets requires a verification primitive that satisfies the **Resolver Trilemma**:

- Velocity  
- Security  
- Decentralization  

Pure Futarchy uses market price as the oracle but fails in long-tail markets due to:

- **Reflexive Veto** — Anticipated failure suppresses price, preventing payment even if work is delivered.
- **Speculative Manipulation** — Thin markets allow capital-heavy actors to suppress price.
- **Semantic Gap** — Market prices cannot distinguish failed execution from macro conditions.

---

## 2. Agent-in-the-Middle Architecture

The HAOO design places a **Verifier Agent** between the builder's submission and the market's repricing mechanism.

Let a conviction market be defined by:

```text
C = (P, E, V)
```

Where:

- **P** → Problem statement and success criteria  
- **E** → Required evidence schema  
- **V** → Verification logic manifest  

The Verifier Agent computes:

```text
A_v(C, w, π) → (b, τ)
```

Where:

- **b ∈ {SUCCESS, FAILURE}**
- **τ = Proof of Reasoning trace**

This assertion enters an **Optimistic Liveness Window (L)** of approximately **12–48 hours**.

### Challenge Game

**Passive Path**
- No challenge raised
- Assertion accepted
- Capital released

**Active Path**
- Challenge escalates to a Reputation-Weighted Social Court
- Incorrect challengers lose bonds

### Security Properties

- Builder payoff tied to verification, not token price
- Reputation slashing raises attack cost
- PoR trace provides auditability

---

## 3. Integration with Conviction Markets

- Reputation and conviction weighting  
- Curation as protocol moat  
- Automated audit trail

---

## 4. Comparison to Existing Approaches

| Approach | Limitation |
|---|---|
| Pure Futarchy (MetaDAO) | Reflexivity risk |
| Optimistic Oracles (UMA) | No semantic understanding |
| Pure AI Oracles | No economic accountability |

HAOO combines the strengths of all three.

---

## 5. Conclusion and Future Work

The HAOO resolves the reflexivity trap by turning verification into an automated, semantically rich audit trail.

Future work includes:

- ZK-PoR in TEE environments  
- Liquidity stress simulation  
- Empirical evaluation on Conviction Markets testnets  

This design is submitted as an open contribution.

---

## References

- MetaDAO Futarchy Design  
- UMA Optimistic Oracle Protocol  
- Kleros Decentralized Court  
- Conviction Markets Whitepaper (2026)