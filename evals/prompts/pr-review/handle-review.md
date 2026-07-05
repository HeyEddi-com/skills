@pr-review-responder

## Handle PR #42 review (fixture mode)

This eval uses **fixture comments** — do not call live `gh api` to post replies.

1. Run `fetch_pr_comments` with `--pr 42 --fixture .pr-fixture/comments.json --project-root .`
2. Build a **tracking table** in `.heyeddi/docs/pr-42-tracking.md` — **every** inline comment, discussion comment, and review must have a row with: ID, type, author, summary, action (fix / decline / acknowledge), response status.
3. Draft threaded replies in `.heyeddi/docs/pr-42-replies.md`:
   - Inline comments: one reply block per comment ID (as you would post via `gh api .../comments/ID/replies`)
   - Discussion + review comments: drafted `@mention` responses
4. For comments marked **fix**: apply the code fix in this repo if the referenced files exist (`src/composables/useUsers.ts`, `backend/app/routers/users.py`); otherwise document the fix in the tracking table.
5. End with a **summary** section in `.heyeddi/docs/pr-42-replies.md` (only after all individual replies are drafted).

Team rules: reply to **every** comment; no comment left without a response plan.
