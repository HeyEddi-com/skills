# Mockup brief — Settings (TaskFlow Mobile)

Authored from `PRODUCT.md` intent — users need settings and a home screen. Material 3 Flutter handoff (no PNG mockups present).

## Audience (from product.md)

TaskFlow Mobile users who need to update profile details and notification preferences from an in-app settings screen.

## Designer read (first impression)

Calm in-app settings with clear hierarchy: drawer navigation, elevated cards on a low surface, generous 16dp card padding, and a primary save action outside the card stack.

## Layout topology

### Desktop / tablet
| Zone | Size / position | Behavior |
|------|-----------------|----------|
| Navigation drawer | 248dp width | Home + Settings destinations |
| App bar | full width | Route title |
| Main content | padded ListView | Card stack + save CTA |

### Mobile
| Zone | Behavior |
|------|----------|
| App bar | Title + hamburger opens drawer |
| Content | Full-width cards, 24dp page inset |
| Save CTA | Right-aligned FilledButton below cards |

## Region map

| Region | What the user sees | Build |
|--------|-------------------|-------|
| Drawer | Home + Settings nav | `NavigationDrawer` in `AppShell` |
| Profile card | Display name field | Material 3 `Card` + `TextField` |
| Notifications card | Email toggle | `Card` + `SwitchListTile` |
| Save CTA | Primary action | `FilledButton` "Save changes", right-aligned |

## Spacing & alignment (designer rules)

- Card internal padding: **16dp** (`EdgeInsets.all(16)`)
- Gap between cards: **16dp**
- Drawer width: **248dp** (`DrawerThemeData(width: 248)`)
- Save button **outside** card stack, not inside Profile card

## Implementation spec

| Component / region | Requirement | Target |
|--------------------|-------------|--------|
| Material theme | useMaterial3 CardTheme elevation 0 borderRadius 12 | lib/theme/app_theme.dart |
| Drawer width | drawer width 248 DrawerThemeData | lib/theme/app_theme.dart |
| App shell | NavigationDrawer Home Settings destinations | lib/widgets/app_shell.dart |
| Profile card | Card( EdgeInsets.all(16) Display name TextField | lib/screens/settings_screen.dart |
| Notifications card | Card( EdgeInsets SwitchListTile | lib/screens/settings_screen.dart |
| Save CTA | FilledButton Save changes | lib/screens/settings_screen.dart |

## Theme notes

- Seed brand color `Color(0xFF2563EB)` via `ColorScheme.fromSeed`
- Card: elevation 0, 12dp radius, surface container color
- Light and dark themes both configured

## Responsive

- Drawer overlays on narrow viewports; persistent layout optional on wide screens
- Content uses scrollable `ListView` with 24dp padding

_Source route: `/settings` · Feature folder: `.heyeddi/designs/settings/`_
