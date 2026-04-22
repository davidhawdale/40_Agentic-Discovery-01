# Viability Review — Discussion Response

## Response to Other Specialists

### Agreements

**With the UX Researcher — single-archetype risk is the biggest strategic vulnerability.** My Phase 1 review flagged single-persona risk independently. 40 of 53 participants unaddressed is not just a desirability gap — it is a viability gap. A Series A investor will ask "what's the TAM for Workflow Optimisers who use Google Workspace?" and the honest answer is a small fraction of the $47-50B headline number. The brief needs at minimum a credible second-archetype expansion sketch, even if it is out of scope for v1 build.

**With the Engineer — unit economics are the unwritten chapter.** The feasibility review's point about LLM cost per user at $17/month lands directly in viability territory. If persistent memory requires frequent embedding generation, vector search, and background inference for proactive surfacing, we could be looking at $5-10/month in infrastructure cost per active user before OAuth maintenance, support, or hosting. That leaves gross margins of 40-70% — viable at scale but dangerously thin during the subsidised pilot phase. The brief must model this explicitly.

**With the UX Researcher — confidence signalling cannot wait.** I initially accepted deferring confidence signals to post-MVP. The desirability review changed my position. If retrieval provenance is what separates "helpful memory" from "creepy surveillance," then it is not a nice-to-have — it is the trust mechanism that determines whether the memory recall moment in Experiment 3 drives conversion or drives uninstalls. This has direct viability implications: a product that feels surveillant will not retain, and retention is the entire revenue model.

### Disagreements or Tensions

**On the strategic brief mismatch — I think it matters less than the UX review suggests.** The UX Researcher flags that the strategic brief asks for a "personal assistant" while the MVP delivers a "work coordination tool." This is a deliberate and correct narrowing. Every successful consumer product starts narrower than the vision. The risk is not that the MVP is too narrow versus the brief — the risk is that it is too narrow versus the addressable market. These are different problems with different solutions. The brief's framing is fine; the market sizing needs work.

**On the 8-second metric — I side with the Engineer but for business reasons, not technical ones.** The Engineer correctly identifies that the 8-second target bundles too many things. From a viability perspective, the real metric is not round-trip time — it is whether the approval gate feels faster than doing the task manually. If it takes 8 seconds but the alternative is 45 seconds of switching apps, that is a win. If it takes 8 seconds but the user could have done it in 5 seconds in their calendar app, the feature is worse than useless. The experiment should benchmark against the manual alternative, not an absolute time threshold.

### Cross-Cutting Insights

**All three reviews converge on the same root concern: the brief is strong on what to build but silent on how the business works.** Desirability says "trust mechanics are underspecified." Feasibility says "infrastructure costs are unacknowledged." Viability says "acquisition and unit economics are absent." These are not three separate problems — they are one problem: the brief describes a product, not a business. A product brief can defer go-to-market. An MVP brief that asks for $17/month cannot.

**The memory layer is simultaneously the moat, the risk, and the cost driver.** All three reviews identified persistent memory as the critical subsystem, but each from a different angle — desirability (trust), feasibility (architecture), viability (cost and differentiation). This convergence tells us something: the memory layer is the entire bet. If it works well, the product is differentiated and retains. If it fails — stale recalls, false matches, high inference cost — the product has no fallback position. The brief should acknowledge this single-point dependency explicitly and ensure Experiment 3 is designed to stress-test memory quality, not just measure conversion rates.

**Google Workspace dependency creates a ceiling the brief does not size.** My Phase 1 question about Gmail/Google Calendar platform risk was not addressed in any review, but it compounds the single-persona problem. Workflow Optimisers who use Google Workspace is a subset of a subset. The brief should state the addressable segment size for the launch configuration honestly — even if the number is small, showing awareness of it builds credibility with investors.

## Refined Recommendations

1. **Add a unit economics model to the brief.** Even a rough estimate — LLM inference cost per user per month, OAuth and infra overhead, target gross margin — transforms the revenue table from projection to plan. This is the single highest-impact addition for investor credibility.

2. **Sketch a two-archetype expansion path.** The brief does not need to build for a second archetype, but it needs to show one. Identify the next-most-evidenced archetype from the 53 interviews, describe their pain overlap with Workflow Optimisers, and explain what product changes would be required to serve them. This converts single-persona risk from a weakness to a staged growth story.

3. **Reframe Experiment 2 around comparative friction.** Replace the absolute 8-second target with a relative benchmark: approval-gated action must be measurably faster than the manual alternative for the same task. This makes the success signal business-meaningful, not just technically achievable.

4. **Promote retrieval provenance to MVP scope.** Move confidence signalling from "out of scope" to "minimal viable trust" — even a simple "recalled from [date] conversation" attribution on surfaced memories. The cost of building this is low; the cost of shipping memory without it is a trust failure that kills retention.

5. **Add a "why now" section.** Two sentences explaining the market timing — model cost decreases, API maturity, user readiness after two years of ChatGPT habituation — would address the gap that any investor will probe. The data is available; the brief simply omits the argument.
