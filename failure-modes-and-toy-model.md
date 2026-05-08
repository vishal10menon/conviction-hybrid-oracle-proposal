# Failure Modes and Toy Model for Hybrid Agentic-Optimistic Oracles

**Author:** Vishal Menon  
**Status:** Draft for feedback  
**Related proposal:** Hybrid Agentic-Optimistic Oracle for Conviction Markets  
**Date:** 8 May 2026

## Abstract

The original Hybrid Agentic-Optimistic Oracle proposal argues that long-tail coordination markets need a verification layer that separates semantic proof of work from market-price reflexivity. In that design, a verifier agent evaluates submitted work against a semantic contract, then an optimistic challenge window provides economic finality through bonded disputes and reputation-weighted escalation. <citation sourcetype="external" sourceid="Hybrid Agentic-Optimistic Oracle proposal" label="Hybrid Agentic-Optimistic Oracle proposal" url="https://github.com/vishal10menon/conviction-hybrid-oracle-proposal" textbefore="The original Hybrid Agentic-Optimistic Oracle proposal argues that long-tail coordination markets need a verification layer that separates semantic proof of work from market-price reflexivity. In that design, a verifier agent evaluates submitted work against a semantic contract, then an optimistic challenge window provides economic finality through bonded disputes and reputation-weighted escalation."></citation>

This follow-up does not assume that the design works. It does the opposite. It maps the assumptions, failure modes, adversarial cases, incentive tensions, and simulation questions that need to be resolved before a hybrid agentic-optimistic oracle can be treated as a credible primitive.

The core claim is narrow: AI-assisted semantic verification may be useful for high-velocity coordination systems, but only if it is surrounded by explicit evidence schemas, challenge incentives, reputation constraints, and falsifiable tests. The verifier should reduce the cost of judgment. It should not become an unquestioned judge.

## 1. System recap

The proposed system has five moving parts:

1. A market or coordination process defines a task through a semantic contract.
2. A builder submits a work artifact and proof of authorship.
3. A verifier agent evaluates the artifact against the semantic contract.
4. The verifier posts an assertion and reasoning trace.
5. The assertion enters an optimistic challenge window before capital is released.

The original proposal defines the semantic contract as:

$$
C = (P, E, V)
$$

where:

- $$P$$ is the problem statement and success criteria.
- $$E$$ is the required evidence schema.
- $$V$$ is the verification logic manifest.

A builder submits:

$$
(w, \pi)
$$

where:

- $$w$$ is the work artifact.
- $$\pi$$ is proof of authorship.

The verifier agent computes:

$$
A_v(C, w, \pi) \rightarrow (b, \tau)
$$

where:

- $$b \in \{SUCCESS, FAILURE\}$$
- $$\tau$$ is a proof-of-reasoning trace.

If no valid challenge is raised during the liveness window, the assertion finalizes. If challenged, the dispute escalates to a reputation-weighted social court or equivalent dispute-resolution layer. <citation sourcetype="external" sourceid="Hybrid Agentic-Optimistic Oracle proposal" label="Hybrid Agentic-Optimistic Oracle proposal" url="https://github.com/vishal10menon/conviction-hybrid-oracle-proposal" textbefore="If no valid challenge is raised during the liveness window, the assertion finalizes. If challenged, the dispute escalates to a reputation-weighted social court or equivalent dispute-resolution layer."></citation>

The design borrows from several existing families of mechanisms, but combines them differently:

