# Anti-patterns: Project engineering

- NEVER ship a new view without running `audit_scaffold` on thin repos first.
- NEVER skip `write_test_stub` for user-facing views when `tests/` exists.
- NEVER replace real `vite build` with echo stubs in production app repos.
- NEVER run `scaffold_vue --force` on mature apps without reviewing overwrites.
- NEVER ship AI prose slop (em/en dashes, delve/leverage/tapestry, "Certainly!", "it is important to note", emoji theater); follow `context/PROSE_ANTI_SLOP.md` fully
