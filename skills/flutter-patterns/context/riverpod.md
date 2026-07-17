
# Riverpod conventions

- `Provider` for repositories (singletons).
- `FutureProvider` / `StreamProvider` for one-shot or live data.
- `StateNotifierProvider` for form/edit state.
- Screens `ConsumerWidget` / `ConsumerStatefulWidget`: `ref.watch` in build, `ref.read` in callbacks.

Keep provider files small; one feature per file (`users_provider.dart`).