- Futarchy and decision markets use market prices to guide decisions. Robin Hanson’s formulation is “vote on values, but bet on beliefs.” <citation sourcetype="external" sourceid="Robin Hanson, Futarchy" label="Robin Hanson, Futarchy" url="http://hanson.gmu.edu/futarchy.html" textbefore="- Futarchy and decision markets use market prices to guide decisions. Robin Hanson’s formulation is “vote on values, but bet on beliefs.”"></citation>
- MetaDAO’s decision-market model accepts or rejects proposals based on whether traders think a proposal will increase or decrease token value. <citation sourcetype="external" sourceid="MetaDAO docs" label="MetaDAO docs" url="https://docs.metadao.fi/governance/overview" textbefore="- MetaDAO’s decision-market model accepts or rejects proposals based on whether traders think a proposal will increase or decrease token value."></citation>
- UMA’s Optimistic Oracle lets assertions become accepted if they are not disputed within a liveness period; disputed assertions escalate to UMA’s Data Verification Mechanism. <citation sourcetype="external" sourceid="UMA Optimistic Oracle docs" label="UMA Optimistic Oracle docs" url="https://docs.uma.xyz/protocol-overview/how-does-umas-oracle-work" textbefore="- UMA’s Optimistic Oracle lets assertions become accepted if they are not disputed within a liveness period; disputed assertions escalate to UMA’s Data Verification Mechanism."></citation>
- Kleros provides decentralized dispute resolution through randomly selected jurors, evidence submission, voting, appeals, and game-theoretic incentives. <citation sourcetype="external" sourceid="Kleros docs" label="Kleros docs" url="https://docs.kleros.io/" textbefore="- Kleros provides decentralized dispute resolution through randomly selected jurors, evidence submission, voting, appeals, and game-theoretic incentives."></citation>

The proposed HAOO design is not identical to any of these. It uses a verifier agent for first-pass semantic assessment, then uses optimistic challenge mechanics and social/economic escalation as a backstop.

## 2. Why this primitive is being considered

Conviction Markets frames itself as an on-chain coordination layer where “capital only moves when work is verified.” <citation sourcetype="external" sourceid="Conviction Markets" label="Conviction Markets" url="https://www.convictionmarkets.io/" textbefore="Conviction Markets frames itself as an on-chain coordination layer where “capital only moves when work is verified.”"></citation> Its Request for Builders explicitly lists “Verification without managers” and “Disputes without courts” among its open problems. <citation sourcetype="external" sourceid="Conviction Markets Request for Builders" label="Conviction Markets Request for Builders" url="https://www.convictionmarkets.io/submit" textbefore="Its Request for Builders explicitly lists “Verification without managers” and “Disputes without courts” among its open problems."></citation>

That creates a verification problem that pure price-based systems may not fully solve.

A market price can express expected value, belief, and confidence. It is less naturally suited to judging whether a specific work artifact satisfies a specific milestone. This distinction matters most in long-tail markets, where liquidity is thin, information is unevenly distributed, and the boundary between “the work failed” and “the market lost confidence” can blur.

The original proposal calls this the reflexivity problem: if capital release depends too directly on market price, weak price action can become a veto on valid work. <citation sourcetype="external" sourceid="Hybrid Agentic-Optimistic Oracle proposal" label="Hybrid Agentic-Optimistic Oracle proposal" url="https://github.com/vishal10menon/conviction-hybrid-oracle-proposal" textbefore="The original proposal calls this the reflexivity problem: if capital release depends too directly on market price, weak price action can become a veto on valid work."></citation>

The proposed alternative is to separate two functions:

1. **Semantic verification:** Did the builder deliver what the manifest required?
2. **Economic finality:** Is the assertion accepted by the system after a challenge period?

That separation is the main design idea. It is also where most of the failure modes live.

## 3. Core assumptions

The design only works if several assumptions hold.

### Assumption 1: Work can be decomposed into verifiable milestones

The system assumes that useful work can be broken into milestones with observable artifacts.

This is plausible for code commits, deployed contracts, signed attestations, benchmarks, audits, dashboards, test suites, dataset releases, and other artifact-heavy work. It is harder for ambiguous work such as “community growth,” “strategic value,” “quality of research,” or “brand development.”

If the work cannot be decomposed, the verifier agent becomes a vague evaluator. That reintroduces discretionary judgment.

### Assumption 2: A semantic manifest can define success precisely enough

The system depends on the quality of the semantic contract.

A weak manifest creates weak verification. If the success criteria are vague, the verifier is not solving the problem. It is simply inheriting ambiguity from the task definition.

This resembles a lesson from dispute systems. Kleros integration guidance says a dispute policy is crucial because jurors use the policy, the evidence, and court policies to decide cases. <citation sourcetype="external" sourceid="Kleros integration docs" label="Kleros integration docs" url="https://docs.kleros.io/integrations/types-of-integrations/1.-dispute-resolution-integration-plan" textbefore="This resembles a lesson from dispute systems. Kleros integration guidance says a dispute policy is crucial because jurors use the policy, the evidence, and court policies to decide cases."></citation>

