You are running **primevue-openprops-architect**.

**Mandatory workflow (do not skip steps):**
1. Read `context/VOCABULARY.md` and `context/ANTI_PATTERNS.md` before editing.
2. Fix `src/components/BadPanel.vue` to comply with `DESIGN.md`:
   - Replace all hardcoded hex colors with OpenProps tokens.
   - Replace raw `16px` padding with `var(--size-3)` or similar token.
3. Run `python scripts/validate_vue.py --project-root .` and include full output in your summary.
4. Run `npm test` and `npm run build`; fix any issues before finishing.

Only edit BadPanel.vue unless imports are required.
