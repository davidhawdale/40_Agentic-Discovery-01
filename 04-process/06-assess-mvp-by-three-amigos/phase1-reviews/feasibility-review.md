# Feasibility Review — Engineer Lens

## Overall Assessment

The MVP scopes a buildable product, but the brief underestimates the engineering complexity of two critical subsystems: persistent memory retrieval and the approval-gated action pipeline. The experiments are well-designed but Experiment 2's 8-second target conflates network latency with UX latency in a way that may mislead investment decisions.

## Strengths

- **Narrow integration surface at launch.** Gmail and Google Calendar only — avoids the multi-provider OAuth nightmare. This is the right call. Expanding to Outlook and Apple Mail later is a separate engineering phase, and the brief correctly defers it.
- **Human-in-the-loop gate is architecturally simple.** A confirmation step before any write operation is a well-understood pattern (think Zapier's approval steps). This is low implementation risk and high trust payoff.
- **Experiment 2 isolates the hardest technical question early.** The approval-gated calendar reschedule spike directly tests the riskiest integration path. If this fails, the team knows before investing in the full product.
- **Commitment list derived from email and calendar is tractable.** NLP extraction of action items from email bodies and calendar descriptions is a solved-enough problem with current LLMs. The accuracy floor is high enough for an MVP.

## Gaps and Concerns

- **Memory retrieval false matches are the highest-risk failure mode, and the brief names it but does not scope a mitigation.** Semantic search returning plausible-but-wrong context is not an edge case — it is the default behaviour of embedding-based retrieval at scale. Stale memory ("you prefer mornings" from six months ago) triggering a proactive action will destroy trust at the exact moment the product is trying to build it. The brief should specify a memory decay or invalidation strategy, even a simple one (e.g., recency weighting, explicit user correction).
- **The 8-second round-trip target for Experiment 2 is ambitious and poorly defined.** It bundles OAuth token refresh, API read, LLM inference, UI render, user decision time, and API write into a single metric. A cold OAuth token refresh alone can take 2-3 seconds. The experiment needs to distinguish system latency from user decision latency, or the pass/fail signal will be uninterpretable.
- **"Persistent cross-session memory" has no stated storage architecture.** Will this be a vector database, a structured knowledge graph, or raw conversation logs with retrieval? Each has fundamentally different cost, latency, and accuracy profiles. The brief treats memory as a feature without specifying the technical approach, which means engineering cannot estimate cost or timeline.
- **Proactive commitment surfacing requires a scheduling/polling layer that is not addressed.** The assistant needs to run background processes that check calendar and email on a cadence, compare against the commitment list, and trigger notifications. This is not a stateless LLM interaction — it requires persistent infrastructure (cron jobs, message queues, or a push notification service). The brief does not acknowledge this architectural requirement.
- **No mention of LLM cost per user.** A daily briefing that reads email and calendar, maintains memory, and generates personalised output will consume significant tokens per user per day. At $17/month, the unit economics depend heavily on which model tier handles which task. The brief should include a back-of-envelope cost model.

## Key Recommendation

- **Add a one-page technical architecture appendix** that specifies: (1) memory storage and retrieval approach, (2) background processing architecture for proactive surfacing, and (3) per-user LLM cost estimate at the $17/month price point. Without these, engineering cannot validate the feasibility of the revenue model.

## Verdict

**Conditionally feasible.** The core loop (read email/calendar, extract commitments, surface briefing, gate actions) is buildable with current technology. But the brief has three architectural blind spots — memory retrieval quality, background processing infrastructure, and per-user cost — that must be addressed before committing to the experiment timeline. None of these are blockers; all are scope risks that become blockers if ignored.
