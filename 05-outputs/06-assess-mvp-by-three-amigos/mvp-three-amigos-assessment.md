# Three Amigos Assessment: MVP Brief

## Executive Summary

The brief makes a credible case for an underserved market position, but it describes a product vision rather than an MVP specification. The three-gap framing (persistent memory, proactive action, integrated reasoning) is well-evidenced from 53 interviews and no current competitor occupies this intersection. The panel's verdict: the core loop is desirable and conditionally buildable, but three structural omissions must be resolved before the experiments can generate trustworthy signals.

**Top 3 strengths:**
- Problem statement is participant-grounded, with the three core frustrations (no memory, no proactivity, confident errors) supported by direct interview evidence
- Experiment design is disciplined — quantified success/failure thresholds and a technical spike before feature investment show founders who understand learning velocity
- Human-approval gate addresses the non-negotiable trust condition named by Participants 3, 46, and 35, and is architecturally simple to implement

**Top 3 concerns:**
- No unit economics: per-user inference cost for the persistent memory and daily briefing pipeline could reach $0.50–$2.00/day, making the $17/month price point margin-negative for heavy users
- No acquisition strategy beneath the subscriber projections: 10k/50k/100k revenue tables are spreadsheet fiction without a channel hypothesis
- Memory retrieval quality is simultaneously the product's primary differentiator and its highest-risk failure mode — a false memory recall moment is worse than no memory at all, yet the brief treats mitigation as optional infrastructure

**Highest-priority action:** Add a unit economics model and a source-attribution requirement for memory-sourced outputs before committing to the Experiment 1 build.

---

## Desirability Assessment

**Strengths:**
- **Problem statement is evidence-grounded, not invented.** The three core frustrations — AI that does not remember, does not act proactively, and presents errors confidently — are directly supported by Participants 6, 8, 37, and 50. The brief earns its problem framing.
- **Target user selection is empirically justified.** Maya Patel maps to 13 of 53 participants, the largest archetype cluster, with concrete daily coordination pain and enough tolerance for new tooling that signal will be unambiguous.
- **Daily briefing answers participant language verbatim.** Participant 28 described wanting "is there something that I said I would do that I haven't yet achieved?" — the briefing directly addresses this. The match between stated desire and proposed feature is unusually clean.
- **Human-approval gate is correctly non-negotiable.** Multiple participants named approval as a condition of trust, not a preference. The brief's treatment of this as an architectural constraint rather than a UX option is correct.
- **Out-of-scope decisions are explicit and rationale-backed.** Deferred features are named with reasons, signalling disciplined prioritisation rather than oversight.

**Gaps and Concerns:**
- **The MVP is a work coordination tool; the strategic brief asked for a personal assistant.** The research spans health, creative projects, learning, and financial planning. Scoping entirely to email and calendar for a professional user risks delivering productivity SaaS while the VC narrative promises a personal AI revolution.
- **Confidence signalling is deferred despite trust being the stated differentiator.** Hallucination-as-confident is a named primary pain point. Retrieval provenance ("Based on your email from March 1") is not a full confidence system — it is a UI label — and it should be in v1 scope.
- **The memory recall moment has no design specification.** This is the highest-stakes UX moment in the product. How memory surfaces determines whether it reads as a feature or surveillance. Tone, timing, and opt-out design are absent from the brief.
- **No expansion narrative for 40 of 53 participants.** The single-archetype focus is sound for validation clarity, but the brief must state which v1 architectural choices are archetype-neutral and which are archetype-specific.
- **Emotional and relational dimensions are silently dropped.** The strategic brief lists personality, interaction style, and loss of human connection as explicit research dimensions. Dropping them without acknowledgment is a gap, not a decision.

**Key recommendation:** Require a daily briefing design specification — covering tone, layout, memory display, and zero-commitment state — before Experiment 1 build begins. This is the single surface where all trust dimensions and the core value proposition converge.

---

## Feasibility Assessment

