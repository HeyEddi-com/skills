# Firebase backend (HeyEddi)

## Layout

```
firebase.json
.firebaserc
firestore.rules
firestore.indexes.json
.env.firebase.example   → copy values to .env.local
```

## Setup

```bash
scaffold_stack --stack firebase
npm i -g firebase-tools   # once
firebase login
```

Copy Firebase web config from console into `.env.local` (see `.env.firebase.example`).

## Run emulators locally

```bash
firebase emulators:start
```

- Emulator UI: http://localhost:4000
- Firestore: port 8080
- Auth: port 9099

Vue app uses `VITE_FIREBASE_*` env vars. Run `npm run dev` in a second terminal.

## Client patterns

Use `@composable-patterns` → `context/firebase-client.md` for composables.

## Schema hints

`@backend-type-bridger` → `fetch_firestore_schema`
