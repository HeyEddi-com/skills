
# Vocabulary: PrimeVue + project tokens

- **Token source:** detect from `package.json` (`open-props`), `tokens.css`, `.heyeddi/design.md`: see `heyeddi-design/reference/token-strategy.md`.
- **Semantic vars:** `var(--surface-1)`, `var(--text-1)`, `var(--brand)`, `var(--font-sans)`: from project `tokens.css`, OpenProps-backed or custom.
- **OpenProps (when present):** prefer aliases in `:root` over raw OpenProps names in components.
- PrimeVue components in use: Button, DataTable, Dialog, InputText, Card, Panel, Toast.
- **Card slots:** `#title`, `#subtitle`, `#content` (required for body), `#footer`: never rely on default slot.
- Vue 3 `<script setup lang="ts">` with typed props and `defineEmits`.
- Import shared wrappers from `@/components/ui/` before creating new primitives.
- Wire PrimeVue Aura `primary` to project `--brand` / `design.md` `{colors.primary}`: never leave default green on shipped UI.
- **PrimeVue v4:** map brand with `definePreset(Aura, { semantic: { primary: { 500: "{indigo.500}", … } } })` in `main.ts`: `--p-primary-color` in CSS alone does not change Aura buttons.
- Spacing: project token scale (`var(--size-*)`): OpenProps fluid sizes when project uses OpenProps; else follow `design.md` spacing table.
