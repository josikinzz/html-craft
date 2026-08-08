# Responsive Section Navigation

Navigation pattern for multi-section pages (reviews, recaps, dashboards). Provides a sticky sidebar TOC on desktop and a sticky horizontal scrollable bar on mobile.

## Layout Structure

The page uses a two-column CSS Grid: sidebar (TOC) + main content. On mobile it collapses to single-column with the TOC becoming a horizontal bar.

```html
<body>
<div class="wrap">

  <nav class="toc" id="toc">
    <div class="toc-title">Contents</div>
    <a href="#s1">1. First Section</a>
    <a href="#s2">2. Second Section</a>
    <!-- one link per section -->
  </nav>

  <div class="main">
    <h1>Page Title</h1>
    <p class="subtitle">Subtitle text</p>

    <div id="s1" class="sec-head ...">1 — First Section</div>
    <!-- section content -->

    <div id="s2" class="sec-head ...">2 — Second Section</div>
    <!-- section content -->
  </div><!-- /main -->

</div><!-- /wrap -->
</body>
```

Key structural rules:
- `<nav class="toc">` is the **first child** of `.wrap`
- All page content goes inside `<div class="main">`
- Every section heading gets an `id="s1"`, `id="s2"`, etc.
- TOC links use `href="#s1"` matching those IDs
- Keep TOC link text short (truncate long section names)

## CSS

### Wrap (grid layout)

```css
.wrap {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 170px 1fr;
  gap: 0 40px;
}
.main { min-width: 0; }
```

### TOC — Desktop (sticky sidebar)

```css
.toc {
  position: sticky;
  top: 24px;
  align-self: start;
  padding: 14px 0;
  /* `.toc` and `.main` are the wrap's only children, so both land in row 1.
     `grid-row: 1 / -1` reads like "span every row" but -1 can't address
     implicit rows — with no grid-template-rows it resolves to row 1 anyway.
     Say row 1 outright rather than lean on that. If the wrap ever gains
     explicit rows the sidebar wants to span, declare them and update this. */
  grid-row: 1;
  max-height: calc(100dvh - 48px);
  overflow-y: auto;
}
.toc::-webkit-scrollbar { width: 3px; }
.toc::-webkit-scrollbar-thumb { background: var(--surface-elevated); border-radius: 2px; }

/* 10px is the floor for a mono label at this tracking — 9px in --text-dim is
   past the point where the uppercase forms stay distinguishable. */
.toc-title {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--text-dim);
  padding: 0 0 10px;
  margin-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

/* TOC entries are navigation targets, not captions — they have to be readable
   at a glance and clickable with confidence. 11px in --text-dim is the low
   point of most palettes; 12px and a slightly stronger ink costs no space and
   makes the rail usable. --text-dim still has to clear 4.5:1 here regardless. */
.toc a {
  display: block;
  font-size: 12px;
  color: var(--text);
  opacity: 0.78;
  text-decoration: none;
  padding: 4px 8px;
  border-radius: 5px;
  border-left: 2px solid transparent;
  transition: all 0.15s;
  line-height: 1.4;
  margin-bottom: 1px;
}
.toc a:hover { color: var(--text); opacity: 1; background: var(--surface2); }
.toc a.active { color: var(--text); opacity: 1; font-weight: 600; border-left-color: var(--accent); }
.toc a:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; opacity: 1; }
```

Replace `var(--accent)` with your page's primary accent color variable (e.g., `var(--orange)`, `var(--blue)`).

The 2px `border-left` on `.active` is a functional state indicator, not a decorative accent stripe — that carve-out is explicit in the Anti-Patterns section of `SKILL.md`. Note it's paired with a weight change so the active item is distinguishable without relying on the color alone.

### TOC — Mobile (sticky horizontal bar)

