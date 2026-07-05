@design-handoff-flutter

Implement `/settings` from `.heyeddi/designs/settings/` mockups (if present) or from product.md intent.

Follow two-pass workflow:
1. Write `mockup-brief.md` with Implementation spec (Material 3 Card, drawer width, save CTA)
2. Ensure `lib/theme/app_theme.dart`, `app_shell.dart`, and `settings_screen.dart` match spec
3. Run `verify_handoff --phase full --check`, `verify_tokens --check`, `verify_theme --check`

Use `flutter test` if tests exist. Do not start dev servers.
