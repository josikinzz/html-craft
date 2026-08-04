#!/usr/bin/env python3
"""
Contrast checker for html-craft pages.

Parses a generated self-contained HTML file, resolves its CSS custom properties
for each theme block it defines, and reports text/background pairs that fall
below their WCAG floor — plus two failure modes that contrast math alone misses:
light ink committed on top of a bright accent fill, and background line patterns
strong enough to cut through text.

Usage:
    python3 check-contrast.py page.html
    python3 check-contrast.py page.html --quiet     # only FAIL rows
    python3 check-contrast.py page.html --strict    # exit 1 on WARN too

Exit status is 1 when any FAIL is found, so it can gate a delivery step.
"""

import argparse
import os
import re
import sys

# ---------------------------------------------------------------- color math

NAMED = {
    'white': (255, 255, 255), 'black': (0, 0, 0), 'transparent': None,
    'red': (255, 0, 0), 'green': (0, 128, 0), 'blue': (0, 0, 255),
    'gray': (128, 128, 128), 'grey': (128, 128, 128),
}


def parse_color(value, resolve=None, _depth=0):
    """Return (r, g, b, a) or None if the value isn't a resolvable color."""
    if value is None or _depth > 12:
        return None
    v = value.strip().lower().rstrip(';').strip()
    if not v:
        return None

    # var(--x, fallback) — follow the chain
    m = re.match(r'^var\(\s*(--[\w-]+)\s*(?:,\s*(.+))?\)$', v)
    if m:
        name, fallback = m.group(1), m.group(2)
        if resolve and name in resolve:
            got = parse_color(resolve[name], resolve, _depth + 1)
            if got:
                return got
        return parse_color(fallback, resolve, _depth + 1) if fallback else None

    # color-mix(in srgb, A p%, B) — approximate by linear blend in sRGB
    m = re.match(r'^color-mix\(\s*in\s+[\w-]+\s*,\s*(.+)\)$', v)
    if m:
        return _parse_color_mix(m.group(1), resolve, _depth)

    if v in NAMED:
        rgb = NAMED[v]
        return None if rgb is None else (*rgb, 1.0)

    m = re.match(r'^#([0-9a-f]{3,8})$', v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        elif len(h) == 4:
            h = ''.join(c * 2 for c in h)
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
        if len(h) == 8:
            return (int(h[0:2], 16), int(h[2:4], 16),
                    int(h[4:6], 16), int(h[6:8], 16) / 255)
        return None

    m = re.match(r'^rgba?\(([^)]+)\)$', v)
    if m:
        parts = [p.strip() for p in re.split(r'[,\s/]+', m.group(1)) if p.strip()]
        try:
            nums = []
            for p in parts[:3]:
                nums.append(int(round(float(p[:-1]) * 255 / 100)) if p.endswith('%')
                            else int(round(float(p))))
            a = 1.0
            if len(parts) > 3:
                a = float(parts[3][:-1]) / 100 if parts[3].endswith('%') else float(parts[3])
            return (*nums, a)
        except ValueError:
            return None
    return None


def _parse_color_mix(body, resolve, depth):
    """Handle the 'A 30%, B' body of a color-mix() call."""
    parts, depth_paren, cur = [], 0, ''
    for ch in body:
        if ch == '(':
            depth_paren += 1
        elif ch == ')':
            depth_paren -= 1
        if ch == ',' and depth_paren == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    parts.append(cur)
    if len(parts) < 2:
        return None

    def split_pct(s):
        s = s.strip()
        m = re.match(r'^(.*?)\s+([\d.]+)%$', s)
        return (m.group(1), float(m.group(2)) / 100) if m else (s, None)

    c1, p1 = split_pct(parts[0])
    c2, p2 = split_pct(parts[1])
    a = parse_color(c1, resolve, depth + 1)
    b = parse_color(c2, resolve, depth + 1)
    if not a or not b:
        return None
    if p1 is None and p2 is None:
        p1 = p2 = 0.5
    elif p1 is None:
        p1 = 1 - p2
    elif p2 is None:
        p2 = 1 - p1
    total = p1 + p2 or 1
    p1, p2 = p1 / total, p2 / total
    return tuple(a[i] * p1 + b[i] * p2 for i in range(4))


def flatten(fg, bg):
    """Composite a possibly-translucent color over an opaque backdrop."""
    if fg is None:
        return None
    a = fg[3]
    if a >= 0.999:
        return fg[:3]
    if bg is None:
        return None
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3))


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = rgb[:3]
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(fg, bg):
    if fg is None or bg is None:
        return None
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def to_hex(rgb):
    if rgb is None:
        return '?'
    return '#%02x%02x%02x' % tuple(int(round(max(0, min(255, c)))) for c in rgb[:3])

