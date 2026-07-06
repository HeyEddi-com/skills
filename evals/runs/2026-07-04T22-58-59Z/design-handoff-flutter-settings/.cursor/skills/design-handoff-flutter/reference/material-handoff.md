# Material handoff — Flutter

## Shell

- `NavigationDrawer` or `Drawer` in `AppShell`
- `AppBar` title from route
- Body: padded `ListView` or `SingleChildScrollView`

## Settings pattern

```dart
Card(
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Profile', style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 12),
        TextField(decoration: InputDecoration(labelText: 'Display name')),
      ],
    ),
  ),
),
```

## Theme

- Seed color in `ColorScheme.fromSeed`
- Card: `elevation: 0`, `borderRadius: 12`
- Minimum card padding: **16dp**; gap between cards: **16dp**

## Visual QA

```bash
flutter run -d web-server --web-port=8085 --web-hostname=127.0.0.1
export FLUTTER_WEB_URL=http://127.0.0.1:8085
```

Then `@visual-auditor` on `/settings`.
