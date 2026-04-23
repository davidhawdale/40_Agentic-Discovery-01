# MVP Brief: Personal AI Assistant

> Max 2500 words. Every section must fit the page budget. Cut before padding.

## Problem Statement

Today's AI tools are capable but not personal. Users re-explain context every session, receive hallucinated results with no warning, and face disconnected apps that force them to be their own integration layer.

The core frustration across 53 interviews is three-fold: AI doesn't remember you, doesn't act until prompted, and can't signal when it's wrong. "There's also no way to know which parts are not accurate, especially if you're not an expert in the field." It presents errors "in a very confident and convincing way, even when it's completely wrong." (Participants 6, 8)

Users who want proactive help instead describe managing the gap themselves: "all of those things live in separate applications ... I end up being my own single point of failure." (Participant 50) The most resonant vision in the data: an assistant that takes initiative — "someone who would take initiatives, more than an assistant who would wait for me to tell it to do things." (Participant 37)

No current product addresses all three gaps. The MVP targets exactly this combination: persistent memory, proactive commitment-tracking, and human-in-the-loop action.

## Scope

### In Scope

- **Persistent cross-session memory** of the user's commitments and priorities, maintained across all sessions
- **Proactive commitment surfacing** — the assistant surfaces overdue or at-risk commitments before the user asks
- **Email and calendar read access** (Gmail and Google Calendar at launch) to identify tasks, deadlines, and scheduling gaps
- **Daily briefing:** "What do I have today? What did I say I would do that I haven't done?"
- **Human-review step before any outbound action** — user approves before any send or calendar write

### Out of Scope

- **Autonomous outbound action without approval** — trust must be earned incrementally before removing this gate (Participants 3, 46, 35)
- **Creative generation, emotional support, DIY guidance** — deferred to preserve MVP focus on commitment-tracking
- **Confidence signalling** — relevant for Guarded Verifiers but adds scope risk to v1; revisit after core loop is validated
- **Team-level coordination** — dilutes the single-user learning signal at this stage
- **Integrations beyond Gmail and Google Calendar** — Outlook, Apple Mail, and messaging extend after core loop is validated

## Target User

### Primary User: Maya Patel — Workflow Optimiser

Maya is a 42-year-old operations lead. Her daily friction is exactly what the research identifies. Participant 50 stated it plainly: "all of those things live in separate applications ... I end up being my own single point of failure." Participant 28 described the ideal as an assistant that taps into email and calendar and answers "is there something that I said I would do that I haven't yet achieved?" — persistent memory and proactive action in a single sentence.

The Workflow Optimisers archetype has 13 participants, the largest evidence base in the study. They are productivity-heavy professionals who already live in calendar and email tools, treat AI as a legitimate work tool, and have concrete daily coordination pain — which means their success criteria are unambiguous, and experiments yield a clear signal.

Maya is the right first user for three reasons. First, her pain is structural: she coordinates across tools and people in ways that no single app currently handles. Second, she has enough tolerance for new tooling that she will persist through rough edges in a pilot — but enough baseline scepticism that she will not inflate engagement data. Third, she maps directly onto a reachable acquisition segment: productivity professionals already paying for at least one AI subscription. Building for Maya first does not rule out later segments; it gives the product a focused validation target before expanding.

## Experiments

### Experiment 1: Daily Briefing Engagement

**Hypothesis:** Workflow Optimisers who connect email and calendar to a persistent-memory assistant will use the daily briefing and commitment-tracking at least three times per week, because it removes the overhead they currently absorb themselves.

**Build:** A daily briefing interface reading Gmail and Google Calendar. The assistant maintains a running commitment list derived from emails and calendar events and surfaces a prioritised morning briefing. All outbound actions require user approval before any write occurs.

**Measure:** Weekly active use rate of the daily briefing across 20 Workflow Optimiser-profile users over a 4-week pilot.

**Success signal:** 60% open the briefing at least 3 times per week by week 3; 40% describe commitment-tracking as "would miss it if removed."

**Failure signal:** Fewer than 30% open the briefing more than once per week after week 1, or output requires too much correction to be useful.

---

### Experiment 2: Approval-Gated Calendar Reschedule (Technical Spike)

