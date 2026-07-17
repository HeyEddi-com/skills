
# Anti-patterns: Build verification

- NEVER merge when `verify_build` exits non-zero.
- NEVER silence build warnings that indicate missing chunks or dynamic import failures.
- NEVER assume dev-server success implies production build success.
- NEVER ship AI prose slop (em/en dashes, delve/leverage/tapestry, "Certainly!", "it is important to note", emoji theater); follow `context/PROSE_ANTI_SLOP.md` fully