In HAOO, the semantic manifest plays a similar role. It is not administrative detail. It is the core object being interpreted.

### Assumption 3: Verifier-agent reasoning can be audited

The verifier cannot simply return “success” or “failure.” It needs to produce an auditable trace.

The original proposal calls this a proof-of-reasoning trace and suggests that future versions could explore trusted execution environments or zero-knowledge proof wrappers. <citation sourcetype="external" sourceid="Hybrid Agentic-Optimistic Oracle proposal" label="Hybrid Agentic-Optimistic Oracle proposal" url="https://github.com/vishal10menon/conviction-hybrid-oracle-proposal" textbefore="The original proposal calls this a proof-of-reasoning trace and suggests that future versions could explore trusted execution environments or zero-knowledge proof wrappers."></citation>

The trace does not need to prove that the model is always correct. It needs to make the decision inspectable enough that challengers can identify errors, omissions, or manipulation.

### Assumption 4: Challengers have enough incentive to dispute bad assertions

Optimistic systems rely on someone watching.

UMA’s Optimistic Oracle accepts data as correct if it is not disputed during the liveness period; if it is disputed, it escalates to the DVM. <citation sourcetype="external" sourceid="UMA Optimistic Oracle docs" label="UMA Optimistic Oracle docs" url="https://docs.uma.xyz/protocol-overview/how-does-umas-oracle-work" textbefore="UMA’s Optimistic Oracle accepts data as correct if it is not disputed during the liveness period; if it is disputed, it escalates to the DVM."></citation> UMA’s bond and liveness guidance notes that bonds create incentives for disputers, and that higher-value or more complex requests may require larger bonds or longer challenge windows. <citation sourcetype="external" sourceid="UMA bond and liveness docs" label="UMA bond and liveness docs" url="https://docs.uma.xyz/developers/setting-custom-bond-and-liveness-parameters" textbefore="UMA’s bond and liveness guidance notes that bonds create incentives for disputers, and that higher-value or more complex requests may require larger bonds or longer challenge windows."></citation>

HAOO inherits the same issue. If challengers are underpaid, bad assertions pass. If challengers are over-incentivized, valid work gets griefed.

### Assumption 5: Reputation weighting improves judgment more than it creates cartel risk

The proposal uses conviction-weighted or reputation-weighted participation in the challenge process. <citation sourcetype="external" sourceid="Hybrid Agentic-Optimistic Oracle proposal" label="Hybrid Agentic-Optimistic Oracle proposal" url="https://github.com/vishal10menon/conviction-hybrid-oracle-proposal" textbefore="The proposal uses conviction-weighted or reputation-weighted participation in the challenge process."></citation>

This can reduce spam and Sybil attacks, but it introduces a different risk: insiders may accumulate enough reputation to dominate disputes.

Reputation is useful only if it can decay, be slashed, diversify over time, and remain contestable.

### Assumption 6: The liveness window can balance speed and security

A short liveness window improves builder experience but weakens review. A long liveness window improves review but delays payment.

UMA describes liveness as a challenge period and notes that it can be adjusted based on security and user-experience tradeoffs. <citation sourcetype="external" sourceid="UMA bond and liveness docs" label="UMA bond and liveness docs" url="https://docs.uma.xyz/developers/setting-custom-bond-and-liveness-parameters" textbefore="UMA describes liveness as a challenge period and notes that it can be adjusted based on security and user-experience tradeoffs."></citation>

HAOO needs the same parameter discipline. A single fixed window is unlikely to work across all task types.

### Assumption 7: Market price should monitor confidence, not adjudicate semantic truth

Decision markets are useful because they put capital behind beliefs. MetaDAO’s docs describe decision markets as a system where proposals pass or fail based on whether traders expect token value to increase or decrease. <citation sourcetype="external" sourceid="MetaDAO docs" label="MetaDAO docs" url="https://docs.metadao.fi/governance/overview" textbefore="Decision markets are useful because they put capital behind beliefs. MetaDAO’s docs describe decision markets as a system where proposals pass or fail based on whether traders expect token value to increase or decrease."></citation>

