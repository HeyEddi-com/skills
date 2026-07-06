# Research — trend and reference gathering

**Scope:** External context to inform the brief. No code.

**When:** After discovery, before explore/brief. Mandatory in **`shape`** unless the user explicitly opts out.

## Process

1. **Form 2–4 search queries** from discovery answers — combine domain + surface type + year:
   - Product category (e.g. "B2B SaaS admin", "enterprise settings")
   - Pattern (e.g. "sidebar navigation", "data table density", "settings IA")
   - Optional: named anchors from discovery ("Linear app navigation patterns") — see `reference/modern-reference.md` for default HeyEddi anchors (Linear, Vercel, Stripe Dashboard, Superhuman, etc.)

2. **Run web search** (use available search tools — do not skip for "efficiency").

3. **Synthesize `designs/<feature>/research.md`** with:
   - **Audience fit** (required) — which persona this research serves; what they'd trust/reject
   - **Trend summary** (3–5 bullets — what's common in 2025–2026 for this surface)
   - **Patterns to adopt** (with rationale tied to user's goals)
   - **Patterns to avoid** (especially AI-slop tropes: cream SaaS default, hero metrics, identical card grids)
   - **References** — linked sources or named products with *what* to borrow (use `modern-reference.md` anchor table as starting point)
   - **Implications for HeyEddi stack** — which PrimeVue components / layout patterns fit

4. **Present a short summary in chat** (5–8 lines) and highlight 1–2 decisions research suggests before explore.

## Quality bar

- Tie every recommendation to discovery answers — not generic "best practices."
- Prefer recent sources; note when citing evergreen patterns vs trends.
- If search returns thin results, say so and lean on named anchor references from discovery.

## Exit

Proceed to `reference/explore.md` (unless fidelity is sketch-only and user skipped visual exploration).
