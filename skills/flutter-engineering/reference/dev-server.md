# Dev server: Flutter

**Web (visual audit / QA):**

```bash
flutter run -d web-server --web-port=8085 --web-hostname=127.0.0.1
```

Export for Playwright:

```bash
export FLUTTER_WEB_URL=http://127.0.0.1:8085
```

**Mobile:**

```bash
flutter devices
flutter run -d <device-id>
```

Run `dev_server_info` for project-specific ports from `.heyeddi/stack.json`.