But a milestone-verification system asks a different question: did a particular artifact satisfy a particular specification?

The design assumption is that markets should provide economic context and monitoring, while semantic verification should evaluate the artifact itself.

## 4. Failure-mode table

| Failure mode | What happens | Why it matters | Possible mitigation |
|---|---|---|---|
| Agent false positive | Bad work passes verification | Capital is released incorrectly | Better manifests, challenger rewards, multiple verifiers, stronger evidence schemas |
| Agent false negative | Good work is rejected | Builders lose trust in the market | Appeal path, human escalation, verifier slashing, manifest revision |
| Ambiguous manifest | The success criteria are vague | Disputes become political rather than evidentiary | Require structured evidence schemas and pre-registered verification logic |
| Frivolous challenge | A bad actor disputes valid work to delay payout | The market becomes slow and hostile to builders | Challenge bonds, challenger reputation loss, escalating costs for repeated bad challenges |
| Challenger apathy | Nobody disputes bad assertions | Optimistic finality becomes rubber-stamping | Challenge bounties, monitoring markets, delegated watchdogs |
| Reputation cartel | High-reputation actors coordinate | The dispute layer becomes captured | Reputation decay, caps, diversity constraints, appeal to broader juror set |
| Verifier capture | The verifier agent or provider becomes biased | The system hides centralization behind automation | Rotating verifiers, open verifier markets, audit logs, model diversity |
| Correlated verifier error | Multiple verifiers fail the same way | Redundancy creates false confidence | Use heterogeneous models, human spot checks, adversarial test sets |
| Liquidity shock | Market price collapses during verification | Valid work is socially punished by unrelated price movement | Keep price as monitor, not final judge |
| Evidence spoofing | Builder submits forged or misleading proof | The agent verifies the wrong reality | Cryptographic attestations, signed commits, on-chain proofs, provenance checks |
| Dispute latency | Resolution takes too long | Builders discount the value of future payouts | Task-tiered windows, fast paths for low-value claims, stronger upfront manifests |
| Governance capture | Rule changes are controlled by insiders | The mechanism becomes adaptive in favor of incumbents | Public parameter governance, delay periods, emergency exits |
| Manifest gaming | Builders optimize for the manifest rather than useful work | The system rewards checklist completion over outcomes | Mix objective criteria with sponsor review, post-hoc audits, outcome-linked tranches |
| Semantic overreach | The verifier judges work it cannot reliably understand | False precision becomes dangerous | Restrict agent verification to well-scoped claim types |

## 5. Adversarial test cases

### Scenario 1: The polished fake builder

A builder submits an artifact that looks complete, has clean documentation, and satisfies superficial checks. The verifier approves it. Later, users discover that the artifact fails under real conditions.

Question: what catches the gap between apparent completion and functional completion?

Possible mitigations:

- Require executable tests.
- Require reproducible benchmarks.
- Require signed deployment proofs.
- Require post-deployment monitoring before full payout.
- Split payment into staged tranches.

### Scenario 2: The griefing challenger

A challenger disputes every valid milestone. The challenger does not expect to win. The goal is to delay payments and make the market unusable.

Question: how expensive must griefing become before it stops?

Possible mitigations:

- Challenge bonds.
- Reputation penalties for failed challenges.
- Higher bonds for repeat challengers.
- Fast dismissal for challenges without evidence.
- Compensation to builders for malicious delay.

### Scenario 3: The reputation cartel

A group of high-reputation actors coordinates to control dispute outcomes. They do not need to attack the verifier directly. They only need to dominate the escalation layer.

Question: when does reputation-weighting stop being anti-Sybil protection and start becoming oligarchy?

Possible mitigations:

- Reputation decay.
- Domain-specific reputation rather than universal reputation.
- Caps on voting power.
- Randomized juror selection.
- Appeal to a broader or more expensive court.
- Minority reports attached to rulings.

### Scenario 4: The ambiguous manifest

A builder delivers work that is useful but not exactly what the manifest specified. The verifier rejects it. The builder argues that the outcome was achieved. The sponsor argues that the specification was not met.

