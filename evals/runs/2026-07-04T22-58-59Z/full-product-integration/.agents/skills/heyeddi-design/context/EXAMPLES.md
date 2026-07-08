
# Examples — HeyEddi design

## Vague brief (no sub-command)

```
I want an enterprise view for our admin app
```

Agent runs **discover** → asks about users, density, nav, data → **shape** pipeline.

## Full shape flow

```
@heyeddi-design shape
Feature: enterprise-settings
Brief: B2B admin settings — org profile, members, billing, danger zone
```

Produces `designs/enterprise-settings/research.md`, wireframes, `brief.md` — waits for confirmation.

## Build after confirmation

```
@heyeddi-design craft enterprise-settings
Route: /settings
```

## Greenfield project

```
@heyeddi-design init
```

Then `document` → `shape` → `craft`.

## Critique only

```
@heyeddi-design critique the login page
```

Or plain language: *"this login screen looks terrible — what's wrong?"*

Writes `.heyeddi/docs/login-critique.md` — no code unless you ask to fix.

## Critique then polish

```
@heyeddi-design polish /login
```

Runs **critique** first if needed, then fixes P0/P1 issues.

## Polish only

```
@heyeddi-design polish
Route: /settings — tighten mobile spacing
```

## Wrong skill (has mockups)

```
@heyeddi-handoff
Route: /settings
Attachments: desktop.png, mobile.png
```
