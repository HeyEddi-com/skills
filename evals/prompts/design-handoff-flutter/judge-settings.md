@design-handoff-flutter — Material 3 settings handoff (not Vue `@heyeddi-handoff`).

## Required (Flutter skill spec)

- `mockup-brief.md` with **Implementation spec** (Material widgets, dp spacing)
- `lib/theme/app_theme.dart`, `lib/widgets/app_shell.dart`, `lib/screens/settings_screen.dart`
- `verify_handoff --route /settings --phase full --check` passes
- `verify_tokens --check` and `verify_theme --check` pass

## Do NOT require (Vue-only)

- `.heyeddi/design.md` **Decision log** — Flutter handoff syncs layout via `describe_handoff --sync-design` only
- PrimeVue / `tokens.css` / Playwright captures (unless dev server was started)

## Pass when

Implementation matches mockup-brief spec and all three Flutter verify scripts pass. `flutter test` is optional when Flutter SDK is not on PATH.
