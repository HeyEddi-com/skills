# Anti-patterns

- **Skipping SKILL.md** — suggestions are pointers; always read the target skill before tools.
- **Loading every skill at once** — wastes context; use catalog + 1–3 reads.
- **Ignoring skill-routing.json** — when present, it overrides keyword guesses.
- **Implementing in orchestrator** — this skill routes only; no product/design/code output.
- **Hardcoding skill list in chat** — run `load_catalog` so descriptions stay in sync with registry.
- **Central trigger map in orchestrator** — each skill owns optional `reference/triggers.md` instead.
