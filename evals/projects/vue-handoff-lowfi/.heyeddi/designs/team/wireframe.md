# Wireframe — Team

Fidelity: **wireframe** (layout only). Colors from `.heyeddi/design.md` tokens.

## Desktop (ASCII)

```
+--sidebar------+-- main ----------------------------------------+
| SecureVault  | Topbar [ search............... ] [avatar A]     |
|   Dashboard  |                                                 |
| > Team *     |  Team                                           |
|   Settings   |  Manage members and roles.                      |
|              |  [ Invite member ]  (primary, top-right)        |
|              |  +---------------------------------------------+ |
|              |  | Name       | Email           | Role        | |
|              |  | Alex Rivera| alex@example.com| Admin       | |
|              |  | Sam Lee    | sam@example.com | Member      | |
|              |  +---------------------------------------------+ |
| [user chip]  |                                                 |
+--------------+-------------------------------------------------+
```

## Mobile

```
[≡] SecureVault                              [A]
Team
Manage members
[ Invite member ] full width
| Alex Rivera — Admin |
| Sam Lee — Member    |
```

## Regions

| Region | Component |
|--------|-----------|
| Member table | `DataTable` or Card list |
| Invite CTA | `Button` primary |
| Search | reuse top bar `InputText` |
