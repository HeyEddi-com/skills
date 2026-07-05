"""Post-agent quality checks: build, test, deps, visual."""
from __future__ import annotations

import json
import os
import re
import shutil
import socket
import subprocess
import time
from pathlib import Path

BACKEND = "backend"
PREVIEW_PORT = 4173
_active_preview_port: int | None = None

# Vitest can exit 0 while Vue logs unresolved components to stderr.
VITEST_VUE_WARNING_PATTERNS = (
    r"\[Vue warn\]: Failed to resolve component:",
    r"\[Vue warn\]: injection .+ not found",
)


def run_cmd(cmd: list[str], cwd: Path, timeout: int = 600) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"timeout after {timeout}s: {' '.join(cmd)}"
    output = ((proc.stdout or "") + (proc.stderr or "")).strip()
    return proc.returncode, output


def ensure_node_deps(root: Path) -> tuple[bool, str]:
    if not (root / "package.json").is_file():
        return True, "no package.json"
    if (root / "node_modules").is_dir():
        return True, "node_modules present"
    code, out = run_cmd(["npm", "install"], root, timeout=600)
    return code == 0, out[:500]


def npm_build(root: Path) -> tuple[bool, str]:
    if not (root / "package.json").is_file():
        return True, "skip: no package.json"
    pkg = json.loads((root / "package.json").read_text())
    if "build" not in pkg.get("scripts", {}):
        return False, "no build script"
    if str(pkg["scripts"]["build"]).strip().startswith("echo "):
        return False, "build script is stub"
    code, out = run_cmd(["npm", "run", "build"], root, timeout=600)
    return code == 0, out[-800:] if out else "ok"


def npm_test(root: Path) -> tuple[bool, str]:
    if not (root / "package.json").is_file():
        return True, "skip: no package.json"
    pkg = json.loads((root / "package.json").read_text())
    if "test" not in pkg.get("scripts", {}):
        return False, "no test script"
    if str(pkg["scripts"]["test"]).strip().startswith("echo "):
        return False, "test script is stub"
    code, out = run_cmd(["npm", "test"], root, timeout=300)
    if code != 0:
        return False, out[-800:] if out else "npm test failed"
    for pattern in VITEST_VUE_WARNING_PATTERNS:
        match = re.search(pattern, out)
        if match:
            line = match.group(0)
            return False, f"tests passed but Vue runtime warning: {line[:200]}"
    return True, out[-800:] if out else "ok"


def pytest_backend(root: Path) -> tuple[bool, str]:
    api = root / BACKEND
    if not (api / "tests").is_dir():
        return True, "skip: no backend tests"
    if shutil.which("poetry") and (api / "pyproject.toml").is_file():
        cmd = ["poetry", "run", "pytest", "-q"]
    else:
        cmd = ["python3", "-m", "pytest", "-q"]
    code, out = run_cmd(cmd, api, timeout=300)
    return code == 0, out[-800:] if out else "ok"


def audit_dependencies(root: Path, *, max_major_behind: int = 1) -> tuple[bool, str]:
    issues: list[str] = []
    warnings: list[str] = []

    pkg_path = root / "package.json"
    if not pkg_path.is_file():
        return True, "no frontend package.json"

    if not (root / "package-lock.json").is_file() and not (root / "pnpm-lock.yaml").is_file():
        issues.append("missing lockfile (package-lock.json or pnpm-lock.yaml)")

    if not (root / "node_modules").is_dir():
        issues.append("node_modules missing — run npm install")

    pkg = json.loads(pkg_path.read_text())
    for name, script in pkg.get("scripts", {}).items():
        if str(script).strip().startswith("echo "):
            issues.append(f"stub script: {name}")

    if shutil.which("npm") and (root / "node_modules").is_dir():
        code, out = run_cmd(["npm", "outdated", "--json"], root, timeout=120)
        if code == 0 and out.strip():
            try:
                outdated = json.loads(out)
                for dep, meta in outdated.items():
                    if isinstance(meta, dict) and meta.get("type") == "dependencies":
                        current = meta.get("current", "")
                        latest = meta.get("latest", "")
                        if _major_behind(current, latest) > max_major_behind:
                            warnings.append(f"{dep}: {current} → latest {latest}")
            except json.JSONDecodeError:
                pass

    api = root / BACKEND / "pyproject.toml"
    if api.is_file() and not shutil.which("poetry"):
        warnings.append("backend pyproject.toml but poetry not on PATH")

    if issues:
        return False, "FAIL: " + "; ".join(issues) + (
            (" | WARN: " + "; ".join(warnings[:5])) if warnings else ""
        )
    if warnings:
        return True, "WARN: " + "; ".join(warnings[:5])
    return True, "lockfile ok, deps installed, no stub scripts"