```css
@media (max-width: 1000px) {
  /* The bar's metrics are tokens so its height can be computed instead of
     guessed — `scroll-margin-top` below depends on it, and a hardcoded number
     there silently goes stale the first time this padding or type size moves. */
  :root {
    --toc-bar-pad: 10px;
    --toc-link-pad: 6px;
    --toc-link-size: 12px;
    --toc-bar-h: calc(2 * var(--toc-bar-pad) + 2 * var(--toc-link-pad)
                      + var(--toc-link-size) * 1.4 + 1px);  /* +1px bottom border */
  }

  .wrap { grid-template-columns: 1fr; padding-top: 0; }
  body { padding-top: 0; }

  .toc {
    position: sticky;
    top: 0;
    z-index: 200;
    max-height: none;
    display: flex;
    gap: 4px;
    align-items: center;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    padding: var(--toc-bar-pad) 0;
    margin: 0 -40px;
    padding-left: 40px;
    padding-right: 40px;
    grid-row: auto;
  }
  .toc::-webkit-scrollbar { display: none; }
  .toc-title { display: none; }

  /* Same floor as the desktop rail: these are navigation targets, not
     captions. 10px was below it — the bar is the only nav a phone reader has. */
  .toc a {
    white-space: nowrap;
    flex-shrink: 0;
    border-left: none;
    border-bottom: 2px solid transparent;
    border-radius: 4px 4px 0 0;
    padding: var(--toc-link-pad) 10px;
    font-size: var(--toc-link-size);
    line-height: 1.4;
  }
  .toc a.active {
    border-left: none;
    border-bottom-color: var(--accent);
    background: var(--surface);
  }

  .main { padding-top: 20px; }

  /* Offset scroll target so headings clear the sticky bar, plus a little air */
  .sec-head { scroll-margin-top: calc(var(--toc-bar-h) + 8px); }
}
```

Adjust `margin: 0 -40px` and `padding-left/right: 40px` to match your `body` padding so the bar bleeds edge-to-edge.

## JavaScript — Scroll Spy

Place before `</body>`, after any Mermaid init:

```html
<script>
(function() {
  const toc = document.getElementById('toc');
  const links = toc.querySelectorAll('a');
  const sections = [];

  // Chrome and Safari animate scrollIntoView({behavior:'smooth'}) whatever the
  // user's motion preference says — only Firefox honors it. Every scripted
  // scroll here checks for itself. Read at call time so a mid-session flip counts.
  const motionOK = () => !matchMedia('(prefers-reduced-motion: reduce)').matches;

  links.forEach(link => {
    const id = link.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) sections.push({ id, el, link });
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        links.forEach(l => l.classList.remove('active'));
        const match = sections.find(s => s.el === entry.target);
        if (match) {
          match.link.classList.add('active');
          // On mobile, auto-scroll the active tab into view
          if (window.innerWidth <= 1000) {
            match.link.scrollIntoView({
              behavior: motionOK() ? 'smooth' : 'auto',
              block: 'nearest', inline: 'center'
            });
          }
        }
      }
    });
  }, { rootMargin: '-10% 0px -80% 0px' });

  sections.forEach(s => observer.observe(s.el));

  links.forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      const id = link.getAttribute('href').slice(1);
      const el = document.getElementById(id);
      if (el) {
        el.scrollIntoView({ behavior: motionOK() ? 'smooth' : 'auto', block: 'start' });
        history.replaceState(null, '', '#' + id);
      }
    });
  });
})();
</script>
```

## Adaptation Notes

- The `.toc-title` text, link labels, accent color, and section IDs change per page. Everything else is copy-paste.
- For pages with fewer than 4 sections, skip the TOC entirely — it adds clutter without value.
- The `grid-template-columns: 170px 1fr` width works for most TOCs. If section names are longer, go up to `200px`.
- Change the mobile bar's padding or link size through the `--toc-bar-*` tokens, not the rules themselves — `--toc-bar-h` feeds the heading `scroll-margin-top`, so headings keep clearing the bar without a second edit.
- The `rootMargin: '-10% 0px -80% 0px'` means a section is "active" when its heading enters the top 10-20% of the viewport. This works well with sticky headers.
- On mobile, the horizontal bar uses `overflow-x: auto` with hidden scrollbar. The active tab auto-scrolls into the center of the bar as the user scrolls the page.
