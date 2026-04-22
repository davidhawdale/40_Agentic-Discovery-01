# Discussion Transcript

*Three Amigos panel — March 2026*
*Participants: UX Researcher (Desirability), Engineer (Feasibility), Product Manager (Viability)*

## Phase 1 Review Summaries

### Desirability Review
Strong desirability case anchored in real participant pain with the three-gap framing (memory, proactivity, trust) directly evidenced. Key concerns: the MVP narrows to a work coordination tool rather than the personal assistant the strategic brief envisions, confidence signalling is deferred despite trust being the core differentiator, and the memory recall moment has no design detail.

### Feasibility Review
The core loop (read email/calendar, extract commitments, surface briefing, gate actions) is buildable with current technology — conditionally feasible. Three architectural blind spots must be addressed: memory retrieval quality (false matches will destroy trust), background processing infrastructure for proactive surfacing, and per-user LLM cost at the $17/month price point.

### Viability Review
Credible MVP thesis with a real market gap, but significant business plan holes. The moat is thinner than acknowledged (features, not structural advantages), there is no go-to-market strategy beneath the subscriber projections, unit economics are absent, and the market timing argument is missing.

---

## Round 1

**[UX Researcher]**

### Agreements

**With Engineer on memory retrieval as highest-risk failure mode.** This is exactly right from a desirability standpoint too. The "memory recall moment" is positioned as the primary willingness-to-pay driver in Experiment 3, but a false memory recall moment — the assistant confidently surfacing a stale or wrong commitment — is actively worse than no memory at all. It does not just fail to delight; it triggers the exact "confident and convincing way, even when it's completely wrong" frustration that Participants 6 and 8 already named as their core complaint about current tools. The brief acknowledges this in the Risks section but treats it as a technical concern. It is first and foremost a desirability concern: the feature most likely to create the "magic moment" is the same feature most likely to destroy trust on first contact. Memory decay and invalidation strategy is not optional infrastructure — it is a UX-critical design requirement.

**With PM on single-persona risk.** The brief builds a tight case for Maya Patel, but the strategic brief asks for a "personal assistant" across planning, health, learning, creativity, relationships, and financial decisions. Thirteen of 53 participants is a legitimate starting point. But the brief never articulates a credible expansion path from "workflow coordination tool for operations leads" to "personal AI assistant people choose to use daily." If the product validates with Maya and then discovers that the persistent-memory architecture only serves professional task management, the pivot to broader personal use cases is a rebuild, not an extension.

**With PM on absent go-to-market.** The revenue projections (10k/50k/100k subscribers) have no acquisition strategy beneath them. From a desirability perspective, you cannot validate willingness-to-pay if you cannot reach the people willing to pay. The brief should specify at minimum a recruitment channel hypothesis for the 20-user Experiment 1 cohort — are these sourced from productivity communities, existing AI tool subscribers, or cold outreach? The channel shapes the signal.

### Disagreements or Tensions

**With Engineer on the 8-second round-trip target.** The Engineer is right that the metric bundles too many subsystems. But I want to push back on the framing: the 8-second target is not primarily an engineering benchmark — it is a desirability threshold. If the approval-gated reschedule takes longer than completing the task manually, users will abandon it not because the system is slow but because it fails to feel like help. The correct approach is to decompose the 8 seconds into the user-facing interaction time (tap-to-confirm should feel instant, under 1 second) and the backend processing time (which can be longer if the UI provides progressive feedback). The brief conflates system latency with perceived latency, and those are different design problems.

**With PM on moat as "features not structural advantages."** I partially disagree. Persistent memory that accumulates over months creates a switching cost that is structural, not feature-level. The longer a user stays, the more the assistant knows, and the harder it is to replicate that knowledge elsewhere. Google or Apple could ship memory as a feature, but they cannot ship six months of a specific user's accumulated context. The moat is not the capability — it is the data gravity. However, the brief fails to make this argument explicitly, which means the PM's critique is fair against what the brief actually says.

**On confidence signalling being out of scope.** My independent review flagged this and I want to reinforce it against the Engineer's concern about memory false matches. The brief defers confidence signalling to avoid scope risk, but retrieval provenance — showing the user where a memory came from ("from your email on Tuesday" vs. "from your conversation last month") — is the minimum viable trust mechanism. Without it, users cannot distinguish a correct memory recall from a hallucination. This is not the same as building a full confidence scoring system. It is a UI label on memory-sourced outputs, and it should be in scope for v1.

### Cross-Cutting Insights

