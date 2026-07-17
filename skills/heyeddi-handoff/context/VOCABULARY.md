
# Vocabulary: Design handoff

- **Role**: designer **and** frontend developer: layout, component architecture, Vue implementation.
- **Token source**: project semantic CSS vars (`tokens.css`); OpenProps optional: detect via `package.json` / `design.md` (`heyeddi-design/reference/token-strategy.md`).
- **Mockup contract**: PNGs define **layout regions**; colors from `design.md` tokens, not PNG pixels (`reference/mockup-contract.md`).
- **Component strategy**: per region: reuse catalog | PrimeVue as-is | thin wrapper | custom component.
- Handoff brief: route, screenshots[], notes, component mapping hints.
- `.heyeddi/designs/<feature>/`: designer-provided PNG/SVG references (legacy: `designs/<feature>/`).
- `handoff.json`: optional structured brief (shell topology, region notes).
- **Layout components**: `AppShell`, `AppSidebar`, `AppTopBar`, `PageHeader`; implement or reuse before route body.
- **Custom component**: new `.vue` when PrimeVue + tokens cannot achieve mockup layout/behavior; add to `design.md` **Components**.
