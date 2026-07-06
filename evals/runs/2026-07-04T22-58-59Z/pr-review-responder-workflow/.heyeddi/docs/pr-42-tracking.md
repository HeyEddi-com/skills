# PR #42 — Comment Tracking Table

**PR:** 42 · **Repo:** heyeddi/taskflow-app  
**Date:** 2026-07-04  
**Mode:** Fixture (no live `gh api` replies)

| ID | Type | Author | Summary | Action | Response Status |
|---|---|---|---|---|---|
| 9001001 | inline | qa-reviewer | Pagination uses 0-based `page` but API expects 1-based | fix | DRAFTED |
| 9001002 | inline | backend-lead | Redundant `Depends(get_db)` on unused `db` parameter | fix | DRAFTED |
| DC_10001 | discussion | product-owner | Request loading state on dashboard during user fetch | decline | DRAFTED |
| 8001 | review | backend-lead | CHANGES_REQUESTED — address inline pagination and Depends notes | acknowledge | DRAFTED |
| 8002 | review | qa-reviewer | APPROVED — LGTM once CI is green | acknowledge | DRAFTED |

**Totals:** 5/5 comments tracked · 5/5 response plans drafted

## Fix Details

### 9001001 — Pagination (applied)

- **File:** `src/composables/useUsers.ts`
- **Change:** Default `page` parameter changed from `0` to `1` so the query string sent to `/api/users?page=` is 1-based, matching the API contract.

### 9001002 — Redundant Depends (applied)

- **File:** `backend/app/routers/users.py`
- **Change:** Removed unused `db=Depends(get_db)` parameter, `get_db` helper, and `Depends` import. The endpoint returns a static list and never used the injected dependency.

### DC_10001 — Loading state (declined)

- **Reason:** Out of scope for this PR, which focuses on user fetch pagination and backend list endpoint cleanup. Dashboard loading UX should be a separate frontend PR tied to the dashboard component.
