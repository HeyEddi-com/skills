#!/usr/bin/env python3
"""Verify theme coherence: semantic tokens + PrimeVue surface alignment."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from _skill_cli import emit, fail, resolve_project_root

TOKENS_DEFAULT = Path("src/styles/tokens.css")


def verify_theme(root: Path, tokens_path: Path) -> list[str]:
    errors: list[str] = []
    if not tokens_path.is_file():
        return [f"missing {tokens_path}"]

    text = tokens_path.read_text()

    if "light-dark(" not in text and "prefers-color-scheme" not in text:
        errors.append(
            "tokens.css must define light+dark semantic surfaces "
            "(light-dark() or @media prefers-color-scheme)"
        )

    if "color-scheme:" not in text:
        errors.append("tokens.css should set color-scheme on :root")

    circular = re.findall(r"(--[\w-]+)\s*:\s*var\(\1\)", text)
    if circular:
        errors.append(f"circular token aliases: {', '.join(sorted(set(circular)))}")

    main_ts = root / "src" / "main.ts"
    if main_ts.is_file():
        main = main_ts.read_text()
        if "PrimeVue" in main and "preset:" not in main:
            errors.append("main.ts: PrimeVue should use a theme preset")
        uses_define_preset = "definePreset" in main
        uses_raw_aura = bool(re.search(r"preset:\s*Aura\b", main))
        has_brand_token = bool(re.search(r"--brand\s*:", text))
        if has_brand_token and uses_raw_aura and not uses_define_preset:
            errors.append(
                "main.ts uses raw Aura preset while tokens.css defines --brand; "
                "use definePreset(Aura, { semantic: { primary: … } }) mapped to brand "
                "(see primevue-openprops-architect/context/VOCABULARY.md)"
            )
        if has_brand_token and "--p-primary-color" in text and not uses_define_preset:
            errors.append(
                "tokens.css --p-primary-color does not remap PrimeVue v4 Aura primary; "
                "wire brand via definePreset in main.ts"
            )
    else:
        errors.append("missing src/main.ts")

    vue_files = list((root / "src").rglob("*.vue")) if (root / "src").is_dir() else []
    has_primevue = any(
        "primevue" in p.read_text(errors="replace").lower() for p in vue_files[:40]
    )
    tokens_has_pv = ".p-card" in text or ".p-inputtext" in text
    if has_primevue and not tokens_has_pv:
        view_overrides = any(
            ":deep(.p-card)" in p.read_text(errors="replace")
            or ":deep(.p-inputtext)" in p.read_text(errors="replace")
            for p in vue_files
        )
        if not view_overrides:
            errors.append(
                "PrimeVue in use but no .p-card/.p-inputtext semantic overrides "
                "in tokens.css or :deep() in views: risk of dark/light mismatch"
            )

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify theme coherence")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--tokens-path", default=str(TOKENS_DEFAULT))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = resolve_project_root(args.project_root)
    tokens_path = root / args.tokens_path

    errors = verify_theme(root, tokens_path)
    if errors:
        msg = "Theme verification FAILED:\n" + "\n".join(f"- {e}" for e in errors)
        if args.check:
            fail(msg)
        emit(msg)
        return
    emit("Theme verification OK: semantic light/dark tokens and PrimeVue surfaces aligned.")


if __name__ == "__main__":
    main()