def _major_behind(current: str, latest: str) -> int:
    try:
        c = [int(x) for x in re.split(r"[.^]", current) if x.isdigit()]
        l = [int(x) for x in re.split(r"[.^]", latest) if x.isdigit()]
        if not c or not l:
            return 0
        return max(0, l[0] - c[0])
    except (ValueError, IndexError):
        return 0


def feature_test_exists(root: Path, vue_path: str) -> tuple[bool, str]:
    rel = Path(vue_path)
    stem = rel.stem
    parent = rel.parent
    candidates = [
        root / "tests" / "unit" / parent / f"{stem}.spec.ts",
        root / "tests" / "unit" / f"{stem}.spec.ts",
    ]
    for c in candidates:
        if c.is_file():
            return True, str(c.relative_to(root))
    return False, f"no test for {vue_path}"


def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _allocate_preview_port() -> int:
    env = os.environ.get("EVAL_PREVIEW_PORT", "").strip()
    if env:
        return int(env)
    for port in range(PREVIEW_PORT, PREVIEW_PORT + 10):
        if not _port_open(port):
            return port
    return PREVIEW_PORT


def preview_base_url() -> str:
    port = _active_preview_port or PREVIEW_PORT
    return f"http://127.0.0.1:{port}"


def _non_white_ratio(img) -> float:
    """Share of pixels that are not near-white (RGB all >= 245)."""
    pixels = list(img.convert("RGB").getdata())
    if not pixels:
        return 0.0
    non_white = sum(1 for p in pixels if any(c < 245 for c in p))
    return non_white / len(pixels)


def _preview_url(route: str) -> str:
    return preview_base_url().rstrip("/") + (route if route.startswith("/") else f"/{route}")


def _ensure_preview(root: Path) -> tuple[subprocess.Popen | None, str | None]:
    """Build and start preview if needed. Returns (proc, error)."""
    global _active_preview_port
    port = _allocate_preview_port()
    _active_preview_port = port
    proc: subprocess.Popen | None = None
    if _port_open(port):
        return proc, None
    code, out = run_cmd(["npm", "run", "build"], root, timeout=600)
    if code != 0:
        return None, f"build failed before preview: {out[-400:]}"
    proc = start_preview_server(root, port=port)
    if not _port_open(port):
        stop_preview_server(proc)
        return None, f"preview server did not start on port {port}"
    return proc, None


