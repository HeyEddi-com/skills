
# Anti-patterns: Engineering excellence

- NEVER write architecture notes at repo root: use `.heyeddi/docs/engineering/`
- NEVER mix engineering ADRs into `.heyeddi/design.md` Decision log
- NEVER add abstraction before second use case (YAGNI)
- NEVER skip `reuse-catalog.md` update when introducing shared module
- NEVER fatten router files with business rules (SOLID)
- NEVER treat audit warnings as optional without explicit user waive
- NEVER ship AI prose slop (em/en dashes, delve/leverage/tapestry, "Certainly!", "it is important to note", emoji theater); follow `context/PROSE_ANTI_SLOP.md` fully
