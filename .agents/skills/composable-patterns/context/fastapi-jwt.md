
# FastAPI JWT composable pattern

```ts
// useApi.ts — attach Bearer token, handle 401 refresh
export function useApi() {
  const auth = useAuthStore();
  async function fetchApi<T>(path: string, init?: RequestInit): Promise<T> {
    const res = await fetch(`/api${path}`, {
      ...init,
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
        "Content-Type": "application/json",
        ...init?.headers,
      },
    });
    if (res.status === 401) {
      await auth.refresh();
      return fetchApi(path, init);
    }
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  }
  return { fetchApi };
}
```
