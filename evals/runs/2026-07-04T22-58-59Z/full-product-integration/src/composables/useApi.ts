/**
 * Shared fetch wrapper for the FastAPI backend.
 *
 * Vite dev server proxies `/api` → `http://127.0.0.1:8090` (see `.heyeddi/stack.json`).
 * Pass paths relative to `/api` (e.g. `fetchApi("/users")` → `GET /api/users`).
 *
 * JWT Bearer attachment is deferred until auth endpoints exist; see
 * `@composable-patterns` → `context/fastapi-jwt.md` for the refresh pattern.
 */
export function useApi() {
  async function fetchApi<T>(path: string, init?: RequestInit): Promise<T> {
    const normalized = path.startsWith("/") ? path : `/${path}`;
    const res = await fetch(`/api${normalized}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...init?.headers,
      },
    });
    if (!res.ok) {
      throw new Error(await res.text());
    }
    return res.json() as Promise<T>;
  }

  return { fetchApi };
}
