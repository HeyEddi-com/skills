"""Playwright screenshots + mockup comparison for agentic visual QA."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Reuse preview server + similarity from quality gate
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.lib.quality_gate import (  # noqa: E402
    _ensure_preview,
    _preview_url,
    stop_preview_server,
)


@dataclass
class VisualCaptureResult:
    ok: bool
    route: str
    artifacts: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    comparisons: list[dict] = field(default_factory=list)
    spacing_checks: list[dict] = field(default_factory=list)
    content_checks: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    skipped: bool = False

    def format_for_judge(self, sandbox: Path) -> str:
        lines = [
            "## Visual QA captures (Playwright)",
            "",
            f"Route: `{self.route}`",
            "",
        ]
        if self.skipped:
            lines.append("**SKIPPED** — Playwright/Pillow not available. This is a FAIL for design handoff turns.")
            return "\n".join(lines)

        if self.errors:
            lines.append("**Errors:**")
            for err in self.errors:
                lines.append(f"- {err}")
            lines.append("")

        if self.artifacts:
            lines.append("**Captured screenshots** (read these PNG files in the workspace — compare to references):")
            for path in self.artifacts:
                rel = Path(path)
                try:
                    rel = rel.relative_to(sandbox)
                except ValueError:
                    pass
                size = Path(path).stat().st_size if Path(path).is_file() else 0
                lines.append(f"- `{rel}` ({size} bytes)")
            lines.append("")

        if self.references:
            lines.append("**Reference mockups** (layout/hierarchy only — colors come from design.md, not PNG pixels):")
            for path in self.references:
                rel = Path(path)
                try:
                    rel = rel.relative_to(sandbox)
                except ValueError:
                    pass
                lines.append(f"- `{rel}`")
            lines.append("")
        else:
            lines.append(
                "**No reference mockups** (from-scratch design) — judge captures only. "
                "Fail unstyled UI, black inputs, empty/sparse pages."
            )
            lines.append("")

        if self.comparisons:
            lines.append(
                "**Automated pixel similarity** (coarse — high score does NOT mean good spacing; "
                "mostly white/gray layouts score ~0.9+ even when cramped):"
            )
            for row in self.comparisons:
                mark = "ok" if row.get("ok") else "LOW"
                lines.append(
                    f"- [{mark}] capture `{row.get('capture', '?')}` vs ref `{row.get('reference', '?')}`: "
                    f"{row.get('detail', '')}"
                )
            lines.append("")

        if self.spacing_checks:
            lines.append("**Rendered spacing checks** (computed CSS — AUTO-FAIL if any fail):")
            for row in self.spacing_checks:
                mark = "ok" if row.get("ok") else "FAIL"
                lines.append(
                    f"- [{mark}] {row.get('name')}: {row.get('value_px')}px (expect {row.get('expect')})"
                )
            lines.append("")

        if self.content_checks:
            lines.append("**Rendered content checks** (DOM — AUTO-FAIL if any fail):")
            for row in self.content_checks:
                mark = "ok" if row.get("ok") else "FAIL"
                detail = row.get("detail") or row.get("value_px")
                lines.append(
                    f"- [{mark}] {row.get('name')}: {detail} (expect {row.get('expect')})"
                )
            lines.append("")

        lines.extend([
            "**Your job:** Open the captured screenshots and reference mockups. Fail if:",
            "- No app shell when mockup shows sidebar/top bar (flat page on gray background)",
            "- Inputs look like solid black boxes or unstyled native fields",
            "- No card/panel layout / wrong region hierarchy vs mockups",
            "- Page is sparse, cramped in a corner, or missing key regions (Profile, Notifications, Save CTA)",
            "- **Empty PrimeVue Cards** — title/subtitle only with no fields, toggles, or stat values in card body",
            "- **Cramped spacing** — card body padding < 16px, card stack gap < 16px, or sidebar < 220px at desktop",
            "- Captures are missing or capture errors occurred",
            "",
            "**Do not fail** solely because primary button/toggle color differs from mockup PNG — judge colors against design.md tokens.",
            "",
        ])
        return "\n".join(lines)


def _resolve_reference(sandbox: Path, ref: str) -> Path | None:
    p = sandbox / ref
    if p.is_file():
        return p
    # Legacy fallbacks
    name = Path(ref).name
    for candidate in (
        sandbox / ".heyeddi" / "designs" / "settings" / name,
        sandbox / "designs" / "settings" / name,
        sandbox / ref.lstrip("/"),
    ):
        if candidate.is_file():
            return candidate
    return None


def _compare_png_files(capture: Path, reference: Path, *, min_similarity: float) -> tuple[bool, str]:
    try:
        from PIL import Image
    except ImportError:
        return False, "Pillow not installed"
    if not capture.is_file():
        return False, f"capture missing: {capture}"
    if not reference.is_file():
        return False, f"reference missing: {reference}"
    shot = Image.open(capture).convert("RGB")
    ref = Image.open(reference).convert("RGB")
    ref = ref.resize(shot.size)
    ref_px = list(ref.getdata())
    shot_px = list(shot.getdata())
    if not ref_px:
        return False, "empty reference"
    diff = sum(abs(a - b) for p1, p2 in zip(ref_px, shot_px) for a, b in zip(p1, p2))
    max_diff = len(ref_px) * 3 * 255
    similarity = 1.0 - (diff / max_diff)
    ok = similarity >= min_similarity
    return ok, f"similarity={similarity:.2f} (min {min_similarity})"


def _px(value: str | float | int) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return float(str(value).replace("px", "").strip() or 0)


def _measure_spacing(page, *, viewport_width: int) -> list[dict]:
    """Computed-style checks — catches broken token aliases that zero out padding/gap."""
    checks: list[dict] = []

    if viewport_width >= 768:
        sidebar = page.locator(".app-sidebar").first
        if sidebar.count():
            width = _px(sidebar.evaluate("el => getComputedStyle(el).width"))
            ok = 220 <= width <= 290
            checks.append(
                {
                    "name": "sidebar width @ desktop",
                    "ok": ok,
                    "value_px": round(width, 1),
                    "expect": "220–290px",
                }
            )

    cards = page.locator(".settings__cards").first
    if cards.count():
        gap = _px(
            cards.evaluate(
                "el => { const s = getComputedStyle(el); "
                "return parseFloat(s.gap || s.rowGap || '0'); }"
            )
        )
        ok = gap >= 16
        checks.append(
            {
                "name": "settings card stack gap",
                "ok": ok,
                "value_px": round(gap, 1),
                "expect": ">= 16px",
            }
        )

    body = page.locator(".p-card .p-card-body").first
    if body.count():
        pad = _px(body.evaluate("el => getComputedStyle(el).paddingTop"))
        ok = pad >= 16
        checks.append(
            {
                "name": "card body padding-top",
                "ok": ok,
                "value_px": round(pad, 1),
                "expect": ">= 16px",
            }
        )

    return checks


def _measure_content(page, *, route: str) -> list[dict]:
    """DOM presence checks — catches PrimeVue Card slot bugs and sparse pages."""
    checks: list[dict] = []
    slug = route.strip("/").split("/")[-1] or "home"

    if slug == "settings" or route.rstrip("/").endswith("settings"):
        root = page.locator(".settings").first
        if not root.count():
            checks.append(
                {
                    "name": "settings root region",
                    "ok": False,
                    "detail": "missing .settings",
                    "expect": ".settings container",
                }
            )
            return checks

        inputs = root.locator("input.p-inputtext, .p-inputtext input, .p-inputtext")
        input_count = inputs.count()
        checks.append(
            {
                "name": "settings form inputs",
                "ok": input_count >= 2,
                "detail": f"{input_count} visible",
                "expect": ">= 2 (Display name + Email)",
            }
        )

        toggles = root.locator(".p-toggleswitch, [role='switch']")
        toggle_count = toggles.count()
        checks.append(
            {
                "name": "settings notification toggle",
                "ok": toggle_count >= 1,
                "detail": f"{toggle_count} visible",
                "expect": ">= 1 ToggleSwitch",
            }
        )

        save = root.locator(".settings__save .p-button, button:has-text('Save')")
        checks.append(
            {
                "name": "settings save CTA",
                "ok": save.count() >= 1,
                "detail": f"{save.count()} visible",
                "expect": "Save changes button",
            }
        )

    elif slug == "dashboard":
        root = page.locator(".dashboard").first
        if not root.count():
            root = page.locator("main, .app-main, [class*='dashboard']").first
        if not root.count():
            return checks

        stat_values = root.locator(".dashboard__stat-value")
        stat_count = stat_values.count()
        rows = root.locator(".p-datatable-tbody tr, table tbody tr, .dashboard__table tr")
        row_count = rows.count()
        has_table = (
            root.locator(".dashboard__table, .p-datatable, table").count() >= 1 or row_count >= 1
        )

        # TaskFlow / integration: user roster table + optional 1–2 summary stats.
        if has_table and row_count >= 1:
            checks.append(
                {
                    "name": "dashboard user table",
                    "ok": True,
                    "detail": f"{row_count} rows",
                    "expect": ">= 1 DataTable row (team roster dashboard)",
                }
            )
            if stat_count >= 1:
                checks.append(
                    {
                        "name": "dashboard summary stats",
                        "ok": stat_count >= 1,
                        "detail": f"{stat_count} visible",
                        "expect": ">= 1 summary stat (roster dashboard; 3 only for KPI wireframes)",
                    }
                )
        elif stat_count >= 1:
            # Wireframe / KPI grid: three stat tiles without a roster table.
            checks.append(
                {
                    "name": "dashboard stat values",
                    "ok": stat_count >= 3,
                    "detail": f"{stat_count} visible",
                    "expect": ">= 3 KPI stat cards (wireframe dashboard)",
                }
            )
            if row_count >= 1:
                checks.append(
                    {
                        "name": "dashboard activity rows",
                        "ok": row_count >= 1,
                        "detail": f"{row_count} rows",
                        "expect": ">= 1 DataTable row",
                    }
                )

        cta = root.locator(".dashboard__cta .p-button, .dashboard__cta button")
        if cta.count() or root.locator(".dashboard__cta").count():
            checks.append(
                {
                    "name": "dashboard primary CTA",
                    "ok": cta.count() >= 1,
                    "detail": f"{cta.count()} visible",
                    "expect": "New task button",
                }
            )

        if not checks:
            has_heading = root.locator("h1, h2").count() >= 1
            has_body = len(root.inner_text().strip()) > 40
            checks.append(
                {
                    "name": "dashboard page content",
                    "ok": has_heading and has_body,
                    "detail": f"heading={has_heading}, body_chars={len(root.inner_text().strip())}",
                    "expect": "title + substantive main content",
                }
            )
            if row_count >= 1:
                checks.append(
                    {
                        "name": "dashboard table rows",
                        "ok": True,
                        "detail": f"{row_count} rows",
                        "expect": ">= 1 row",
                    }
                )

    elif slug == "team":
        root = page.locator(".team, .team-view, [class*='team']").first
        if root.count():
            members = root.locator(
                ".team__member, .p-datatable-tbody tr, .p-avatar, [class*='member']"
            )
            member_count = members.count()
            checks.append(
                {
                    "name": "team member rows",
                    "ok": member_count >= 1,
                    "detail": f"{member_count} visible",
                    "expect": ">= 1 member row or avatar",
                }
            )

    return checks


def append_process_manifest(
    sandbox: Path,
    *,
    step_name: str,
    turn_index: int,
    routes: list[str],
    results: list["VisualCaptureResult"],
) -> None:
    """Append turn capture metadata to `.heyeddi/audits/eval-process/manifest.json`."""
    process_dir = sandbox / ".heyeddi" / "audits" / "eval-process"
    process_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = process_dir / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = {"turns": []}
    else:
        manifest = {"turns": []}

    entry = {
        "turn_index": turn_index,
        "step": step_name,
        "routes": routes,
        "capture_dir": f".heyeddi/audits/eval-process/{step_name}",
        "artifacts": [],
        "ok": all(r.ok for r in results),
    }
    for result in results:
        for art in result.artifacts:
            try:
                entry["artifacts"].append(str(Path(art).relative_to(sandbox)))
            except ValueError:
                entry["artifacts"].append(art)
    manifest["turns"] = [t for t in manifest.get("turns", []) if t.get("step") != step_name]
    manifest["turns"].append(entry)
    manifest["turns"].sort(key=lambda row: row.get("turn_index", 0))
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def run_visual_audit(
    sandbox: Path,
    *,
    route: str,
    widths: list[int] | None = None,
    references: list[str] | None = None,
    min_similarity: float = 0.12,
    color_schemes: list[str] | None = None,
    step_name: str | None = None,
) -> VisualCaptureResult:
    """Build, preview, screenshot route at widths; compare to reference PNGs."""
    widths = widths or [375, 768, 1440]
    if step_name:
        out_dir = sandbox / ".heyeddi" / "audits" / "eval-process" / step_name
    else:
        out_dir = sandbox / ".heyeddi" / "audits" / "eval-capture"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        return VisualCaptureResult(
            ok=False,
            route=route,
            skipped=True,
            errors=["Playwright not installed — run ./scripts/setup-evals.sh"],
        )

    proc, err = _ensure_preview(sandbox)
    if err:
        return VisualCaptureResult(ok=False, route=route, errors=[err])

    artifacts: list[str] = []
    errors: list[str] = []
    spacing_checks: list[dict] = []
    content_checks: list[dict] = []
    url = _preview_url(route)
    slug = route.strip("/").replace("/", "_") or "home"
    schemes = color_schemes or ["light"]

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for w in widths:
                page = browser.new_page(viewport={"width": w, "height": 900})
                try:
                    page.emulate_media(color_scheme="light")
                    page.goto(url, wait_until="networkidle", timeout=25000)
                except Exception as exc:
                    errors.append(f"navigation failed {url} @ {w}px: {exc}")
                    page.close()
                    continue
                dest = out_dir / f"{slug}_{w}px.png"
                page.screenshot(path=str(dest), full_page=True)
                artifacts.append(str(dest))
                if w >= 768:
                    spacing_checks.extend(_measure_spacing(page, viewport_width=w))
                    content_checks.extend(_measure_content(page, route=route))
                page.close()

            # Dark-mode sanity at desktop width (theme coherence)
            if "dark" in schemes:
                dark_width = 1440 if 1440 in widths else max(widths)
                page = browser.new_page(viewport={"width": dark_width, "height": 900})
                try:
                    page.emulate_media(color_scheme="dark")
                    page.goto(url, wait_until="networkidle", timeout=25000)
                    dest = out_dir / f"{slug}_{dark_width}px_dark.png"
                    page.screenshot(path=str(dest), full_page=True)
                    artifacts.append(str(dest))
                    # Spot-check readable surfaces in dark mode
                    card_bg = page.locator(".p-card").first
                    if card_bg.count():
                        bg = card_bg.evaluate(
                            "el => getComputedStyle(el).backgroundColor"
                        )
                        checks_dark = _measure_content(page, route=route)
                        for row in checks_dark:
                            row = dict(row)
                            row["name"] = f"{row['name']} @ dark"
                            content_checks.append(row)
                        content_checks.append(
                            {
                                "name": "dark mode card surface",
                                "ok": bg not in ("rgba(0, 0, 0, 0)", "transparent"),
                                "detail": bg,
                                "expect": "non-transparent card background",
                            }
                        )
                except Exception as exc:
                    errors.append(f"dark capture failed {url}: {exc}")
                finally:
                    page.close()

            browser.close()
    except Exception as exc:
        errors.append(str(exc))
    finally:
        stop_preview_server(proc)

    if not artifacts:
        errors.append("no screenshots captured")
        return VisualCaptureResult(
            ok=False,
            route=route,
            artifacts=artifacts,
            errors=errors,
        )

    ref_paths: list[str] = []
    comparisons: list[dict] = []
    for ref_spec in references or []:
        ref_path = _resolve_reference(sandbox, ref_spec)
        if not ref_path:
            errors.append(f"reference not found: {ref_spec}")
            continue
        ref_paths.append(str(ref_path))
        # Compare widest capture to desktop ref, narrowest to mobile ref
        if "mobile" in ref_spec.lower():
            cap = out_dir / f"{slug}_375px.png"
        else:
            cap = out_dir / f"{slug}_1440px.png"
        if not cap.is_file():
            cap = Path(artifacts[-1])
        ok, detail = _compare_png_files(cap, ref_path, min_similarity=min_similarity)
        comparisons.append({
            "capture": str(cap.relative_to(sandbox)),
            "reference": str(ref_path.relative_to(sandbox)),
            "ok": ok,
            "detail": detail,
        })

    # Mirror captures to skill screenshot dir under .heyeddi/
    skill_shots = sandbox / ".heyeddi" / "audits" / "visual" / "screenshots"
    skill_shots.mkdir(parents=True, exist_ok=True)
    manifest = {"route": route, "artifacts": []}
    for art in artifacts:
        dest = skill_shots / Path(art).name
        try:
            dest.write_bytes(Path(art).read_bytes())
            manifest["artifacts"].append(str(dest.relative_to(sandbox)))
        except OSError:
            pass
    (skill_shots / "last-capture.json").write_text(json.dumps(manifest, indent=2) + "\n")

    capture_ok = bool(artifacts) and not errors
    spacing_ok = not spacing_checks or all(row.get("ok") for row in spacing_checks)
    content_ok = not content_checks or all(row.get("ok") for row in content_checks)
    return VisualCaptureResult(
        ok=capture_ok and spacing_ok and content_ok,
        route=route,
        artifacts=artifacts,
        references=ref_paths,
        comparisons=comparisons,
        spacing_checks=spacing_checks,
        content_checks=content_checks,
        errors=errors,
    )