def start_preview_server(root: Path, *, port: int | None = None) -> subprocess.Popen | None:
    global _active_preview_port
    port = port if port is not None else _allocate_preview_port()
    _active_preview_port = port
    if _port_open(port):
        return None
    proc = subprocess.Popen(
        ["npm", "run", "preview", "--", "--host", "127.0.0.1", "--port", str(port)],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        if _port_open(port):
            return proc
        time.sleep(0.25)
    proc.kill()
    return None


def warn_busy_eval_ports(ports: tuple[int, ...] = (8090, 8085, 4173)) -> None:
    """Print a warning when stale dev servers may confuse the agent or harness."""
    busy = [p for p in ports if _port_open(p)]
    if not busy:
        return
    joined = ", ".join(str(p) for p in busy)
    print(
        f"  WARN: port(s) {joined} already in use on 127.0.0.1 — "
        "stop stale uvicorn/vite from other evals (`pkill -f 'uvicorn app.main'` or close terminals). "
        "Agent turns must not start backend servers.",
        flush=True,
    )


def stop_preview_server(proc: subprocess.Popen | None) -> None:
    if proc is None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def page_loads(
    root: Path,
    route: str,
    *,
    must_contain: list[str] | None = None,
    selectors: list[str] | None = None,
) -> tuple[bool, str]:
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        return True, "[skip] Playwright not installed"

    proc, err = _ensure_preview(root)
    if err:
        return False, err

    url = _preview_url(route)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            try:
                response = page.goto(url, wait_until="networkidle", timeout=20000)
                if response is None or response.status >= 400:
                    status = response.status if response else "no response"
                    return False, f"HTTP {status} for {url}"
                body = page.inner_text("body")
                for text in must_contain or []:
                    if text not in body:
                        return False, f"page missing text {text!r}"
                for sel in selectors or ["main", "h1"]:
                    loc = page.locator(sel).first
                    if loc.count() == 0:
                        return False, f"selector not found: {sel}"
                    box = loc.bounding_box()
                    if not box or box.get("width", 0) < 8 or box.get("height", 0) < 8:
                        return False, f"selector not visibly rendered: {sel}"
                return True, f"loaded {url}"
            finally:
                browser.close()
    except Exception as exc:
        return False, str(exc)
    finally:
        stop_preview_server(proc)


def ui_rendered(
    root: Path,
    route: str,
    *,
    primevue_selectors: list[str] | None = None,
    min_width: int = 120,
    min_height: int = 24,
) -> tuple[bool, str]:
    """Require styled PrimeVue components with real on-screen size (not unstyled HTML)."""
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
    except ImportError:
        return True, "[skip] Playwright not installed"

    proc, err = _ensure_preview(root)
    if err:
        return False, err

    selectors = primevue_selectors or [".p-card", ".p-button"]
    url = _preview_url(route)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            try:
                response = page.goto(url, wait_until="networkidle", timeout=20000)
                if response is None or response.status >= 400:
                    status = response.status if response else "no response"
                    return False, f"HTTP {status} for {url}"
                for sel in selectors:
                    loc = page.locator(sel).first
                    if loc.count() == 0:
                        return False, f"missing styled component: {sel}"
                    box = loc.bounding_box()
                    if not box:
                        return False, f"no layout box for {sel}"
                    w, h = box.get("width", 0), box.get("height", 0)
                    if w < min_width or h < min_height:
                        return False, f"{sel} too small ({w:.0f}x{h:.0f}px, need >={min_width}x{min_height})"
                h1 = page.locator("h1").first
                if h1.count():
                    size = h1.evaluate("el => parseFloat(getComputedStyle(el).fontSize)")
                    if size < 18:
                        return False, f"h1 font-size {size}px — styles likely not loaded"
                return True, f"styled UI visible at {url} ({', '.join(selectors)})"
            finally:
                browser.close()
    except Exception as exc:
        return False, str(exc)
    finally:
        stop_preview_server(proc)


def visual_similarity(
    root: Path,
    route: str,
    reference: Path,
    *,
    min_similarity: float = 0.15,
    min_content_ratio: float | None = None,
    ref_content_fraction: float = 0.35,
) -> tuple[bool, str]:
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
        from PIL import Image
        import io
    except ImportError:
        return True, "[skip] Playwright or Pillow not installed"

    if not reference.is_file():
        return True, f"[skip] no reference image: {reference}"

    proc, err = _ensure_preview(root)
    if err:
        return False, err

    url = _preview_url(route)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto(url, wait_until="networkidle", timeout=20000)
            png = page.screenshot(full_page=False)
            browser.close()

        shot = Image.open(io.BytesIO(png)).convert("RGB")
        ref = Image.open(reference).convert("RGB")
        ref = ref.resize(shot.size)

        shot_ratio = _non_white_ratio(shot)
        ref_ratio = _non_white_ratio(ref)
        required_ratio = (
            min_content_ratio
            if min_content_ratio is not None
            else max(0.008, ref_ratio * ref_content_fraction)
        )
        if shot_ratio < required_ratio:
            return False, (
                f"page too sparse: {shot_ratio:.2%} non-white pixels "
                f"(need >= {required_ratio:.2%}; handoff mockup {ref_ratio:.2%})"
            )

        ref_px = list(ref.getdata())
        shot_px = list(shot.getdata())
        if not ref_px:
            return False, "empty reference"
        diff = sum(
            abs(a - b) for p1, p2 in zip(ref_px, shot_px) for a, b in zip(p1, p2)
        )
        max_diff = len(ref_px) * 3 * 255
        similarity = 1.0 - (diff / max_diff)
        ok = similarity >= min_similarity
        return ok, (
            f"similarity={similarity:.2f} (min {min_similarity}), "
            f"content={shot_ratio:.2%} non-white"
        )
    except Exception as exc:
        return False, str(exc)
    finally:
        stop_preview_server(proc)


def screenshot_not_blank(root: Path, route: str) -> tuple[bool, str]:
    try:
        from playwright.sync_api import sync_playwright  # noqa: PLC0415
        from PIL import Image
        import io
    except ImportError:
        return True, "[skip] Playwright/Pillow not installed"

    proc, err = _ensure_preview(root)
    if err:
        return False, err

    url = _preview_url(route)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto(url, wait_until="networkidle", timeout=20000)
            png = page.screenshot()
            browser.close()
        img = Image.open(io.BytesIO(png)).convert("RGB")
        ratio = _non_white_ratio(img)
        if ratio < 0.008:
            return False, f"screenshot mostly blank ({ratio:.4%} non-white pixels)"
        return True, f"page rendered with content ({ratio:.2%} non-white pixels)"
    except Exception as exc:
        return False, str(exc)
    finally:
        stop_preview_server(proc)