**The trust paradox is underspecified across all three reviews.** The MVP's core loop requires users to (1) grant OAuth access to email and calendar, (2) trust the assistant's memory of their commitments, and (3) approve actions the assistant proposes. Each step demands a different kind of trust: data trust (will you keep my data safe?), competence trust (are you remembering correctly?), and agency trust (will you do what I approved and nothing else?). The brief treats trust as a single dimension and designs a single mechanism (human-approval gate) to address all three. The approval gate addresses agency trust. It does nothing for data trust or competence trust. The experiments should be designed to measure all three trust dimensions independently — otherwise a "trust" failure in the pilot will be undiagnosable.

**Emotional and relational dimensions remain absent.** The strategic brief explicitly lists "relationship and social planning," "personality and interaction style that feels right," and "loss of human connection" as research dimensions. The MVP brief addresses none of these. This is a deliberate scope decision and may be correct for v1 — but it should be acknowledged as a known gap rather than silently dropped. Forty of 53 participants are outside the Workflow Optimiser archetype, and some of their needs are relational, not transactional.

**The daily briefing is the real MVP, and it is underdesigned.** All three reviews circle around memory, proactive action, and trust — but the daily briefing is the concrete surface where all three converge. It is the moment the user sees what the assistant remembers, what it proactively surfaces, and whether it earns enough trust to act on. Yet the brief describes it in one sentence. What does it look like? What tone does it use? How does it handle a day with no overdue commitments? The daily briefing UX is the single highest-leverage design decision in the MVP, and it needs its own design specification — not a bullet point.

### Refined Recommendations

1. **Elevate memory provenance to v1 scope.** Not full confidence scoring — just source attribution on memory-sourced outputs ("Based on your email from March 1"). This is the minimum viable trust signal.
2. **Decompose trust into three testable dimensions.** Redesign Experiment 1 and Experiment 3 to separately measure data trust, competence trust, and agency trust.
3. **Require a daily briefing design specification before build.**
4. **Add a one-paragraph expansion narrative** stating how the product moves from Maya Patel to the next two archetypes.
5. **Specify the Experiment 1 recruitment channel.**

---

**[Engineer]**

### Agreements

**With UX Researcher — "memory recall moment" needs design detail.** From an engineering perspective, this concern maps directly onto my Phase 1 finding about memory retrieval false matches. The UX question ("does memory read as feature or surveillance?") and the engineering question ("how do we avoid stale or wrong memory surfacing?") are the same problem viewed from different sides. A memory recall moment that surfaces the wrong commitment is not just a bad UX — it is the single fastest way to lose the user permanently. The brief needs to specify both the retrieval architecture and the interaction design for memory surfacing as a single integrated spec, not as separate concerns.

**With PM — unit economics are unresolved and must be resolved pre-build.** I want to make this more concrete: a daily briefing that reads 20-50 emails, maintains a commitment list, and generates personalised output could consume 30,000-80,000 tokens per user per day depending on email volume and model tier. At current API pricing (Sonnet-class for reasoning, Haiku-class for extraction), that is roughly $0.50-$2.00 per user per day — potentially $15-$60 per user per month in inference cost alone. At $17/month, the margin is negative for heavy users unless the model tier strategy is carefully designed. This is not a "nice to have" appendix item — it is a viability gate.

**With PM — moat is thinner than the brief acknowledges.** From an engineering standpoint, the defensibility comes from the accumulated memory graph per user, not the product architecture. This is a data network effect, not a technology moat.

### Disagreements or Tensions

**With UX Researcher — confidence signalling should not be deferred.** I partially disagree with the framing but agree with the conclusion. Retrieval provenance — showing the user where a memory or commitment came from — is not a "confidence signal" feature; it is a necessary component of the approval gate. When the assistant says "you committed to sending the Q3 report to Sarah by Friday," the user needs to see that this was extracted from a specific email on a specific date. Without provenance, the approval gate becomes a trust-me button, and participants explicitly rejected that pattern. Recommendation: include source attribution (email subject, date, calendar event) in the approval step as a core v1 requirement, but defer the broader confidence-calibration system.

**With UX Researcher — single-archetype focus is correct for engineering.** From a feasibility standpoint, the single-archetype focus is exactly right: it constrains the integration surface (email + calendar only), narrows the commitment extraction problem, and makes experiment success criteria unambiguous. The expansion path is a product strategy question, not a technical architecture question.

**With PM — "why now" has an engineering answer.** The answer is clear: the cost-performance curve of LLMs crossed a threshold in 2024-2025 that makes per-user persistent reasoning economically viable for the first time. Two years ago, the inference cost for a daily briefing pipeline would have been $5-$15 per user per day. Today it is $0.50-$2.00. The brief should state this explicitly.

### Cross-Cutting Insights

**All three reviews converge on the same meta-problem: the brief describes what the product does but not how it works.** The UX Researcher wants design detail for memory surfacing. The PM wants unit economics and go-to-market. I want storage architecture, background processing, and cost modelling. These are not three separate gaps — they are one gap: the brief is a product vision document masquerading as an MVP specification.

