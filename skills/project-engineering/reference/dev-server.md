# Local dev server (Vite)

## Prerequisites

1. `audit_scaffold`: project has `dev` script and Vite config
2. `ensure_npm`: `node_modules` installed

## Run

```bash
cd <project-root>
npm run dev
```

Vite defaults to **http://localhost:5173** unless `vite.config.ts` sets `server.port`.

## After implementing a route

1. Register the route in `src/router/index.ts`
2. Start dev server (separate terminal: it runs until Ctrl+C)
3. Open e.g. `http://localhost:5173/settings`

## Production preview (optional)

```bash
npm run build
npm run preview
```

Use `dev_server_info` for all stacks: returns Vue, FastAPI (`:8090/docs` by default), and Firebase emulators (`:4000`) when present.

See also `reference/fastapi-backend.md` and `reference/firebase-backend.md`.
