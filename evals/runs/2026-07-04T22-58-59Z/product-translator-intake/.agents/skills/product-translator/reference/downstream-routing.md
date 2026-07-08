# Downstream routing

After `write_routing.py`, `.heyeddi/docs/intake/skill-routing.json` drives the team:

```json
{
  "frontend": "vue",
  "backends": ["fastapi"],
  "product_name": "TaskFlow",
  "routes": [
    {
      "route": "/",
      "register": "brand",
      "skill": "heyeddi-design",
      "mode": "craft",
      "feature": "taskflow-marketing"
    },
    {
      "route": "/dashboard",
      "skill": "heyeddi-design",
      "mode": "craft",
      "feature": "taskflow-dashboard",
      "notes": "Team roster table — not 3 KPI wireframe"
    },
    {
      "route": "/settings",
      "skill": "heyeddi-handoff",
      "feature": "settings",
      "mockups": ".heyeddi/designs/settings/",
      "brief": ".heyeddi/designs/settings/mockup-brief.md"
    }
  ],
  "scaffold": ["project-engineering", "scaffold_stack --stack full"]
}
```

## Skill selection rules

| Surface | Has PNG + brief | Skill |
|---------|-----------------|-------|
| Settings / handoff screen | Yes | `@heyeddi-handoff` |
| Marketing / greenfield app page | No PNG | `@heyeddi-design` shape → craft |
| Flutter app | product.md says flutter | `@flutter-engineering` then handoff-flutter |
| API types | fastapi in backends | `@dart-type-bridger` or `@backend-type-bridger` |

Always run `@heyeddi-design document` if `design.md` missing before craft/handoff.