**The 8-second metric is a proxy for a deeper design question.** The real question is not "can the system complete in 8 seconds?" but "does the user feel confident enough to approve within 3 seconds of seeing the trace?" That is a trust metric, not a latency metric. Experiment 2 should be redesigned to measure system latency and user decision time separately.

**Memory quality is the make-or-break technical bet.** If memory retrieval is good, the product is differentiated, defensible, and delightful. If memory retrieval is mediocre, it is worse than having no memory at all. The brief should elevate memory retrieval quality from a risk item to the central technical investment thesis.

### Refined Recommendations

1. **Mandate a technical architecture appendix** covering memory storage and retrieval approach, background processing architecture, and per-user LLM cost model.
2. **Include source attribution in the approval gate as a v1 requirement.**
3. **Split Experiment 2 into two metrics:** system round-trip time (target: under 5 seconds) and user approval decision time (target: under 3 seconds).
4. **Add an explicit "why now" section** grounded in the LLM cost curve.
5. **Scope a memory quality benchmark before Experiment 3.**

---

**[Product Manager]**

### Agreements

**With the UX Researcher — single-archetype risk is the biggest strategic vulnerability.** 40 of 53 participants unaddressed is not just a desirability gap — it is a viability gap. A Series A investor will ask "what's the TAM for Workflow Optimisers who use Google Workspace?" and the honest answer is a small fraction of the $47-50B headline number. The brief needs at minimum a credible second-archetype expansion sketch.

**With the Engineer — unit economics are the unwritten chapter.** The feasibility review's point about LLM cost per user at $17/month lands directly in viability territory. If persistent memory requires frequent embedding generation, vector search, and background inference for proactive surfacing, we could be looking at $5-10/month in infrastructure cost per active user before OAuth maintenance, support, or hosting. That leaves gross margins of 40-70% — viable at scale but dangerously thin during the subsidised pilot phase. The brief must model this explicitly.

**With the UX Researcher — confidence signalling cannot wait.** I initially accepted deferring confidence signals to post-MVP. The desirability review changed my position. If retrieval provenance is what separates "helpful memory" from "creepy surveillance," then it is not a nice-to-have — it is the trust mechanism that determines whether the memory recall moment in Experiment 3 drives conversion or drives uninstalls.

### Disagreements or Tensions

**On the strategic brief mismatch — I think it matters less than the UX review suggests.** The UX Researcher flags that the strategic brief asks for a "personal assistant" while the MVP delivers a "work coordination tool." This is a deliberate and correct narrowing. The risk is not that the MVP is too narrow versus the brief — the risk is that it is too narrow versus the addressable market. These are different problems with different solutions.

**On the 8-second metric — I side with the Engineer but for business reasons.** From a viability perspective, the real metric is not round-trip time — it is whether the approval gate feels faster than doing the task manually. If it takes 8 seconds but the alternative is 45 seconds of switching apps, that is a win. The experiment should benchmark against the manual alternative, not an absolute time threshold.

### Cross-Cutting Insights

**All three reviews converge on the same root concern: the brief is strong on what to build but silent on how the business works.** Desirability says "trust mechanics are underspecified." Feasibility says "infrastructure costs are unacknowledged." Viability says "acquisition and unit economics are absent." These are not three separate problems — they are one problem: the brief describes a product, not a business. A product brief can defer go-to-market. An MVP brief that asks for $17/month cannot.

**The memory layer is simultaneously the moat, the risk, and the cost driver.** All three reviews identified persistent memory as the critical subsystem from different angles — desirability (trust), feasibility (architecture), viability (cost and differentiation). The brief should acknowledge this single-point dependency explicitly.

**Google Workspace dependency creates a ceiling the brief does not size.** Workflow Optimisers who use Google Workspace is a subset of a subset. The brief should state the addressable segment size for the launch configuration honestly.

### Refined Recommendations

1. **Add a unit economics model to the brief.** Even rough estimates transform the revenue table from projection to plan.
2. **Sketch a two-archetype expansion path.** Identify the next-most-evidenced archetype and describe the product changes required.
3. **Reframe Experiment 2 around comparative friction** — benchmark against manual alternative, not an absolute 8-second threshold.
4. **Promote retrieval provenance to MVP scope.** Move from "out of scope" to "minimal viable trust."
5. **Add a "why now" section** — two sentences on model cost decreases, API maturity, and user readiness after two years of ChatGPT habituation.

---

## Round 2

**[UX Researcher]**

- **The PM frames narrowing as correct scope discipline; I frame it as an architectural bet that needs to be made explicit.** We may not actually disagree on what to build in v1 — the disagreement is about what the brief should say about its own constraints. A single paragraph stating which v1 architectural decisions enable expansion and which constrain it would resolve this tension without changing scope. The PM says the problem is market sizing, not vision alignment — but if the architecture locks you into professional task management, the market you sized is unreachable from the product you built.