**Strengths:**
- **Narrow integration surface at launch is the right engineering call.** Gmail and Google Calendar only avoids multi-provider OAuth complexity. Deferring Outlook and Apple Mail is explicitly justified and correct.
- **Human-in-the-loop gate is architecturally low-risk.** The confirmation step before any write operation is a well-understood pattern with high trust payoff and low implementation complexity.
- **Experiment 2 isolates the hardest technical question early.** The approval-gated calendar reschedule spike tests the riskiest integration path before full product investment. If it fails, the team knows before building on a broken foundation.
- **Commitment extraction from email and calendar is tractable.** NLP action-item extraction using current LLM capabilities is solved enough for an MVP accuracy floor.
- **The "why now" answer exists.** The cost-performance curve of LLMs crossed a viability threshold in 2024-2025. Per-user daily inference cost fell from $5–$15 to $0.50–$2.00. The brief should state this explicitly as its market timing argument.

**Gaps and Concerns:**
- **Memory retrieval false matches are the highest-risk failure mode and the brief names but does not mitigate them.** Semantic search returning plausible-but-wrong context is not an edge case — it is the default behaviour of embedding-based retrieval at scale. A stale memory driving a proactive action destroys trust at the exact moment the feature is supposed to build it. A memory decay or recency-weighting strategy must be specified.
- **No storage architecture is stated.** Vector database, knowledge graph, or raw conversation logs have fundamentally different cost, latency, and accuracy profiles. The brief treats memory as a feature without specifying the technical approach — engineering cannot estimate cost or timeline without this.
- **Proactive commitment surfacing requires background infrastructure that is not acknowledged.** The assistant must run background processes checking email and calendar on a cadence. This is not a stateless LLM interaction — it requires persistent infrastructure (cron jobs, message queues, push notifications) that is absent from the brief.
- **The 8-second Experiment 2 target bundles incompatible metrics.** System latency and user decision time are different problems. A cold OAuth token refresh alone can take 2–3 seconds. The experiment should split into two targets: system round-trip under 5 seconds, user approval decision under 3 seconds.
- **No per-user LLM cost model.** A daily briefing reading 20–50 emails could consume 30,000–80,000 tokens per user per day. At current Sonnet-class pricing, that is $0.50–$2.00/user/day — potentially $15–$60/month in inference cost alone. At $17/month, margins are negative for heavy users without a tiered model strategy.

**Key recommendation:** Mandate a one-page technical architecture appendix covering: (1) memory storage and retrieval approach with a decay/invalidation strategy, (2) background processing architecture for proactive surfacing, and (3) per-user LLM cost estimate by model tier. Without these, the revenue model is unvalidatable.

---

## Viability Assessment

**Strengths:**
- **Competitive gap identification is the brief's strongest asset.** The three-gap framework is evidenced from 53 interviews and maps cleanly against a competitor table where no product occupies the full intersection. This is the kind of insight that secures a first VC meeting.
- **Pricing logic is disciplined.** $17/month undercuts ChatGPT Plus marginally to reduce switching friction while sitting above pure productivity tools. The brief ties pricing to willingness-to-pay signals from research rather than guessing.
- **Experiment-driven validation shows learning velocity.** Quantified success and failure thresholds for three experiments demonstrate founders who understand de-risking before scaling. VCs fund this approach.
- **Scope constraints are smart.** Excluding autonomous action, team features, and multi-platform integrations shows restraint and keeps the validation signal clean.

**Gaps and Concerns:**
- **No go-to-market strategy.** Revenue milestones (10k/50k/100k subscribers) have no acquisition path beneath them. At minimum, the brief must state the recruitment channel for the 20-user Experiment 1 cohort — the channel shapes the signal.
- **The moat is thinner than stated.** Persistent memory, proactive action, and calendar integration are features that Google (Gemini + Workspace), Apple (Siri + native OS), and OpenAI (ChatGPT memory) could replicate with existing distribution. The brief does not address the incumbent response scenario.
- **Unit economics are absent.** No inference cost per user, no OAuth maintenance overhead, no support burden estimate. A Series A investor will ask "what's your gross margin at 10k users?" and the brief has no answer.
- **Single-archetype risk understates the TAM problem.** Workflow Optimisers on Google Workspace is a fraction of the $47–50B headline market figure. Either an expansion narrative exists and must be stated, or the market sizing must be revised downward to reflect what the launch product actually addresses.
- **Market timing argument is missing.** The brief cites 17–19% CAGR but does not explain why this opportunity is available in 2026 and not earlier or later. The LLM cost curve answer exists — it should be included.

