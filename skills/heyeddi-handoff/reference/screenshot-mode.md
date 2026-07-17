# Screenshot mode (v1)

Read **`reference/mockup-contract.md`**, **`reference/interpret-mockups.md`**, and **`reference/handoff-to-code.md`**.

## Workflow

1. Designer places PNGs in `.heyeddi/designs/<feature>/`.
2. `load_handoff.py`: check `interpret_required`.
3. **Designer pass**: `mockup-brief.md` with region map + **Implementation spec** (measurable tokens/CSS).
4. `describe_handoff.py --sync-design`.
5. **Implementer pass**: tokens → shell → `verify_handoff --phase shell` → route → `verify_handoff --phase full`.
6. Wire PrimeVue theme; append Decision log.

## Region checklist (before calling done)

- [ ] Brief has **Implementation spec** table
- [ ] `verify_handoff.py --check` passes
- [ ] Sidebar: `brand-subtle` active pill, user `margin-top: auto`, width token
- [ ] Cards: explicit padding/gap (not PrimeVue defaults only)
- [ ] Save CTA outside cards per spec
