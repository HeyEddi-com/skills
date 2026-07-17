
# Examples: Build verification

## Typical failure: unresolved import

```
[exit 1]
Could not resolve "./MissingComponent.vue" from src/views/Settings.vue
```

Fix: correct the import path or add the missing file, then re-run verify_build.

## Success

```
vite v5.4.0 building for production...
✓ built in 4.2s
```
