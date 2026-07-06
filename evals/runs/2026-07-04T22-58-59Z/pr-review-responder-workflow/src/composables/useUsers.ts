/** Eval fixture — pagination bug for PR review eval */
export interface User {
  id: string
  email: string
}

export async function fetchUsers(page = 1): Promise<User[]> {
  const res = await fetch(`/api/users?page=${page}`)
  if (!res.ok) throw new Error('fetch failed')
  return res.json()
}
