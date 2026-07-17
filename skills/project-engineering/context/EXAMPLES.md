# Examples: Project engineering

## Thin eval project

```
@project-engineering
audit_scaffold → scaffold_vue → ensure_npm → dev_server_info
@heyeddi-handoff implement /settings
write_test_stub for src/views/SettingsView.vue
run_tests
# Human: npm run dev → http://localhost:5173/settings
```

## Existing app missing tests

```
audit_scaffold
write_test_stub --path src/views/LoginView.vue
npm test
```
