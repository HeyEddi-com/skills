@pr-submission-review

## Review submitted PR #42 (fixture mode)

This eval uses a **fixture diff** — do not call live `gh` for PR metadata.

1. Run `fetch_pr_context` with `--pr 42 --fixture .pr-fixture/diff.json --project-root . --write-cache`
2. Run `check_doc_drift` with `--pr 42 --fixture .pr-fixture/diff.json --project-root .`
3. Run `audit_pr_changes` with `--pr 42 --fixture .pr-fixture/diff.json --project-root .`
4. Read `.heyeddi/product.md` — note `/dashboard` AC vs changed composable/API files
5. Run `write_pr_review` with `--pr 42 --fixture .pr-fixture/diff.json --force --project-root .`
6. **Fill the report** `.heyeddi/docs/pr-42-review.md`:
   - Set **Verdict** to `Request changes` (no tests in PR, doc drift on API change)
   - Complete Summary and Product fit with concrete notes (not placeholders)
7. Run `verify_pr_review --pr 42 --check --project-root .`

Scope: committed files in fixture only (`useUsers.ts`, `users.py`). Do not review uncommitted work.