**Hypothesis:** An approval-gated reschedule — OAuth read, one-step reasoning trace, tap-to-confirm, calendar write — can complete in under 8 seconds with a trace that a non-technical user validates as trustworthy.

**Build:** End-to-end spike: read via OAuth, display a single-step reasoning trace ("I moved Tuesday's 10am because you have a conflict with the client call"), present a tap-to-confirm screen, write back to calendar.

**Measure:** Round-trip time (read to write) and trace comprehension rating across 5 non-technical testers.

**Success signal:** All 5 testers complete under 8 seconds; all rate the trace "clear enough to trust"; calendar write matches stated intent.

**Failure signal:** Exceeds 12 seconds median, or trace is rated unreadable by 2 or more testers — UX architecture needs redesign before any feature builds on this foundation.

---

### Experiment 3: Memory Recall Moment and Conversion

**Hypothesis:** Users who experience a memory recall moment in their first two sessions — the assistant correctly surfaces a commitment from a previous session — convert at higher rates at the paywall, making persistent memory the primary willingness-to-pay driver at MVP stage.

**Build:** 14-day free trial with full features (daily briefing, commitment tracking, email and calendar read access); hard paywall at day 15 with a $17/month prompt.

**Measure:** Trial-to-paid conversion rate, segmented by whether users experienced a memory recall event in sessions 1–2 (assistant correctly referenced a prior commitment unprompted).

**Success signal:** Conversion rate 15% or above among users with a memory recall event.

**Failure signal:** Conversion rate below 8% across both segments — product has not yet demonstrated sufficient value to justify a subscription.

## Risks and Constraints

### Technical Risks

- **Memory retrieval false matches:** Semantic search surfaces plausible-but-wrong context. Stale memory ("you prefer mornings" from a previous job) driving proactive actions is worse than no memory — it destroys trust at the moment the feature is most visible.
- **OAuth scope sprawl:** Read-write calendar and email spans Gmail, Outlook, and Apple Mail — three separate rate-limit and schema surfaces. Gmail at launch limits this, but Outlook expansion will require re-engineering the data access layer.
- **Agentic action irreversibility:** Sent emails and accepted invites cannot be recalled. External side effects need a hard confirmation gate — not a toast notification that can be dismissed accidentally.
- **Approval-gate abandonment:** If the human-review step adds more friction than completing the task manually, users will bypass or stop using it. Must be sub-5-seconds and mobile-native to remain useful rather than obstructive.
- **Confidence signal miscalibration:** A "high confidence" badge on a wrong interpretation destroys trust faster than no badge at all. Any confidence indicator must be grounded in retrieval evidence, not logit probability.

### Constraints

- **Human approval before external action** — no send or calendar write without explicit confirmation. Non-negotiable: Participants 3, 46, 35 made this a condition of trust, not a preference.
- **Granular OAuth consent** — per-source controls, not "allow all." Participants 50, 13, 45 cited data access granularity as the primary privacy requirement.
- **Step-visible reasoning** — reasoning trace must appear in the UI, not only in logs. Participant 18: "If they can show me the things that they are doing step by step, I can spot whether there's any step that's slightly off track."
- **No data resale** — memory scoped to that user only. Participants 50, 13, PL13 identified resale as a trust-breaking condition.

## Market Review

### Competitor Landscape

| Product                  | Price/month | Memory                                                         | Proactive                                  | Integration                                           |
| ------------------------ | ----------- | -------------------------------------------------------------- | ------------------------------------------ | ----------------------------------------------------- |
| ChatGPT Plus (OpenAI)    | $20         | Partial — opt-in, shallow, user-reported as unreliable        | None                                       | Limited; plugins fragmented                           |
| ChatGPT Pro (OpenAI)     | $200        | Same as Plus                                                   | None                                       | Same as Plus                                          |
| Claude Pro (Anthropic)   | $20         | Projects hold scoped context; no cross-session personal memory | None                                       | None built-in                                         |
| Claude Max (Anthropic)   | $100        | Same as Pro                                                    | None                                       | None built-in                                         |
| Gemini Advanced (Google) | $20         | No persistent personal memory                                  | None                                       | Google Workspace read-access; limited action-taking   |
| Perplexity Pro           | $20         | None                                                           | None                                       | None                                                  |
| Rewind / Limitless       | $19         | Strong local capture; no cross-app action layer                | None — search-only                        | Screen/audio capture; no calendar or email write      |
| Reclaim.ai               | $10–$20    | None conversational                                            | Proactive scheduling only — narrow domain | Deep Google Calendar + task; no email or AI reasoning |
| Mem.ai                   | $14.99      | Note-level memory; no behavioural or preference memory         | None                                       | Notes capture; no calendar or email action            |

