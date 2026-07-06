import type { User } from "@/types/api";

/** Offline demo roster when GET /api/users is unavailable (eval + local dev). */
export const DEMO_USERS: User[] = [
  { id: "u-001", email: "jordan@team.co" },
  { id: "u-002", email: "riley@team.co" },
  { id: "u-003", email: "alex@team.co" },
  { id: "u-004", email: "sam@team.co" },
];
