
# Anti-patterns: Pre-merge gate

- NEVER merge on FAIL status for build or test.
- NEVER treat SKIP as PASS: investigate missing tooling in CI.
- NEVER ship AI prose slop (em/en dashes, delve/leverage/tapestry, "Certainly!", "it is important to note", emoji theater); follow `context/PROSE_ANTI_SLOP.md` fully
