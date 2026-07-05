Independent **@design-handoff** eval.

## Pipeline
- Agent-authored `mockup-brief.md` with **`## Implementation spec`** (measurable tokens/CSS — not prose only)
- Two-pass workflow per `handoff-to-code.md` (designer then implementer)
- `verify_handoff` + `verify_tokens` run as **hard gates** before the agentic judge

## UI
- App shell + settings cards; spacing not cramped; active nav brand pill
- **FAIL if:** no Implementation spec, bare email/password-style settings without shell polish, sidebar user not pinned bottom, gray full-bleed active nav
- **FAIL if:** `tokens.css` has circular aliases (`--size-N: var(--size-N)`) or rendered spacing checks fail (card padding < 16px, gap < 16px, sidebar < 220px)
- Visual captures in `.heyeddi/audits/eval-capture/` — structure vs reference PNGs; **high pixel similarity does not excuse cramped spacing**
- Tests/build clean
