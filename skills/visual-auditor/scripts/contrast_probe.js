/**
 * In-page WCAG contrast + motion-over-text probe.
 * Invoked via Playwright page.evaluate: returns violation list.
 */
function runContrastProbe() {
  function parseCssColor(value) {
    if (!value || value === "transparent" || value === "none") return null;
    const m = value.match(/rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)(?:\s*,\s*([\d.]+))?\s*\)/i);
    if (m) {
      return { r: +m[1], g: +m[2], b: +m[3], a: m[4] !== undefined ? +m[4] : 1 };
    }
    if (value[0] === "#") {
      let h = value.slice(1);
      if (h.length === 3) h = h.split("").map((c) => c + c).join("");
      if (h.length === 6) {
        return { r: parseInt(h.slice(0, 2), 16), g: parseInt(h.slice(2, 4), 16), b: parseInt(h.slice(4, 6), 16), a: 1 };
      }
    }
    return null;
  }

  function relativeLuminance(c) {
    function ch(v) {
      v = v / 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    }
    return 0.2126 * ch(c.r) + 0.7152 * ch(c.g) + 0.0722 * ch(c.b);
  }

  function contrastRatio(fg, bg) {
    const l1 = relativeLuminance(fg);
    const l2 = relativeLuminance(bg);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  function rgbToHsl(c) {
    const r = c.r / 255;
    const g = c.g / 255;
    const b = c.b / 255;
    const mx = Math.max(r, g, b);
    const mn = Math.min(r, g, b);
    const l = (mx + mn) / 2;
    if (mx === mn) return { h: 0, s: 0, l };
    const d = mx - mn;
    const s = l > 0.5 ? d / (2 - mx - mn) : d / (mx + mn);
    let h;
    if (mx === r) h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
    else if (mx === g) h = ((b - r) / d + 2) / 6;
    else h = ((r - g) / d + 4) / 6;
    return { h: h * 360, s, l };
  }

  function hueDistance(a, b) {
    const d = Math.abs(a - b) % 360;
    return Math.min(d, 360 - d);
  }

  function compositeOver(fg, bg) {
    const a = fg.a + bg.a * (1 - fg.a);
    if (a <= 0) return { r: 0, g: 0, b: 0, a: 0 };
    return {
      r: (fg.r * fg.a + bg.r * bg.a * (1 - fg.a)) / a,
      g: (fg.g * fg.a + bg.g * bg.a * (1 - fg.a)) / a,
      b: (fg.b * fg.a + bg.b * bg.a * (1 - fg.a)) / a,
      a,
    };
  }

  function parseWeight(w) {
    if (!w) return 400;
    if (w === "bold" || w === "bolder") return 700;
    const n = parseInt(w, 10);
    return Number.isFinite(n) ? n : 400;
  }

  function isLargeText(fontSizePx, fontWeight) {
    return fontSizePx >= 18 || (fontSizePx >= 14 && parseWeight(fontWeight) >= 700);
  }

  function requiredRatio(fontSizePx, fontWeight) {
    return isLargeText(fontSizePx, fontWeight) ? 3.0 : 4.5;
  }

  function isVisible(el) {
    const rect = el.getBoundingClientRect();
    if (rect.width < 1 || rect.height < 1) return false;
    const style = getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden") return false;
    if (parseFloat(style.opacity) < 0.08) return false;
    return true;
  }

  function motionRiskFrom(el) {
    let node = el;
    const risks = [];
    while (node && node !== document.documentElement) {
      const s = getComputedStyle(node);
      if (s.animationName && s.animationName !== "none") {
        const dur = parseFloat(s.animationDuration) || 0;
        if (dur > 0) risks.push({ type: "animation", selector: selectorFor(node), detail: s.animationName });
      }
      if (s.backgroundImage && s.backgroundImage !== "none") {
        risks.push({ type: "background-image", selector: selectorFor(node), detail: s.backgroundImage.slice(0, 80) });
      }
      if (node.tagName === "VIDEO" || node.tagName === "CANVAS") {
        risks.push({ type: node.tagName.toLowerCase(), selector: selectorFor(node) });
      }
      node = node.parentElement;
    }
    return risks;
  }

  function selectorFor(el) {
    if (el.id) return "#" + el.id;
    const tag = el.tagName.toLowerCase();
    const cls = (el.className && typeof el.className === "string") ? el.className.trim().split(/\s+/).slice(0, 2).join(".") : "";
    return cls ? tag + "." + cls : tag;
  }

  function effectiveBackground(el) {
    let node = el.parentElement;
    let composite = null;
    let imageBehind = false;
    while (node && node !== document.documentElement) {
      const s = getComputedStyle(node);
      if (s.backgroundImage && s.backgroundImage !== "none") imageBehind = true;
      const c = parseCssColor(s.backgroundColor);
      if (c && c.a > 0.02) {
        composite = composite ? compositeOver(c, composite) : c;
        if (composite.a >= 0.92) break;
      }
      node = node.parentElement;
    }
    if (!composite || composite.a < 0.5) {
      const bodyBg = parseCssColor(getComputedStyle(document.body).backgroundColor);
      const htmlBg = parseCssColor(getComputedStyle(document.documentElement).backgroundColor);
      const fallback = bodyBg || htmlBg || { r: 255, g: 255, b: 255, a: 1 };
      composite = composite ? compositeOver(composite, fallback) : fallback;
    }
    return { color: composite, imageBehind };
  }

  function effectiveForeground(el) {
    const s = getComputedStyle(el);
    let fg = parseCssColor(s.color);
    if (!fg) return null;
    let node = el;
    let opacity = 1;
    while (node && node !== document.documentElement) {
      const st = getComputedStyle(node);
      opacity *= parseFloat(st.opacity) || 1;
      node = node.parentElement;
    }
    if (opacity < 1) fg = { ...fg, a: fg.a * opacity };
    return fg;
  }

  function directText(el) {
    return Array.from(el.childNodes)
      .filter((n) => n.nodeType === Node.TEXT_NODE)
      .map((n) => (n.textContent || "").trim())
      .join(" ")
      .trim();
  }

  function textElements() {
    const seen = new Set();
    const out = [];
    document.querySelectorAll("body *").forEach((el) => {
      if (!isVisible(el)) return;
      const text = directText(el);
      if (text.length < 2) return;
      if (seen.has(el)) return;
      seen.add(el);
      out.push({ el, text: text.slice(0, 120) });
    });
    return out;
  }

  const violations = [];
  let scanned = 0;

  for (const { el, text } of textElements()) {
    scanned += 1;
    const style = getComputedStyle(el);
    const fontSize = parseFloat(style.fontSize) || 16;
    const fontWeight = style.fontWeight;
    const fg = effectiveForeground(el);
    if (!fg) continue;
    const { color: bg, imageBehind } = effectiveBackground(el);
    const ratio = contrastRatio(fg, bg);
    const need = requiredRatio(fontSize, fontWeight);
    const sel = selectorFor(el);
    const motion = motionRiskFrom(el);

    const fgHsl = rgbToHsl(fg);
    const bgHsl = rgbToHsl(bg);
    const sameHue =
      fgHsl.s > 0.15 &&
      bgHsl.s > 0.15 &&
      hueDistance(fgHsl.h, bgHsl.h) < 18 &&
      ratio < need;

    if (ratio < need) {
      violations.push({
        severity: "error",
        code: sameHue ? "same-hue-low-contrast" : "low-contrast",
        selector: sel,
        text,
        ratio: Math.floor(ratio * 100) / 100,
        required: need,
        foreground: `rgb(${Math.round(fg.r)},${Math.round(fg.g)},${Math.round(fg.b)})`,
        background: `rgb(${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)})`,
        fontSizePx: fontSize,
        fontWeight,
      });
    } else if (ratio < need + 1.0 && (imageBehind || motion.length)) {
      violations.push({
        severity: "warn",
        code: "motion-or-image-behind-text",
        selector: sel,
        text,
        ratio: Math.floor(ratio * 100) / 100,
        required: need,
        motion,
        note: "Text may be illegible when background moves or shifts",
      });
    } else if (imageBehind && motion.length && ratio < 7) {
      violations.push({
        severity: "warn",
        code: "text-over-dynamic-background",
        selector: sel,
        text,
        ratio: Math.floor(ratio * 100) / 100,
        motion,
      });
    }

    if (parseFloat(style.opacity) < 0.85 && ratio < 7 && (imageBehind || motion.length)) {
      violations.push({
        severity: "warn",
        code: "faded-text-over-busy-background",
        selector: sel,
        text,
        ratio: Math.floor(ratio * 100) / 100,
        opacity: parseFloat(style.opacity),
        motion,
      });
    }
  }

  return {
    scanned,
    violationCount: violations.length,
    errorCount: violations.filter((v) => v.severity === "error").length,
    warnCount: violations.filter((v) => v.severity === "warn").length,
    violations,
  };
}