Question: should the system reward literal compliance or useful completion?

Possible mitigations:

- Require manifest review before work begins.
- Allow sponsor-approved amendments before submission.
- Separate “spec satisfied” from “outcome valuable.”
- Use different payout paths for objective and discretionary milestones.

### Scenario 5: The thin-market attack

A whale pushes the market price against the builder during the verification period. The work is valid, but the market signal creates social pressure to reject or challenge the payout.

Question: can the system prevent price from becoming a reflexive veto?

Possible mitigations:

- Do not use spot price as the primary verifier.
- Use price only as a trigger for review.
- Use TWAP-style smoothing if price enters the process.
- Require semantic evidence to override price noise.

MetaDAO’s docs explicitly use TWAP-based finalization to reduce manipulation risk from end-of-period prices. <citation sourcetype="external" sourceid="MetaDAO TWAP docs" label="MetaDAO TWAP docs" url="https://docs.metadao.fi/governance/twaps" textbefore="MetaDAO’s docs explicitly use TWAP-based finalization to reduce manipulation risk from end-of-period prices."></citation>

### Scenario 6: The lazy verifier

The verifier agent returns plausible reasoning but does not actually inspect the relevant artifact deeply. The reasoning trace appears coherent, but the decision is shallow.

Question: how can the protocol distinguish explanation quality from verification quality?

Possible mitigations:

- Require deterministic checks where possible.
- Require evidence references in the verifier trace.
- Use adversarial prompts and hidden tests.
- Sample decisions for human audit.
- Slash verifier reputation for missed obvious failures.

### Scenario 7: The passive sponsor

The sponsor funds a market but does not monitor claims. Builders and challengers become the only active participants. The system technically works, but nobody with domain context is accountable.

Question: should sponsors have explicit monitoring duties?

Possible mitigations:

- Sponsor-staked review commitments.
- Delegated reviewers.
- Sponsor silence as acceptance after liveness.
- Sponsor challenge rights with higher reputation weight but higher slashing risk.

## 6. Toy incentive model

This is not a full mechanism model. It is a minimal way to reason about the challenger’s decision.

Let:

- $$R$$ = reward released to the builder.
- $$B$$ = challenger bond.
- $$C$$ = cost of evaluating and submitting a challenge.
- $$p$$ = challenger’s estimated probability that the challenge succeeds.
- $$G$$ = challenger reward if successful.
- $$S_c$$ = challenger penalty if unsuccessful.
- $$D$$ = system-level cost of payout delay.
- $$q$$ = verifier accuracy.
- $$L$$ = liveness-window duration.
- $$k$$ = number of independent challengers.

A rational challenger disputes when expected private payoff is positive:

$$
pG - (1 - p)S_c - C > 0
$$

A protocol wants challenges only when expected social value exceeds expected delay cost:

$$
pR > D
$$

Those two inequalities are not automatically aligned.

A challenge may be privately profitable but socially wasteful. A challenge may also be socially valuable but privately unattractive.

This creates the core parameter problem.

### Bond too low

If $$B$$ and $$S_c$$ are too low, frivolous challenges become cheap. Builders face delay risk even when their work is valid.

### Bond too high

If $$B$$ and $$S_c$$ are too high, legitimate challengers may not dispute bad assertions. The optimistic window becomes theater.

### Reward too low

If $$G$$ is too low, no one monitors. This is especially dangerous for low-attention, long-tail markets.

### Reward too high

If $$G$$ is too high, participants may over-monitor or manufacture disputes.

### Liveness too short

If $$L$$ is too short, complex claims cannot be reviewed.

### Liveness too long

If $$L$$ is too long, builder payouts become slow and unattractive.

### Verifier accuracy threshold

If verifier accuracy $$q$$ is high, the challenge system mostly catches edge cases. If $$q$$ is low, the challenge system becomes the real oracle, and the verifier agent adds little value.

A basic design goal is:

$$
q \text{ high enough that challenges are rare, but not so trusted that challenges become irrelevant.}
$$

## 7. Simulation plan for v2

A useful v2 should simulate the failure modes rather than only describe them.

### Variables to simulate

