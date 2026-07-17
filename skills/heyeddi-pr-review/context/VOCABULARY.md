
# Vocabulary: PR submission review

- **Submission review:** Judge committed PR diff before approval: not replying to comments.
- **Scope:** `base...head` only: ignore uncommitted working tree.
- **Doc drift:** Product/design/engineering docs out of sync with code changes.
- **Verdict:** Approve | Request changes | Block: written in `pr-<N>-review.md`.
- **Gate:** Hard checks from `@pre-merge-gate` (tests, build, types).
