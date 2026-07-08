# Subagent delegation — heyeddi-pr-respond

| Step | Subagent | Readonly | Worker prompt |
|------|----------|----------|---------------|
| `fetch_pr_comments.py` | `shell` | yes | PR number; fixture path in evals |
| Analyze each comment (fix vs decline) | `generalPurpose` | yes | One batch or one subagent per thread for large PRs |
| Apply code fixes | `generalPurpose` | no | Scoped to approved fixes |
| `gh api …/replies` | `shell` | no | One reply per comment ID |
| Summary comment | main | — | After all threads replied |

Main chat owns the tracking table and ensures **every** comment gets a threaded reply.