**Key recommendation:** Add three items in priority order: (1) an honest addressable market size for the launch configuration (Workflow Optimisers on Google Workspace), (2) a unit economics model showing at what retention level the data gravity effect produces positive LTV despite inference costs, and (3) a two-sentence market timing argument grounded in the LLM cost curve.

---

## Cross-Cutting Tensions

**Memory quality as both differentiator and liability:** The UX Researcher, Engineer, and PM all identify persistent memory as the product's core asset — but for different reasons that create conflicting v1 requirements. The Engineer wants a memory architecture spec to cost the feature. The UX Researcher wants interaction design to prevent memory from reading as surveillance. The PM wants the data gravity argument to anchor the moat narrative. These cannot all be satisfied by a single bullet point in the Risks section. Memory requires specification at all three levels simultaneously.

**Confidence signalling: deferred vs. minimum viable trust:** The brief defers confidence signalling as scope risk. The UX Researcher and PM both reversed position during discussion, arguing that source attribution on memory outputs ("from your email on Tuesday") is not a confidence system — it is the minimum viable mechanism for distinguishing a correct memory recall from a hallucination. The Engineer agrees this belongs in the approval gate as a v1 requirement. The tension is whether this qualifies as a "confidence signal" (deferred) or "approval gate component" (in scope). The panel's resolution: retrieval provenance is in scope for v1; broader confidence calibration is deferred.

**Strategic brief scope vs. MVP focus:** The UX Researcher argues the MVP delivers a work coordination tool while the VC narrative promises a personal AI assistant — and that architectural choices in v1 (email and calendar as sole context sources, commitment-tracking as the memory schema) may foreclose broader personal use cases without the team realising it. The PM argues this is a market sizing problem, not a vision alignment problem, and the brief needs an honest TAM figure for the launch configuration rather than a scope expansion. These frame the same risk differently: the UX Researcher sees architecture lock-in; the PM sees investor credibility risk. Both are real.

**The 8-second benchmark: engineering metric vs. UX threshold:** The Engineer reads the 8-second target as an ambiguous system metric that bundles incompatible subsystems. The UX Researcher reads it as a desirability threshold — the approval gate must feel faster than manual task completion, or users will abandon it regardless of backend speed. The PM sides with benchmarking against the manual alternative rather than an absolute time threshold. Resolution: split Experiment 2 into system latency and user decision time, and add a comparative friction benchmark against the manual alternative.

**Product vision vs. business specification:** All three reviewers converged on the same meta-critique: the brief is strong on what to build and why, but silent on how the business works. The UX Researcher identifies trust mechanics as underspecified. The Engineer identifies infrastructure costs as unacknowledged. The PM identifies acquisition and unit economics as absent. The brief presents a product vision; it needs to become an MVP specification with cost modelling, acquisition strategy, and an honest addressable market statement.

---

## Consensus Recommendations

1. **Mandate a technical architecture appendix:** Specify the memory storage and retrieval approach (with decay/invalidation strategy), background processing infrastructure for proactive surfacing, and a per-user LLM cost model by tier. All three lenses require this to validate the core product loop and the revenue model.

2. **Promote retrieval provenance to v1 scope:** Include source attribution (email subject, date, calendar event) in the approval gate as a core v1 requirement. This is the minimum viable mechanism for competence trust and distinguishes a correct memory recall from a hallucination — supported by the UX Researcher, Engineer, and PM.

3. **Require a daily briefing design specification before build:** The daily briefing is the surface where memory, proactive action, and trust converge — described as "the real MVP" by all three reviewers. It must be fully specified (tone, layout, memory display, zero-commitment state) before Experiment 1 build begins.

4. **Add unit economics and an honest addressable market statement:** Model per-user inference cost against the $17/month price point and state the actual addressable market for Workflow Optimisers on Google Workspace at launch. Revenue projections without cost structure and a sized market are not investable.

5. **Sketch a two-archetype expansion path and a market timing argument:** Identify the next archetype, state which v1 architectural choices enable or constrain expansion, and add two sentences on the LLM cost curve as the "why now" answer. Both address Series A credibility gaps that the current brief leaves open.

---

*March 2026 · MVP Brief reviewed by Three Amigos panel*