# ---------------------------------------------------------------- extraction


def extract_styles(html):
    return '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S | re.I))


def strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)


def _strip_at_blocks(css):
    """Remove @media/@supports blocks (and their contents) via brace matching."""
    out, i, n = [], 0, len(css)
    while i < n:
        if css[i] == '@':
            m = re.match(r'@(media|supports|container)\b', css[i:])
            if m:
                j = css.find('{', i)
                if j == -1:
                    break
                depth = 0
                while j < n:
                    if css[j] == '{':
                        depth += 1
                    elif css[j] == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                i = j + 1
                continue
        out.append(css[i])
        i += 1
    return ''.join(out)


def _at_block_bodies(css, keyword_re):
    """Yield the full body of each @media block whose prelude matches."""
    for m in re.finditer(r'@media([^{]*)\{', css):
        if not re.search(keyword_re, m.group(1), re.I):
            continue
        j, depth = m.end() - 1, 0
        while j < len(css):
            if css[j] == '{':
                depth += 1
            elif css[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        yield css[m.end():j]


def theme_blocks(css):
    """
    Return {theme_name: {--var: value}}.

    Base :root declarations seed every theme; each prefers-color-scheme or
    [data-theme] block layers its overrides on top, so a variable defined only
    in the base block is still checked within each theme.
    """
    css = strip_comments(css)

    # Base declarations come only from :root blocks OUTSIDE any @media —
    # otherwise a nested dark-scheme :root overwrites the light values and
    # every theme gets audited against the wrong palette.
    outside = _strip_at_blocks(css)
    base = {}
    for body in re.findall(r'(?<![\w-])(?::root|html)\s*\{([^{}]*)\}', outside):
        base.update(dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', body)))

    themes = {}
    for scheme in ('dark', 'light'):
        pat = r'prefers-color-scheme\s*:\s*' + scheme
        for chunk in _at_block_bodies(css, pat):
            for body in re.findall(r'\{([^{}]*)\}', chunk):
                got = dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', body))
                if got:
                    themes.setdefault(f'prefers {scheme}', dict(base)).update(got)

    for name, body in re.findall(r'\[data-theme\s*=\s*[\'"]?([\w-]+)[\'"]?\s*\][^{]*\{([^{}]*)\}', css):
        got = dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', body))
        if got:
            themes.setdefault(f'data-theme={name}', dict(base)).update(got)

    if not themes:
        themes['default'] = base
    else:
        themes = {'base (:root)': base, **themes}
    return themes

# ---------------------------------------------------------------- the checks

# (fg_var, bg_var, floor, label)
PAIRS = [
    ('--text', '--bg', 4.5, 'body text on page background'),
    ('--text', '--surface', 4.5, 'body text on card surface'),
    ('--text', '--surface2', 4.5, 'body text on alt surface'),
    ('--text', '--surface-elevated', 4.5, 'body text on elevated surface'),
    ('--text-bright', '--bg', 4.5, 'emphasis text on page background'),
    ('--text-bright', '--surface', 4.5, 'emphasis text on card surface'),
    ('--text-dim', '--bg', 4.5, 'secondary text on page background'),
    ('--text-dim', '--surface', 4.5, 'secondary text on card surface'),
    ('--text-dim', '--surface2', 4.5, 'secondary text on alt surface'),
    ('--text-dim', '--surface-elevated', 4.5, 'secondary text on elevated surface'),
    ('--accent', '--bg', 4.5, 'accent as text on page background'),
    ('--accent', '--surface', 4.5, 'accent as text on card surface'),
    ('--accent-on-fill', '--accent-fill', 4.5, 'fill ink on accent fill'),
    ('--code-text', '--code-bg', 4.5, 'code text on code background'),
    # --border is deliberately near-invisible in this skill ("visible when you
    # look, invisible when you don't"), so it is not checked here.
]

SEMANTIC = ['green', 'red', 'orange', 'amber', 'blue', 'teal', 'sage', 'fern',
            'moss', 'berry', 'sky', 'bark', 'node-a', 'node-b', 'node-c']


def build_checks(variables):
    checks = list(PAIRS)
    for name in SEMANTIC:
        v = f'--{name}'
        if v in variables:
            for bgv in ('--surface', '--bg'):
                if bgv in variables:
                    checks.append((v, bgv, 4.5, f'{v} as text on {bgv}'))
    # X-dim / X-wash / X-soft is only a *background tint* when it's genuinely
    # translucent. Palettes also use the -dim suffix for solid secondary TEXT
    # colors (--ink-dim, --text-dim), which are not backgrounds — checking ink
    # against those produces noise, not findings.
    for v in variables:
        if not re.search(r'-(dim|wash|soft|tint)$', v):
            continue
        base_var = re.sub(r'-(dim|wash|soft|tint)$', '', v)
        if base_var not in variables or base_var in ('--text', '--ink'):
            continue
        tint = parse_color(variables[v], variables)
        if tint is None or tint[3] > 0.6:
            continue
        # The base must itself be an opaque ink. A translucent base is a rule,
        # divider, or overlay — nothing sets text in it, so pairing the two
        # measures a combination that never appears on screen.
        base_col = parse_color(variables[base_var], variables)
        if base_col is None or base_col[3] < 0.9:
            continue
        checks.append((base_var, v, 4.5, f'{base_var} as text on its own {v} tint'))
    return checks


def resolve_bg(var, variables, page_bg):
    """Resolve a background var, compositing translucent tints over the page."""
    raw = variables.get(var)
    if raw is None:
        return None
    col = parse_color(raw, variables)
    if col is None:
        return None
    return flatten(col, page_bg)


def check_theme(theme, variables, rows):
    page_bg = None
    for candidate in ('--bg', '--surface', '--background'):
        if candidate in variables:
            c = parse_color(variables[candidate], variables)
            if c and c[3] >= 0.999:
                page_bg = c[:3]
                break
    if page_bg is None:
        page_bg = (255, 255, 255)

    for fg_var, bg_var, floor, label in build_checks(variables):
        if fg_var not in variables or bg_var not in variables:
            continue
        bg = resolve_bg(bg_var, variables, page_bg)
        fg = flatten(parse_color(variables[fg_var], variables), bg)
        r = contrast(fg, bg)
        if r is None:
            continue
        rows.append((theme, label, fg_var, to_hex(fg), bg_var, to_hex(bg), r, floor))


LIGHT_INK = re.compile(
    r'color\s*:\s*(#f[0-9a-f]{5}|#fff\b|#ffffff|white|rgba?\(\s*2[45][0-9]\s*,'
    r'\s*2[45][0-9]\s*,\s*2[45][0-9]|var\(--accent-on-fill)', re.I)


def check_literal_pairs(css, variables_by_theme, findings):
    """
    Flag rules that set a light ink and an accent-derived background in the same
    declaration block — the 'white text on pale green' shape. Reported against
    every theme, since the accent tone flips between them.
    """
    css = strip_comments(css)
    for selector, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        sel = ' '.join(selector.split())
        if sel.startswith('@') or '--' == sel[:2]:
            continue
        bg_m = re.search(r'(?:^|[;\s])background(?:-color)?\s*:\s*([^;]+)', body)
        if not bg_m or not LIGHT_INK.search(body):
            continue
        bg_raw = bg_m.group(1).strip()
        if 'var(--accent-fill' in bg_raw or 'var(--surface' in bg_raw:
            continue
        if not re.search(r'var\(--(accent|node-|green|red|orange|amber|teal|sage|blue|moss|fern|berry)', bg_raw):
            if not re.match(r'^#[0-9a-fA-F]{3,6}$', bg_raw):
                continue
        ink_m = re.search(r'color\s*:\s*([^;]+)', body)
        ink_raw = ink_m.group(1).strip() if ink_m else '?'
        for theme, variables in variables_by_theme.items():
            bg = parse_color(bg_raw, variables)
            fg = parse_color(ink_raw, variables)
            if not bg or not fg:
                continue
            bg = flatten(bg, (255, 255, 255))
            r = contrast(flatten(fg, bg), bg)
            if r and r < 4.5:
                findings.append((theme, sel[:58], ink_raw[:26], bg_raw[:26], r))


def check_bright_fills(css, variables_by_theme, findings):
    """
    Report palette colors that are used as a `background` somewhere and are too
    bright to carry light ink. Cross-rule cascade (ink on a parent, fill on a
    child) is beyond a static checker, so instead of guessing the pairing this
    names the fills whose ink MUST be dark — the list to eyeball in the render.
    """
    css = strip_comments(css)
    used = set()
    for _sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        for m in re.finditer(r'(?:^|[;\s])background(?:-color)?\s*:\s*([^;]+)', body):
            for var in re.findall(r'var\(\s*(--[\w-]+)', m.group(1)):
                used.add(var)

    skip = re.compile(r'-(dim|wash|soft|tint|on-fill)$|^--(bg|surface|border|text|code-bg|pattern)')
    for theme, variables in variables_by_theme.items():
        for var in sorted(used):
            if var not in variables or skip.search(var):
                continue
            fill = parse_color(variables[var], variables)
            if fill is None or fill[3] < 0.9:
                continue
            fill = fill[:3]
            # Skip anything that is effectively the page ground under another
            # name (--paper, --sunk, --canvas): no ink was ever going to be
            # light on it, so naming it here is noise.
            page = parse_color(variables.get('--bg', '#fff'), variables)
            if page and contrast(fill, page[:3]) < 1.6:
                continue
            vs_white = contrast(fill, (255, 255, 255))
            if vs_white and vs_white < 3.0:
                # Suggest whichever ink in the palette actually reads on this
                # fill. In a dark theme --text-bright is near-white and wrong
                # here; --bg is the near-black that works.
                best_var, best_r = None, 0
                for cand in ('--text-bright', '--text', '--bg', '--surface'):
                    col = parse_color(variables.get(cand, ''), variables)
                    if not col:
                        continue
                    r = contrast(col[:3], fill)
                    if r and r > best_r:
                        best_var, best_r = cand, r
                findings.append((theme, var, to_hex(fill), vs_white, best_var, best_r))


PATTERN_RE = re.compile(r'repeating-(?:linear|radial|conic)-gradient\(([^;]*)', re.I)


def check_patterns(css, variables_by_theme, findings):
    """Flag repeating background patterns drawn too strongly, or in --border."""
    css = strip_comments(css)
    for selector, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        sel = ' '.join(selector.split())
        for m in PATTERN_RE.finditer(body):
            frag = m.group(1)
            reasons = []
            if 'var(--border' in frag:
                reasons.append('drawn in --border (use --pattern)')
            spacings = [float(x) for x in re.findall(r'([\d.]+)px', frag)]
            if spacings and max(spacings) < 20:
                reasons.append(f'repeat spacing {max(spacings):.0f}px reads as stripes')
            for theme, variables in variables_by_theme.items():
                for tok in re.findall(r'(var\(--[\w-]+[^)]*\)|#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))', frag):
                    c = parse_color(tok, variables)
                    if c and c[3] > 0.08:
                        against = parse_color(variables.get('--bg', '#fff'), variables) or (255, 255, 255, 1)
                        r = contrast(flatten(c, against[:3]), against[:3])
                        if r and r > 1.35:
                            reasons.append(f'{theme}: stripe {to_hex(flatten(c, against[:3]))} '
                                           f'is {r:.1f}:1 vs --bg (aim under 1.35:1)')
                        break
            if reasons:
                findings.append((sel[:58], sorted(set(reasons))))

# ---------------------------------------------------------------- reporting


def verdict(r, floor):
    if r >= floor:
        return 'PASS'
    return 'WARN' if r >= floor - 1.2 else 'FAIL'


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file')
    ap.add_argument('--quiet', action='store_true', help='only show FAIL rows')
    ap.add_argument('--strict', action='store_true', help='exit 1 on WARN too')
    args = ap.parse_args()

    if not os.path.exists(args.file):
        print(f'no such file: {args.file}', file=sys.stderr)
        return 2

    with open(args.file, encoding='utf-8', errors='replace') as fh:
        html = fh.read()

    css = extract_styles(html)
    if not css.strip():
        print('no <style> block found — nothing to check', file=sys.stderr)
        return 2

    themes = theme_blocks(css)
    rows = []
    for theme, variables in themes.items():
        check_theme(theme, variables, rows)

    literal, patterns, bright = [], [], []
    check_literal_pairs(css, themes, literal)
    check_patterns(css, themes, patterns)
    check_bright_fills(css, themes, bright)

    fails = warns = 0
    print(f'\n  {os.path.basename(args.file)} — {len(themes)} theme block(s)\n')

    current = None
    for theme, label, fg_var, fg_hex, bg_var, bg_hex, r, floor in rows:
        v = verdict(r, floor)
        if v == 'FAIL':
            fails += 1
        elif v == 'WARN':
            warns += 1
        if v == 'PASS' or (args.quiet and v != 'FAIL'):
            continue
        if theme != current:
            print(f'  {theme}')
            current = theme
        print(f'    {v:4}  {r:5.2f}:1 (need {floor})  {label}')
        print(f'          {fg_var} {fg_hex}  on  {bg_var} {bg_hex}')

    if literal:
        print('\n  Light ink on an accent fill — check these by hand:')
        for theme, sel, ink, bg, r in literal:
            fails += 1
            print(f'    FAIL  {r:5.2f}:1  {sel}')
            print(f'          color: {ink}  /  background: {bg}   [{theme}]')

    if bright and not args.quiet:
        print('\n  Bright fills — any text on these must be DARK ink, never white:')
        seen = set()
        for theme, var, hexv, vs_white, ink_var, ink_r in bright:
            key = (var, hexv)
            if key in seen:
                continue
            seen.add(key)
            suggestion = (f'use {ink_var} ({ink_r:.1f}:1)' if ink_var and ink_r >= 4.5
                          else 'no palette ink clears 4.5:1 — darken the fill')
            print(f'    NOTE  {var} {hexv}  white on it = {vs_white:.2f}:1  →  '
                  f'{suggestion}   [{theme}]')

    if patterns:
        print('\n  Background patterns:')
        for sel, reasons in patterns:
            warns += 1
            print(f'    WARN  {sel}')
            for reason in reasons:
                print(f'          {reason}')

    total_checked = len(rows)
    if total_checked == 0:
        print('  no resolvable text/background pairs found — is this a themed '
              'html-craft page?\n  (expects CSS custom properties: --bg, '
              '--surface, --text, --text-dim, ...)\n')
        return 2

    print(f'\n  {total_checked} pair(s) checked · {fails} fail · {warns} warn')
    if fails == 0 and warns == 0:
        print('  clean\n')
    else:
        print('  Floors: 4.5:1 text under ~19px · 3:1 display type and meaningful '
              'non-text.\n  Fix every FAIL; keep a WARN only for a deliberate reason.\n')

    if fails:
        return 1
    return 1 if (args.strict and warns) else 0


if __name__ == '__main__':
    sys.exit(main())