- $$R$$: builder reward
- $$B$$: challenge bond
- $$C$$: cost of challenge
- $$G$$: challenger reward
- $$S_c$$: challenger penalty
- $$D$$: delay cost
- $$q$$: verifier accuracy
- $$L$$: liveness duration
- $$k$$: number of potential challengers
- $$h$$: share of honest challengers
- $$m$$: share of malicious challengers
- $$\rho$$: reputation concentration
- $$\alpha$$: probability of cartel coordination
- $$\epsilon$$: manifest ambiguity rate

### Questions to test

1. At what bond level do frivolous challenges disappear?
2. At what bond level do legitimate challenges also disappear?
3. How accurate must the verifier be before the system becomes usable?
4. How many independent challengers are needed to catch bad approvals?
5. How concentrated can reputation become before cartel risk dominates?
6. How long can the liveness window be before builders discount the payout too heavily?
7. How sensitive is the system to ambiguous manifests?
8. How often does the market price create false social pressure against valid payouts?
9. Does adding more verifier agents improve accuracy, or do correlated errors dominate?
10. When should a task be rejected as unsuitable for agentic verification?

### Minimal simulation outline

Start with three builder types:

- Honest builder
- Low-quality builder
- Adversarial builder

Use three challenger types:

- Honest challenger
- Lazy challenger
- Griefing challenger

Use three verifier states:

- Correct
- False positive
- False negative

Then run repeated trials under different parameter settings:

1. Builder submits claim.
2. Verifier produces assertion.
3. Challengers decide whether to dispute.
4. Dispute layer resolves.
5. Payoff is distributed.
6. Reputation updates.

The objective is not to prove the design. The objective is to find where it breaks.

## 8. Comparison with existing oracle and governance models

| Model | Speed | Semantic accuracy | Decentralization | Manipulation resistance | Main weakness |
|---|---:|---:|---:|---:|---|
| Pure futarchy or decision markets | High | Low to medium | Medium | Depends on liquidity | Market price may not answer semantic work-completion questions |
| UMA-style optimistic oracle | Medium to high | Medium | Medium | Stronger when bonds and liveness are well-set | Requires active disputers and clear resolution criteria |
| Kleros-style social court | Medium to low | Medium to high for subjective disputes | Medium to high | Depends on juror incentives and court design | Slower and more expensive for frequent machine-speed claims |
| Pure AI oracle | High | Medium | Low | Weak if no dispute layer exists | Hidden centralization and model error |
| HAOO | Medium to high | Potentially high for well-scoped tasks | Medium | Depends on challenge incentives and verifier auditability | Complexity and parameter sensitivity |

This table is intentionally conservative.

HAOO is not automatically better. It is only better if the task is semantically structured, the verifier trace is auditable, challengers are incentivized, and dispute resolution is not captured.

## 9. What would falsify this design?

The design should be treated as falsifiable. It fails if any of the following conditions hold.

### 1. Most useful work cannot be written into semantic manifests

If milestones cannot be specified clearly enough, the verifier agent becomes an aesthetic judge rather than an oracle.

### 2. Verifier-agent errors are too correlated

If multiple agents fail in the same way, redundancy does not provide real security.

### 3. Challengers are too passive

If no one monitors long-tail markets, optimistic finality becomes automatic approval.

### 4. Challenge costs exceed expected rewards

If the economics do not reward review, the system depends on altruism. That is not a durable security model.

### 5. Reputation weighting creates cartel behavior

If high-reputation actors can coordinate dispute outcomes, the system becomes less decentralized over time.

### 6. Dispute latency makes builders leave

If builders cannot tolerate the delay between submission and payout, the system may be correct but unusable.

### 7. Manifest gaming dominates real value creation

If builders learn to satisfy the manifest while avoiding useful work, the protocol rewards compliance theater.

### 8. Price reflexivity re-enters through social pressure

If market price is officially only a monitor but socially becomes the real judge, the design has not solved the original problem.

### 9. The verifier cannot produce useful audit traces

If the reasoning trace is not specific enough for challengers to inspect, the agent becomes an opaque authority.

### 10. The system is too complex for users to reason about

A mechanism that is theoretically sound but practically illegible will fail in production.

