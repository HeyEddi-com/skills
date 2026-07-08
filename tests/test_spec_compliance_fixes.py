"""Tests for spec-compliance fixes (verify_intake, verify_theme)."""
from __future__ import annotations

from pathlib import Path

from _skill_loader import load_skill_script


def test_verify_intake_allows_baseline_app_vue_only(tmp_path: Path) -> None:
    vi = load_skill_script("heyeddi-intake", "verify_intake")

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "App.vue").write_text("<template><router-view /></template>\n")
    assert vi._disallowed_vue(tmp_path) == []


def test_verify_intake_blocks_feature_views(tmp_path: Path) -> None:
    vi = load_skill_script("heyeddi-intake", "verify_intake")

    (tmp_path / "src" / "views").mkdir(parents=True)
    (tmp_path / "src" / "App.vue").write_text("<template><router-view /></template>\n")
    (tmp_path / "src" / "views" / "LoginView.vue").write_text("<template>login</template>\n")
    assert "src/views/LoginView.vue" in vi._disallowed_vue(tmp_path)


def test_verify_theme_rejects_raw_aura_with_brand(tmp_path: Path) -> None:
    vt = load_skill_script("heyeddi-handoff", "verify_theme")

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.ts").write_text(
        'import Aura from "@primevue/themes/aura";\n'
        "app.use(PrimeVue, { theme: { preset: Aura } });\n"
    )
    tokens = tmp_path / "src" / "styles" / "tokens.css"
    tokens.parent.mkdir(parents=True)
    tokens.write_text(
        ":root { color-scheme: light dark; --brand: var(--indigo-7); "
        "--p-primary-color: var(--brand); }\n"
        "@media (prefers-color-scheme: dark) { :root { --surface-1: #111; } }\n"
    )
    errors = vt.verify_theme(tmp_path, tokens)
    assert any("definePreset" in e for e in errors)


def test_verify_theme_accepts_define_preset(tmp_path: Path) -> None:
    vt = load_skill_script("heyeddi-handoff", "verify_theme")

    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.ts").write_text(
        "import { definePreset } from '@primeuix/themes';\n"
        'import Aura from "@primevue/themes/aura";\n'
        "const HeyEddiAura = definePreset(Aura, { semantic: { primary: { 500: '{indigo.500}' } } });\n"
        "app.use(PrimeVue, { theme: { preset: HeyEddiAura } });\n"
    )
    tokens = tmp_path / "src" / "styles" / "tokens.css"
    tokens.parent.mkdir(parents=True)
    tokens.write_text(
        ":root { color-scheme: light dark; --brand: var(--indigo-7); }\n"
        ".p-card { background: var(--surface-1); }\n"
        "@media (prefers-color-scheme: dark) { :root { --surface-1: #111; } }\n"
    )
    errors = vt.verify_theme(tmp_path, tokens)
    assert not any("definePreset" in e for e in errors)