- **The risk is not building too small — it is building narrowly in ways that foreclose the broader vision without realising it.** Persistent memory scoped to email and calendar commitments creates a data model optimised for professional obligations. If the memory schema cannot represent personal preferences, health routines, or relationship patterns, expanding later requires a data migration, not a feature addition. This is exactly the kind of constraint that should be named in v1, not discovered in v2.

- **The PM's reframe actually strengthens my concern.** The PM says the brief describes a product, not a business. Part of describing a business is articulating a credible path from first user to target market. If the strategic brief's TAM of $47-50B assumes a personal assistant and the MVP validates only professional workflow coordination, the TAM is overstated by an order of magnitude. Either the expansion narrative exists and should be stated, or the market sizing should be revised downward to reflect what this product actually is.

- **Concrete resolution proposal.** Add a "v1 Expansion Constraints" subsection — three to five sentences maximum — stating: (1) which architectural choices in v1 are archetype-neutral (e.g., the approval gate, memory retrieval engine) and which are archetype-specific (e.g., email/calendar as sole data sources, commitment-tracking as the memory schema), and (2) what the first expansion target would be after Maya Patel validates.

---

**[Engineer]**

- **The three-trust-dimension framework is analytically correct but architecturally misleading for v1.** Data trust, competence trust, and agency trust are real and distinct — but they do not require three separate engineering subsystems. Data trust is handled by OAuth scoping and encryption-at-rest. Agency trust is handled by the approval gate. Competence trust is handled by source attribution on memory-sourced outputs. The risk is not missing subsystems — it is missing measurement.

- **Where I concede ground: the experiments must measure all three dimensions separately, even if the architecture does not separate them.** If Experiment 1 returns a low trust score, we need to know whether users distrust the data handling, the memory accuracy, or the action execution. A single trust metric makes failure undiagnosable — the UX Researcher is right on this point.

- **Source attribution is the only engineering change this implies for v1 scope.** Data trust requires standard security practices. Agency trust requires the approval gate. Competence trust requires source attribution. The three-trust framework does not add engineering scope — it adds experimental instrumentation. That is a design and measurement task, not a build task.

- **The daily briefing is where all three trust dimensions collide, and the UX Researcher is right that it is underdesigned.** The briefing is the first surface where the user encounters memory (competence trust), sees what data was accessed (data trust), and decides whether to act (agency trust). If the briefing design is vague, the experiments will test an undefined artifact and the trust measurements will be noise.

- **Remaining disagreement: the UX Researcher's framing risks scope inflation if taken as a build requirement rather than a measurement requirement.** "Three trust dimensions" should be read as "measure three trust outcomes," not "build three trust mechanisms." If the panel agrees on this reading, we are aligned.

---

**[Product Manager]**

- **It is both, but market sizing is the one that kills you at Series A.** The UX Researcher is right that architecture decisions in v1 can lock out broader personal use cases. But architecture debt is fixable with engineering investment. Telling investors you sized a $47-50B market and then built for a $200M sliver of it is a credibility problem that no pivot can repair. The brief must solve market sizing first.

- **The UX Researcher's "data gravity as structural moat" argument is persuasive — and it changes what the brief must say about retention economics.** Data gravity only works if users stay long enough to accumulate meaningful context. The Engineer's $0.50-$2.00/day inference cost means heavy users — the ones generating the most data gravity — are the ones most likely to be margin-negative at $17/month. The brief needs a retention-cost model showing the crossover point where data gravity offsets acquisition cost.

- **The daily briefing convergence across all three reviews is the clearest signal from this discussion.** The UX Researcher calls it "the real MVP," the Engineer's cost model shows it is the primary inference cost driver, and from my perspective it is the only surface where the value proposition becomes tangible enough to justify $17/month. Yet it remains a single bullet point in the brief. If one feature must be fully specified before Experiment 1, it is this one.

- **On architecture lock-in specifically: the v1 risk is not the memory schema, it is the integration surface.** Building exclusively on Gmail and Google Calendar does not just narrow the addressable market — it creates a dependency that constrains which personal use cases are even expressible. If v1 ships with an integration architecture that assumes all user context flows through OAuth-connected productivity tools, expanding to broader personal use cases requires not just new integrations but a fundamentally different context ingestion model.

- **My revised position: the brief needs three additions, in priority order.** First, an honest addressable market size for the launch configuration (Workflow Optimisers on Google Workspace). Second, a unit economics model accounting for the Engineer's inference cost estimates and showing at what retention rate data gravity produces positive LTV. Third, a one-paragraph architecture extensibility statement from the Engineer confirming whether the v1 memory and ingestion layers can serve non-productivity use cases without a rebuild.
