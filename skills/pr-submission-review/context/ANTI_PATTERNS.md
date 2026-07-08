
# Anti-patterns — PR submission review

- Reviewing local uncommitted files instead of PR diff.
- Approving when `pre_merge_gate` reports BLOCKED.
- Skipping doc drift when routes or API surface changed.
- Approving new composable/router logic with zero test files or references.
- Using `@pr-review-responder` for initial review (wrong workflow).
- Posting GitHub approve without filling Verdict in `.heyeddi/docs/pr-<N>-review.md`.
