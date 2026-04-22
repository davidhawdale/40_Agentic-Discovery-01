## Risks and Constraints

### Technical Risks

- **Confidence signal miscalibration:** A "high confidence" badge on a wrong interpretation destroys trust faster than no badge. Must be grounded in retrieval evidence, not logit probability.
- **Memory retrieval false matches:** Semantic search surfaces plausible-but-wrong context. Stale memory ("you prefer mornings" from a previous job) driving actions is worse than no memory.
- **OAuth scope sprawl:** Read-write calendar and email spans Gmail, Outlook, and Apple Mail — three separate rate-limit and schema surfaces.
- **Agentic action irreversibility:** Sent emails and accepted invites cannot be recalled. External side effects need a hard gate, not a toast.
- **Approval-gate abandonment:** If review adds more friction than doing the task manually, users leave. Must be sub-5-second, mobile-native.

### Constraints

- **Human approval before external action:** Users 3, 46, 35 — no send or calendar write without explicit confirmation.
- **Granular OAuth consent:** Users 50, 13, 45 — per-source controls, not "allow all."
- **Step-visible reasoning:** User 18 — trace in UI, not logged only.
- **No data resale:** Users 50, 13, PL13 — memory scoped to that user only.

### Technical Experiment

**The spike:** Approval-gated calendar reschedule — read via OAuth, show one-step trace, tap-to-confirm, write back.

**Hypothesis:** Round-trip under 8 seconds with a trace a non-technical user validates.

**Pass signal:** Five testers complete under 8 seconds, rate trace "clear enough to trust," write matches intent.

**Fail signal:** Exceeds 12 seconds or trace is unreadable — UX needs redesign before any feature builds on it.
