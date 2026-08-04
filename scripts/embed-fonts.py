#!/usr/bin/env python3
"""Inline Google Fonts <link> tags into a self-contained HTML file.

Turns a page that depends on fonts.googleapis.com / fonts.gstatic.com into one
that carries its fonts as base64 @font-face data URIs, so it opens identically
with no network and works on strict-CSP hosts (e.g. claude.ai Artifacts).

Usage:
    python3 embed-fonts.py path/to/page.html            # rewrite in place
    python3 embed-fonts.py page.html --out out.html      # write a copy
    python3 embed-fonts.py page.html --subsets latin,latin-ext,cyrillic

By default only the `latin` and `latin-ext` unicode-range subsets are embedded
(they cover English plus common accented text and typographic punctuation),
which keeps the file small. Pass --subsets to include more (e.g. `cyrillic`,
`greek`, `vietnamese`) if the page uses those glyphs. `all` embeds everything.

Exit codes: 0 = embedded (or nothing to do), 1 = error.
"""
import argparse
import base64
import re
import sys
import urllib.request

# A desktop browser UA is required — Google serves woff2 (smallest, universal)
# only to modern browsers; a default urllib UA gets bloated ttf.
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

_LINK_RE = re.compile(
    r'https://fonts\.googleapis\.com/css2\?[^"\')\s]+', re.IGNORECASE)


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def _embed_css(css_url: str, subsets) -> str:
    """Fetch one css2 URL and return @font-face blocks with data: URIs."""
    css = _fetch(css_url).decode("utf-8")
    # Google emits `/* subset */` comments before each @font-face block.
    parts = re.split(r"/\*\s*([a-z0-9-]+)\s*\*/", css)
    out = []
    want_all = subsets == {"all"}
    for i in range(1, len(parts), 2):
        label, body = parts[i], parts[i + 1]
        if not want_all and label not in subsets:
            continue
        m_fam = re.search(r"font-family:\s*'([^']+)'", body)
        m_url = re.search(r"url\((https[^)]+\.woff2)\)", body)
        if not (m_fam and m_url):
            continue
        fam = m_fam.group(1)
        style = (re.search(r"font-style:\s*([^;]+);", body) or [None, "normal"])[1].strip()
        weight = (re.search(r"font-weight:\s*([^;]+);", body) or [None, "400"])[1].strip()
        urange = re.search(r"unicode-range:\s*([^;]+);", body)
        b64 = base64.b64encode(_fetch(m_url.group(1))).decode()
        block = [
            "@font-face {",
            f"  font-family: '{fam}';",
            f"  font-style: {style};",
            f"  font-weight: {weight};",
            "  font-display: swap;",
            f"  src: url(data:font/woff2;base64,{b64}) format('woff2');",
        ]
        if urange:
            block.append(f"  unicode-range: {urange.group(1).strip()};")
        block.append("}")
        out.append("\n".join(block))
    return "\n".join(out)


def embed(html: str, subsets) -> str:
    urls = []
    for m in _LINK_RE.finditer(html):
        u = m.group(0).rstrip('"\'')
        if u not in urls:
            urls.append(u)
    if not urls:
        return html

    faces = "\n".join(_embed_css(u, subsets) for u in urls)

    # Drop the preconnect hints and the stylesheet <link>s (any attr order).
    html = re.sub(
        r'[ \t]*<link\b[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>[ \t]*\r?\n?',
        "", html, flags=re.IGNORECASE)

    injected = (
        "<style>\n/* embedded fonts — self-contained, base64 @font-face */\n"
        + faces + "\n</style>")
    # Put the fonts just before the first existing <style>, else before </head>.
    if re.search(r"<style\b", html, re.IGNORECASE):
        html = re.sub(r"(<style\b)", injected + "\n\\1", html, count=1,
                      flags=re.IGNORECASE)
    else:
        html = re.sub(r"(</head>)", injected + "\n\\1", html, count=1,
                      flags=re.IGNORECASE)
    return html


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", help="HTML file to process")
    ap.add_argument("--out", help="output path (default: rewrite in place)")
    ap.add_argument("--subsets", default="latin,latin-ext",
                    help="comma-separated unicode-range subsets, or 'all'")
    args = ap.parse_args()

    subsets = {s.strip() for s in args.subsets.split(",") if s.strip()}
    with open(args.html, encoding="utf-8") as f:
        html = f.read()

    try:
        result = embed(html, subsets)
    except Exception as e:  # network, parse, etc. — fail loud, don't half-write
        print(f"embed-fonts: failed: {e}", file=sys.stderr)
        return 1

    if result == html and re.search(r"fonts\.(googleapis|gstatic)\.com", html):
        print("embed-fonts: found font links but nothing was embedded — "
              "check --subsets", file=sys.stderr)
        return 1

    out_path = args.out or args.html
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)

    leftover = re.search(r"https?://fonts\.(googleapis|gstatic)\.com", result)
    print(f"embed-fonts: wrote {out_path} "
          f"({len(result) // 1024} KB, external font refs: "
          f"{'YES — check output' if leftover else 'none'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