## 10. Design principles

The following principles should guide future iterations.

### Principle 1: Markets should price uncertainty, not adjudicate semantic truth

A price can say what people expect. It cannot always say whether a milestone was actually completed.

### Principle 2: AI should compress verification work, not become final authority

The verifier agent should reduce the cost of first-pass assessment. It should not remove the need for challenge, audit, and escalation.

### Principle 3: Curation quality determines oracle quality

A verifier is only as good as the manifest it interprets. Poorly curated tasks will produce poor verification.

### Principle 4: Optimistic systems fail when no one is paid to challenge

A liveness window is only meaningful if someone has the incentive, ability, and time to dispute bad assertions.

### Principle 5: Reputation must be losable

Reputation that only accumulates becomes power. Reputation that can decay, fragment by domain, and be slashed can become security.

### Principle 6: The system must be designed around the verifier being wrong

The question is not whether the verifier will fail. It will. The question is whether the protocol fails safely.

### Principle 7: Not every task should be agent-verified

Some work may be too ambiguous, too subjective, or too context-dependent for this architecture.

## 11. Open implementation questions

### 1. What is the minimum viable semantic manifest?

A useful manifest may need:

- Task description
- Success criteria
- Required artifacts
- Required evidence
- Verification logic
- Exclusion criteria
- Accepted ambiguity range
- Appeal path

### 2. Should verifiers be general or domain-specific?

A general verifier is easier to deploy but weaker on domain nuance. A domain-specific verifier is more accurate but harder to maintain.

### 3. Should there be one verifier or a verifier market?

A single verifier is simpler but creates centralization risk. A verifier market is more robust but increases complexity.

### 4. How should reputation be scoped?

Universal reputation is powerful but dangerous. Domain-specific reputation may be safer.

### 5. Should price ever influence verification?

The safest answer may be: price can trigger review, but should not determine semantic success.

### 6. What tasks are unsuitable?

The protocol should reject certain tasks upfront if they cannot be verified within the system’s assumptions.

Examples:

- Vague brand-building tasks
- Open-ended strategic advisory
- Subjective design quality
- Community sentiment improvement
- Unbounded research claims

## 12. Suggested next artifact

The next artifact should not be another essay. It should be a small simulation or prototype.

A useful v2 package would include:

1. A sample semantic manifest for a GitHub-based milestone.
2. A verifier-agent prompt or deterministic verification script.
3. A synthetic set of valid and invalid submissions.
4. A simple challenge-game simulation.
5. A parameter table showing where the system fails.

The goal is not to make HAOO look inevitable. The goal is to make it testable.

## 13. Feedback requested

I am especially interested in critique on five questions:

1. Which failure mode is most fatal?
2. Is reputation-weighted dispute resolution salvageable, or does it create cartel risk?
3. Should verifier agents be singular, plural, or market-selected?
4. What should be simulated first?
5. What would make this useful enough for a protocol team to test?

## 14. References

- Vishal Menon, “Hybrid Agentic-Optimistic Oracle for Conviction Markets: Resolving Reflexivity in Long-Tail Coordination”  
  https://github.com/vishal10menon/conviction-hybrid-oracle-proposal

- Conviction Markets, official site  
  https://www.convictionmarkets.io/

- Conviction Markets, Request for Builders  
  https://www.convictionmarkets.io/submit

- Robin Hanson, “Futarchy: Vote Values, But Bet Beliefs”  
  http://hanson.gmu.edu/futarchy.html

- MetaDAO, “Introduction to Decision Markets”  
  https://docs.metadao.fi/governance/overview

- MetaDAO, “Finalizing Proposals”  
  https://docs.metadao.fi/governance/twaps

- UMA, “How does UMA’s Oracle work?”  
  https://docs.uma.xyz/protocol-overview/how-does-umas-oracle-work

- UMA, “Setting Custom Bond and Liveness Parameters”  
  https://docs.uma.xyz/developers/setting-custom-bond-and-liveness-parameters

- Kleros, introduction docs  
  https://docs.kleros.io/

- Kleros, dispute resolution integration plan  
  https://docs.kleros.io/integrations/types-of-integrations/1.-dispute-resolution-integration-plan
