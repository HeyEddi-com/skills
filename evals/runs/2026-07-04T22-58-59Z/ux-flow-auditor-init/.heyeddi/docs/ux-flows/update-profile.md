# Flow: update-profile

**Task ID:** update-profile  
**Goal:** User updates display name and saves profile  
**Route:** `/settings`  
**Click budget:** 4  
**Persona:** Riley (IC contributor — wants control over profile)  
**Status:** Init — not traced yet

Machine-readable steps: [update-profile.flow.json](update-profile.flow.json)

## Flow summary

| Step | Action | Element |
|------|--------|---------|
| 1 | Expect | Profile form visible |
| 2 | Fill | Display name field |
| 3 | Click | Save changes |

## Friction notes

### Settings only reachable via app-shell nav (Medium)

**Observation:** Product intent for `/settings` is "clear settings, one obvious save" (see `.heyeddi/product.md`). This flow assumes direct entry at `/settings`, but Riley typically lands on `/dashboard` first. Reaching settings requires an extra nav click before the form appears — consuming budget before any editing begins.

**Suggested fix:** Add a profile shortcut in the app shell (avatar menu or "Edit profile" link on the dashboard) that deep-links to `/settings` and focuses the display-name field. Keeps the 4-click budget when users don't start on the settings route.

## Next step

After `/settings` is implemented and the dev server is running:

```bash
npm run dev
python .agents/skills/ux-flow-auditor/scripts/trace_flow.py --task-id update-profile --project-root . --check
```

This generates click metrics and step screenshots under `.heyeddi/audits/ux-flow/`.