### Market Size

The global AI assistant market was valued at approximately $15–16 billion in 2023 and is projected to reach $47–50 billion by 2030, a CAGR of roughly 17–19% (Grand View Research / MarketsandMarkets, 2023–2024). The personal productivity segment — AI tools used by individuals for task management, scheduling, and communication — is the fastest-growing sub-segment. By 2025, over 100 million users globally were paying for at least one AI assistant subscription, establishing a clear willingness-to-pay baseline.

### The Gap

Three structural gaps are unoccupied by any current competitor:

- **Persistent personal memory:** No mainstream assistant maintains durable, cross-session knowledge of user preferences, working patterns, or ongoing commitments. ChatGPT's memory toggle is opt-in, shallow, and user-reported as unreliable. Claude and Gemini start fresh by default. Mem.ai captures notes but not behavioural context. The gap is structural — none of these products are designed to know you across time.
- **Proactive action:** Every product in the table waits to be asked. Reclaim.ai is the closest exception — it reschedules tasks autonomously — but operates in a narrow scheduling domain with no language reasoning layer. No product monitors context (calendar, email, task state) and surfaces relevant actions unprompted. This is the whitespace the 53 interviews named most explicitly.
- **Calendar and email integration with a reasoning layer:** Gemini has the deepest integration (Google Workspace), but it surfaces data rather than acting on it. Reclaim.ai writes to calendars but cannot reason across email or messaging. No product today combines read/write access to calendar and email with a conversational AI layer capable of drafting, summarising, and taking consent-gated action.

*Pricing data as of mid-2025 — verify before publishing.*

## Opportunity Statement

### Revenue Model

Four models were evaluated:

- **Monthly subscription:** Low commitment barrier, fast churn signal — but higher churn risk before stickiness is proven.
- **Annual subscription:** Higher LTV and lower churn — but asks for commitment before persistent memory value has been demonstrated.
- **Freemium + paid tier:** Lowers acquisition friction — but delays revenue and risks commoditising free-tier features.
- **Per-seat team pricing:** Upside if work-calendar integration resonates — but adds sales complexity before product-market fit is confirmed.

**Recommendation:** Monthly subscription at launch. It yields the fastest willingness-to-pay and churn signals without requiring an annual commitment before the core differentiation — persistent memory and proactive action — has been demonstrated at scale.

### Pricing

$17/month is defensible. It matches mainstream AI chat pricing (ChatGPT Plus, Claude Pro, Perplexity Pro all at $20) while undercutting marginally to reduce switching friction. Mem.ai ($14.99) and Reclaim.ai ($10–$20) anchor the productivity sub-segment below $20. The premium features — durable cross-session memory, proactive action, consent-gated calendar and email integration — justify matching the $20 ceiling rather than discounting to productivity-tool levels.

### Revenue Potential

| Scale            | Monthly revenue     | ARR |
| ---------------- | ------------------- | --- |
| 10k subscribers  | $170,000 | $2.0M    |     |
| 50k subscribers  | $850,000 | $10.2M   |     |
| 100k subscribers | $1,700,000 | $20.4M |     |

*Assumption: all subscribers on the $17/month monthly plan; no annual discount or freemium tier applied.*

The $10M ARR threshold — reachable at approximately 50,000 subscribers — is the scale at which this becomes a fundable growth-stage business. At 100,000 subscribers the ARR exceeds $20M; comparable productivity SaaS businesses at this ARR have commanded 8–12x revenue multiples in recent funding rounds. The ceiling is larger: if the assistant expands to team use cases after validating single-user product-market fit, per-seat pricing on a 10-person team at $12/seat would yield $120/month per account — doubling or tripling the unit economics without changing the product architecture.

---

*March 2026 · Based on [53] interview transcripts and market data*
