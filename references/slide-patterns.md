# Slide Deck Patterns

CSS patterns, JS engine, slide type layouts, transitions, navigation chrome, and curated presets for self-contained HTML slide presentations. All slides are viewport-fit (100dvh), single-file, same philosophy as scrollable pages.

**When to use slides:** Only when the user explicitly requests them — `/generate-slides`, `--slides` flag on an existing prompt, or natural language like "as a slide deck." Never auto-select slide format.

**Before generating**, also read `./css-patterns.md` for shared patterns (overflow protection, depth tiers, status badges), `./mermaid.md` for Mermaid theming and containers, and `./libraries.md` for Chart.js and font pairings. Those patterns apply to slides too — this file adds slide-specific patterns on top.

## Planning a Deck from a Source Document

When converting a plan, spec, review, or any structured document into slides, follow this process before writing any HTML. Skipping it leads to polished-looking decks that silently drop 30–40% of the source material.

**Step 1 — Inventory the source.** Read the entire source document and enumerate every section, subsection, card, table row, decision, specification, collapsible detail, and footnote. Count them. A plan with 7 sections, 6 decision cards, a 7-row file table, 4 presets, 6 technique guides, and an engine spec with 3 sub-specs and 2 collapsibles is ~25 distinct content items that all need slide real estate.

**Step 2 — Map source to slides.** Assign each inventory item to one or more slides. Every item must appear somewhere. Rules:
- If a section has 6 decisions, all 6 need slides — not the 2 that fit on one split slide.
- If a table has 7 rows, all 7 rows show up.
- Collapsible/expandable details in the source are not optional in the deck — they become their own slides.
- Subsections with multiple cards (e.g., "6 Visual Technique cards") may need 2–3 slides to cover at readable density.
- Each plan section typically needs a divider slide + 1–3 content slides depending on density.

**Step 3 — Choose layouts.** For each planned slide, pick a slide type and spatial composition. Vary across the sequence (see Compositional Variety below). This is where narrative pacing happens — alternate dense slides with sparse ones.

**Step 4 — Plan images.** Run `which surf`. If surf-cli is available, plan 2–4 generated images for the deck. At minimum, target the **title slide** (16:9 background that sets the visual tone) and **one full-bleed slide** (immersive background for a key moment). Content slides with conceptual topics also benefit from a 1:1 illustration in the aside area. Generate these images early — before writing HTML — so you can embed them as base64 data URIs. See the Proactive Imagery section below for the full workflow. If surf isn't available, degrade to CSS gradients and SVG decorations — note the fallback in a comment but don't error.

**Step 5 — Verify before writing HTML.** Scan the inventory from Step 1. Is anything unmapped? Would a reader of the source document notice something missing from the deck? If yes, add slides. A source document with 7 sections typically produces 18–25 slides, not 10–13.

**The test:** After generating the deck, a reader who has never seen the source document should be able to reconstruct every major point from the slides alone. If they'd miss entire sections, the deck is incomplete.

## Slide Engine Base

The deck is a scroll-snap container. Each slide is exactly one viewport tall.

```html
<body>
<div class="deck">
  <section class="slide slide--title"> ... </section>
  <section class="slide slide--content"> ... </section>
  <section class="slide slide--diagram"> ... </section>
  <!-- one <section> per slide -->
</div>
</body>
```

```css
/* Scroll-snap container */
.deck {
  height: 100dvh;
  overflow-y: auto;
  scroll-snap-type: y mandatory;
  /* No scroll-behavior: smooth here — goTo() does its own scrolling, so the
     motion decision belongs in JS where the deck can check the preference.
     Don't assume the browser handles it: only Firefox drops smooth scrolling
     for reduced-motion users; Chrome and Safari animate regardless, for both
     the CSS property and scrollIntoView(). Guard it yourself (see below). */
  -webkit-overflow-scrolling: touch;
}

/* Individual slide */
.slide {
  height: 100dvh;
  scroll-snap-align: start;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(40px, 6vh, 80px) clamp(40px, 8vw, 120px);
  isolation: isolate; /* contain z-index stacking */
}
```

## Typography Scale

Slide typography is 2–3× larger than scrollable pages. Page-sized text on a viewport-sized canvas looks like a mistake.

```css
.slide__display {
  font-size: clamp(48px, 10vw, 120px);
  font-weight: 800;
  letter-spacing: -3px;
  line-height: 0.95;
  text-wrap: balance;
}

.slide__heading {
  font-size: clamp(28px, 5vw, 48px);
  font-weight: 700;
  letter-spacing: -1px;
  line-height: 1.1;
  text-wrap: balance;
}

.slide__body {
  font-size: clamp(16px, 2.2vw, 24px);
  line-height: 1.6;
  text-wrap: pretty;
}

.slide__label {
  font-family: var(--font-mono);
  font-size: clamp(10px, 1.2vw, 14px);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-dim);
}

.slide__subtitle {
  font-family: var(--font-mono);
  font-size: clamp(14px, 1.8vw, 20px);
  color: var(--text-dim);
  letter-spacing: 0.5px;
}
```

| Element | Size range | Notes |
|---------|-----------|-------|
| Display (title slides) | 48–120px | `10vw` preferred, weight 800 |
| Section numbers | 100–240px | Ultra-light (weight 200), decorative |
| Headings | 28–48px | `5vw` preferred, weight 700 |
| Body / bullets | 16–24px | `2.2vw` preferred, 1.6 line-height |
| Code blocks | 14–18px | `1.8vw` preferred, mono |
| Quotes | 24–48px | `4vw` preferred, serif italic |
| Labels / captions | 10–14px | Mono, uppercase, dimmed |

## Cinematic Transitions

IntersectionObserver adds `.visible` when a slide enters the viewport. Slides animate in once and stay visible when scrolling back.

```css
/* Slide entrance — fade + lift + subtle scale */
.slide {
  opacity: 0;
  transform: translateY(40px) scale(0.98);
  transition:
    opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide.visible {
  opacity: 1;
  transform: none;
}

/* Staggered child reveals — add .reveal to each content element */
.slide .reveal {
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide.visible .reveal {
  opacity: 1;
  transform: none;
}

/* Stagger delays — set --i on each .reveal in the HTML: 0, 1, 2, …
   Not nth-child: it counts every sibling (a heading, a decorative SVG, an
   un-revealed wrapper all consume positions), and a hand-written ladder stops
   at whatever number you typed — the 7th item then pops in at 0s while the
   6th is still easing. The custom property has no ceiling and doesn't care
   what sits between the revealed elements. */
.slide.visible .reveal {
  transition-delay: calc(0.1s + var(--i, 0) * 0.1s);
}

@media (prefers-reduced-motion: reduce) {
  .slide,
  .slide .reveal {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
}
```

Number the reveals inline, restarting at 0 on each slide — `<li class="reveal" style="--i:0">`, `--i:1`, and so on. A `.reveal` without `--i` still animates; it just lands in the first wave.

## Navigation Chrome

All navigation is `position: fixed` with high z-index, layered above slides. Styled to be visible on any background.

### Progress Bar

```css
.deck-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: var(--accent);
  z-index: 100;
  transition: width 0.3s ease;
  pointer-events: none;
}
```

### Nav Dots

```css
.deck-dots {
  position: fixed;
  right: clamp(12px, 2vw, 24px);
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 0; /* the spacing lives inside each button — see below */
  z-index: 100;
}

/* 8px of ink inside a 24px button. An 8px dot with an 8px gap is a third of
   the 24px target-size floor and puts neighbouring targets 16px apart — easy
   to mis-tap, and impossible to hit at all with a shaky pointer. Keep the mark
   small and make the hit area real: the dot moves to ::before and the button
   becomes the target. Inactive dots at 0.3 alpha are effectively invisible —
   they're a control, so they need the 3:1 non-text floor. 0.55 reads as
   "available but quiet". */
.deck-dot {
  width: 24px;
  height: 24px;
  display: grid;
  place-items: center;
  background: none;
  border: none;
  border-radius: 50%;
  padding: 0;
  cursor: pointer;
}

.deck-dot::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-dim);
  opacity: 0.55;
  transition: opacity 0.2s ease, transform 0.2s ease, background 0.2s ease;
}

.deck-dot:hover::before {
  opacity: 0.85;
}

/* Ring hugs the hit area rather than floating 3px outside it */
.deck-dot:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}

.deck-dot.active::before {
  opacity: 1;
  transform: scale(1.5);
  background: var(--accent);
}
```

### Slide Counter

```css
.deck-counter {
  position: fixed;
  bottom: clamp(12px, 2vh, 24px);
  right: clamp(12px, 2vw, 24px);
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-dim);
  z-index: 100;
  font-variant-numeric: tabular-nums;
}
```

### Keyboard Hints

Auto-fade after first interaction or after 4 seconds.

```css
.deck-hints {
  position: fixed;
  bottom: clamp(12px, 2vh, 24px);
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-dim);
  opacity: 0.6;
  z-index: 100;
  transition: opacity 0.5s ease;
  white-space: nowrap;
}

/* Dim, don't remove — a viewer who looks back for the controls still finds them */
.deck-hints.faded {
  opacity: 0.25;
}
```

### Chrome Visibility on Mixed Backgrounds

For decks where some slides are light and some dark (especially full-bleed slides), nav chrome needs to remain visible. Give chrome elements a mostly-opaque tint of the page background — solid enough to guarantee legibility on any slide, with no blur or text-shadow (both read as haze/halo artifacts):

```css
.deck-dots,
.deck-counter {
  background: color-mix(in srgb, var(--bg) 85%, transparent 15%);
  padding: 6px;
  border-radius: 20px;
}
```

## SlideEngine JavaScript

The complete SlideEngine — navigation, chrome, scroll-triggered reveals, deep links — lives in `templates/slide-deck.html`. **Copy it wholesale**; it is the single source of truth for this engine. Do not retype it from memory or rebuild it from this summary.

Rules the implementation embodies (verify these survive your adaptation):

- **Boot independently of libraries:** construct SlideEngine on `DOMContentLoaded`, never inside a Mermaid/Chart.js `.then()` — a CDN failure must not take navigation down. Call `autoFit()` (below) after libraries render.
- **Event delegation:** keyboard handlers skip events originating inside `.mermaid-wrap, .table-scroll, .code-scroll, input, textarea, [contenteditable]` so slide-internal interactions never trigger slide navigation.
- **Deep links:** `#5` opens on slide 5; `update()` keeps the URL at the current slide via `history.replaceState` (wrapped in try/catch for `file://` edge cases).
- **Chrome is built in JS:** progress bar, dots (one focusable button per slide), counter, and keyboard hints are appended to `<body>`, so slide markup stays clean.
- **Reduced motion is checked, not delegated:** Chrome and Safari animate `scrollIntoView({behavior:'smooth'})` no matter what the user's motion preference says — only Firefox overrides it. So `goTo()` reads the preference itself, at call time, and picks the behavior:

  ```javascript
  const motionOK = !matchMedia('(prefers-reduced-motion: reduce)').matches;
  el.scrollIntoView({ behavior: motionOK ? 'smooth' : 'auto' });
  ```

  Same guard on every other scripted scroll in the deck. Reading it inside the handler rather than once at boot means a mid-session preference flip is honored.
- **Hints dim, never vanish:** after the 4s timer or first keypress, `.deck-hints.faded` drops to low opacity — first-time viewers can still find it.
- **IntersectionObserver at `threshold: 0.5`** both marks slides `.visible` (triggering reveals) and tracks the current index — one observer, two jobs.

## Auto-Fit

A single post-render function that handles all known content overflow cases. Agents can't perfectly predict how text reflows at every viewport size, so `autoFit()` is a required safety net. Call it after Mermaid/Chart.js render but before SlideEngine init.

```javascript
function autoFit() {
  // Mermaid SVGs: contain in BOTH axes so the whole diagram stays on the slide.
  // width:100% + height:auto stretches to the container width and lets a tall
  // diagram run off the bottom of a fixed-height slide — the slide then opens
  // showing only the top of the graph, with no way to scroll to the rest.
  document.querySelectorAll('.mermaid svg').forEach(function(svg) {
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    svg.style.width = 'auto';
    svg.style.height = 'auto';
    svg.style.maxWidth = '100%';
    svg.style.maxHeight = '100%';
    if (svg.parentElement) {
      svg.parentElement.style.maxWidth = '100%';
      svg.parentElement.style.maxHeight = '100%';
    }
  });

  // KPI values: visually scale down text that overflows card width
  document.querySelectorAll('.slide__kpi-val').forEach(function(el) {
    if (el.scrollWidth > el.clientWidth) {
      var s = el.clientWidth / el.scrollWidth;
      el.style.transform = 'scale(' + s + ')';
      el.style.transformOrigin = 'left top';
    }
  });

  // Blockquotes: reduce font proportionally for long text
  document.querySelectorAll('.slide--quote blockquote').forEach(function(el) {
    var len = el.textContent.trim().length;
    if (len > 100) {
      var scale = Math.max(0.5, 100 / len);
      var fs = parseFloat(getComputedStyle(el).fontSize);
      el.style.fontSize = Math.max(16, Math.round(fs * scale)) + 'px';
    }
  });
}
```

Three cases, one function:
- **Mermaid:** SVGs render at fixed intrinsic dimensions inside flex containers — cap them to the container on both axes so they scale down to fit rather than overflowing. Contain, never stretch.
- **KPI values:** Long text strings at hero scale overflow card boundaries — `transform: scale()` shrinks visually without reflow.
- **Blockquotes:** Quotes longer than ~100 characters get proportionally smaller font. The 0.5 floor prevents unreadably small text; if it needs more than 50% shrink, it should have been a content slide.

## Slide Type Layouts

Each type has a defined HTML structure and CSS layout. The agent can adapt colors, fonts, and spacing per aesthetic, but the structural patterns stay consistent.

### Title Slide

Full-viewport hero. Background treatment via gradient, texture, or surf-generated image. 80–120px display type.

```html
<section class="slide slide--title">
  <svg class="slide__decor" ...><!-- optional decorative accent --></svg>
  <div class="slide__content reveal">
    <h1 class="slide__display">Deck Title</h1>
    <p class="slide__subtitle reveal">Subtitle or date</p>
  </div>
</section>
```

```css
.slide--title {
  justify-content: center;
  align-items: center;
  text-align: center;
}
```

### Section Divider

Oversized decorative number (200px+, ultra-light weight) with heading. Breathing room between topics. SVG accent marks optional.

```html
<section class="slide slide--divider">
  <span class="slide__number">02</span>
  <div class="slide__content">
    <h2 class="slide__heading reveal">Section Title</h2>
    <p class="slide__subtitle reveal">Optional subheading</p>
  </div>
</section>
```

```css
.slide--divider {
  justify-content: center;
}

.slide--divider .slide__number {
  font-size: clamp(100px, 22vw, 260px);
  font-weight: 200;
  line-height: 0.85;
  opacity: 0.08;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -55%);
  pointer-events: none;
  font-variant-numeric: tabular-nums;
}
```

### Content Slide

Heading + bullets or paragraphs. Asymmetric layout — content offset to one side. Max 5–6 bullets (2 lines each).

```html
<section class="slide slide--content">
  <div class="slide__inner">
    <div class="slide__text">
      <h2 class="slide__heading reveal">Heading</h2>
      <ul class="slide__bullets">
        <li class="reveal" style="--i:0">First point</li>
        <li class="reveal" style="--i:1">Second point</li>
      </ul>
    </div>
    <div class="slide__aside reveal">
      <!-- optional: illustration, icon, mini-diagram, accent SVG -->
    </div>
  </div>
</section>
```

```css
.slide--content .slide__inner {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: clamp(24px, 4vw, 60px);
  align-items: center;
  width: 100%;
}

/* Grid items default to min-width: auto, which means a long unbroken string,
   a code block, or a Mermaid SVG sets the column's floor and pushes the other
   column off the slide. Both tracks opt out. */
.slide--content .slide__text,
.slide--content .slide__aside {
  min-width: 0;
}

/* For right-heavy variant: swap to 2fr 3fr */
.slide--content .slide__bullets {
  list-style: none;
  padding: 0;
}

/* Bullets are body copy — they go in --text, not --text-dim.
   Dimming the only substance on the slide is the fastest way to make a deck
   unreadable from the back of a room. If bullets need to recede relative to
   the heading, do it with size and weight; the heading is already 2x their size. */
.slide--content .slide__bullets li {
  padding: 8px 0 8px 20px;
  position: relative;
  font-size: clamp(16px, 2vw, 22px);
  line-height: 1.6;
  color: var(--text);
}

/* Secondary detail hanging off a bullet — this is what --text-dim is for */
.slide--content .slide__bullets li small {
  display: block;
  font-size: 0.75em;
  color: var(--text-dim);
  margin-top: 2px;
}

.slide--content .slide__bullets li::before {
  content: '';
  position: absolute;
  left: 0;
  /* Derived, not eyeballed: padding-top + half a line - half the dot.
     A fixed 18px is correct only at the clamp's 16px minimum; by 22px the
     line has grown 10px and the marker floats up near the ascenders. */
  top: calc(8px + 0.8em - 3px);
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
}
```

### Split Slide

Asymmetric two-panel (60/40 or 70/30). Before/after, text+diagram, text+image. Each panel has its own background tier. Zero padding on the slide itself — panels fill edge to edge.

```html
<section class="slide slide--split">
  <div class="slide__panels">
    <div class="slide__panel slide__panel--primary">
      <h2 class="slide__heading reveal">Left Panel</h2>
      <div class="slide__body reveal">Content...</div>
    </div>
    <div class="slide__panel slide__panel--secondary">
      <!-- diagram, image, code block, or contrasting content -->
    </div>
  </div>
</section>
```

```css
.slide--split {
  padding: 0;
}

.slide--split .slide__panels {
  display: grid;
  grid-template-columns: 3fr 2fr;
  height: 100%;
}

.slide--split .slide__panel {
  padding: clamp(40px, 6vh, 80px) clamp(32px, 4vw, 60px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;   /* a code block or Mermaid SVG here would otherwise widen the
                     track and shove the other panel past the slide edge */
}

.slide--split .slide__panel--primary {
  background: var(--surface);
}

.slide--split .slide__panel--secondary {
  background: var(--surface2);
}
```

### Diagram Slide

Full-viewport Mermaid diagram. Max 8–10 nodes (presentation scale — fewer, larger than page diagrams). Node labels at 18px+, edges at 2px+. Zoom controls from `css-patterns.md` apply here.

**When to use Mermaid vs CSS in slides.** Mermaid renders SVGs at a fixed size the agent can't control — node dimensions are set by the library, not by CSS. This creates a recurring problem: small diagrams (fewer than ~7 nodes, no branching) render as tiny elements floating in a huge viewport with acres of dead space. The rule:

- **Use Mermaid** for complex graphs: 8+ nodes, branching paths, cycles, multiple edge crossings — anything where automatic edge routing saves real effort.
- **Use CSS Pipeline** (below) for simple linear flows: A → B → C → D sequences, build steps, deployment stages. CSS cards give full control over sizing, typography, and fill the viewport naturally.
- **Never leave a small Mermaid diagram alone on a slide.** If the diagram is small, either switch to CSS, or pair it with supporting content (description cards, bullet annotations, a summary panel) in a split layout. A slide with a tiny diagram and empty space is a failed slide.

**Mermaid centering fix.** When you do use Mermaid, add `display: flex; align-items: center; justify-content: center;` to `.mermaid-wrap` so the SVG centers within its container instead of hugging the top-left corner.

**Diagram interaction on slides is click-to-expand only.** Slides are fixed-viewport, so in-slide pan/zoom fights the deck's own scroll model. The full transform-based pan/zoom engine belongs to scrollable pages (see `mermaid.md` and `templates/mermaid-flowchart.html`); on slides, clicking the diagram (or the ⛶ button, kept for discoverability) opens it full size in a new tab — see `openMermaidInNewTab` in `templates/slide-deck.html`.

```html
<section class="slide slide--diagram">
  <h2 class="slide__heading reveal">Diagram Title</h2>
  <div class="mermaid-wrap reveal" style="flex:1; min-height:0;">
    <div class="zoom-controls">
      <button onclick="openDiagramFullscreen(this)" title="Open full size in new tab" aria-label="Open full size in new tab">&#x26F6;</button>
    </div>
    <pre class="mermaid">
      graph TD
        A --> B
    </pre>
  </div>
</section>
```

```css
.slide--diagram {
  padding: clamp(24px, 4vh, 48px) clamp(24px, 4vw, 60px);
}

.slide--diagram .slide__heading {
  margin-bottom: clamp(8px, 1.5vh, 20px);
}

.slide--diagram .mermaid-wrap {
  border-radius: 12px;
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide--diagram .mermaid-wrap .mermaid {
  transform-origin: center center;
}
```

**Auto-fit SVG to container.** Mermaid renders SVGs at fixed intrinsic dimensions with an inline `max-width`, which leaves diagrams either tiny inside a large slide or overflowing a short one. The `autoFit()` function (see above) handles this at runtime. Keep the CSS as a belt-and-suspenders fallback — capping **both** axes, so a tall diagram scales down instead of running off the bottom of the slide:

```css
.slide--diagram .mermaid svg {
  width: auto !important;
  height: auto !important;
  max-width: 100% !important;
  max-height: 100% !important;
}

.slide--diagram .mermaid {
  max-width: 100%;
  max-height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

A slide is a fixed viewport with no scrolling, so an overflowing diagram is unrecoverable for the reader — unlike a scrollable page, there's nowhere to scroll to see the rest. If a diagram only becomes legible at a size that overflows, it belongs on two slides or in the hybrid pattern, not scaled up.

**Mermaid overrides for presentation scale** (add alongside the standard Mermaid CSS overrides from `mermaid.md`):

```css
.slide--diagram .mermaid .nodeLabel {
  font-size: 18px !important;
}

.slide--diagram .mermaid .edgeLabel {
  font-size: 14px !important;
}

.slide--diagram .mermaid .node rect,
.slide--diagram .mermaid .node circle,
.slide--diagram .mermaid .node polygon {
  stroke-width: 2px;
}

.slide--diagram .mermaid .edge-pattern-solid {
  stroke-width: 2px;
}
```

### CSS Pipeline Slide

For simple linear flows (build steps, deployment stages, data pipelines) where Mermaid would render too small. CSS cards with arrow connectors give full control over sizing and fill the viewport naturally. Each step card expands to fill available space via `flex: 1`.

```html
<section class="slide" style="background-image:radial-gradient(...);">
  <p class="slide__label reveal">Pipeline Label</p>
  <h2 class="slide__heading reveal">Pipeline Title</h2>
  <div class="pipeline reveal">
    <div class="pipeline__step" style="border-top-color:var(--accent);">
      <div class="pipeline__num">01</div>
      <div class="pipeline__name">Step Name</div>
      <div class="pipeline__desc">What this step produces or does</div>
      <div class="pipeline__file">output-file.md</div>
    </div>
    <div class="pipeline__arrow">
      <svg viewBox="0 0 24 24" width="20" height="20"><path d="M5 12h14m-4-4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </div>
    <div class="pipeline__step"> ... </div>
    <!-- repeat step + arrow pairs -->
  </div>
</section>
```

```css
.pipeline {
  display: flex;
  align-items: stretch;
  gap: 0;
  flex: 1;
  min-height: 0;
  margin-top: clamp(12px, 2vh, 24px);
}

.pipeline__step {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 3px solid var(--accent);
  border-radius: 10px;
  padding: clamp(14px, 2.5vh, 28px) clamp(12px, 1.5vw, 22px);
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow-wrap: break-word;
}

.pipeline__num {
  font-size: clamp(10px, 1.2vw, 13px);
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 1px;
}

.pipeline__name {
  font-size: clamp(16px, 2vw, 24px);
  font-weight: 700;
  margin: clamp(4px, 0.8vh, 8px) 0;
}

.pipeline__desc {
  font-size: clamp(12px, 1.3vw, 16px);
  color: var(--text-dim);
  line-height: 1.5;
  flex: 1;
}

.pipeline__file {
  font-size: clamp(10px, 1.1vw, 12px);
  color: var(--accent);
  background: var(--accent-dim);
  padding: 3px 8px;
  border-radius: 4px;
  margin-top: clamp(8px, 1.5vh, 16px);
  align-self: flex-start;
}

.pipeline__arrow {
  display: flex;
  align-items: center;
  padding: 0 clamp(3px, 0.4vw, 6px);
  color: var(--accent);
  flex-shrink: 0;
  opacity: 0.4;
}

@media (max-width: 768px) {
  .pipeline {
    flex-direction: column;
    /* Stacked, 5–6 cards are taller than the slide, and the slide is
       overflow: hidden — the last steps would simply be gone, with no scroll
       and no arrow to reveal them. The pipeline scrolls itself instead;
       overscroll-behavior keeps that scroll from snapping the deck. */
    overflow-y: auto;
    overscroll-behavior: contain;
  }
  .pipeline__step { flex: 0 0 auto; }
  .pipeline__arrow { justify-content: center; padding: 4px 0; transform: rotate(90deg); }
}
```

Each `.pipeline__step` uses `flex: 1` to fill available width equally, and the pipeline container itself uses `flex: 1` to fill available vertical space in the slide. Step cards stretch to fill, so the content isn't floating in empty space. The `.pipeline__file` badge at the bottom anchors each card and adds a practical detail. Max 5–6 steps — beyond that, split across two slides.

**Stacked pipelines must not clip.** Horizontally, 6 steps fit; stacked at ≤768px they don't, and a fixed-height slide has no recovery — the reader can't tell that steps 5 and 6 ever existed. Preferred fix is content-side: 3 steps per slide in the stacked case, continued on a second slide, which keeps the "a slide never scrolls" rule intact. The contained scroll above is the fallback for a pipeline you can't split, and it's the same carve-out wide tables and diagrams already take.

### Dashboard Slide

KPI cards at presentation scale (48–64px hero numbers). Mini-charts via Chart.js or SVG sparklines. Max 6 KPIs.

```html
<section class="slide slide--dashboard">
  <h2 class="slide__heading reveal">Metrics Overview</h2>
  <div class="slide__kpis">
    <div class="slide__kpi reveal">
      <div class="slide__kpi-val" style="color:var(--accent)">247</div>
      <div class="slide__kpi-label">Lines Added</div>
    </div>
    <!-- more KPI cards -->
  </div>
</section>
```

```css
.slide--dashboard .slide__kpis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(140px, 20vw, 220px), 1fr));
  gap: clamp(12px, 2vw, 24px);
}

.slide__kpi {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: clamp(16px, 3vh, 32px) clamp(16px, 2vw, 24px);
  min-width: 0;
  overflow: hidden;
}

.slide__kpi-val {
  font-size: clamp(36px, 6vw, 64px);
  font-weight: 800;
  letter-spacing: -1.5px;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.slide__kpi-label {
  font-family: var(--font-mono);
  font-size: clamp(9px, 1.2vw, 13px);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-dim);
  margin-top: 8px;
}
```

**KPI hero values should be short** — numbers, percentages, 1–3 word labels. Ideal length is 1–6 characters at hero scale. Longer strings like `store=false` break the layout at 64px. If you must show a longer value, put it in the label or body text instead. The `autoFit()` function (see below) will scale down overflows as a safety net.

### Table Slide

18–20px cell text for projection readability. Max 8 rows per slide — overflow paginates to the next slide. Stronger alternating row contrast than page tables.

```html
<section class="slide slide--table">
  <h2 class="slide__heading reveal">Data Title</h2>
  <div class="table-wrap reveal" style="flex:1; min-height:0;">
    <div class="table-scroll">
      <table class="data-table"> ... </table>
    </div>
  </div>
</section>
```

```css
.slide--table {
  padding: clamp(24px, 4vh, 48px) clamp(24px, 4vw, 60px);
}

.slide--table .data-table {
  font-size: clamp(14px, 1.8vw, 20px);
}

.slide--table .data-table th {
  font-size: clamp(10px, 1.3vw, 14px);
  padding: clamp(8px, 1.5vh, 14px) clamp(12px, 2vw, 20px);
}

.slide--table .data-table td {
  padding: clamp(10px, 1.5vh, 16px) clamp(12px, 2vw, 20px);
}
```

### Code Slide

18px mono on a recessed dark background. Max 10 lines. Floating filename label. Centered on the viewport for focus.

```html
<section class="slide slide--code">
  <h2 class="slide__heading reveal">What Changed</h2>
  <div class="slide__code-block reveal">
    <span class="slide__code-filename">worker.ts</span>
    <pre><code>function processQueue(items) {
  // highlighted code here
}</code></pre>
  </div>
</section>
```

```css
.slide--code {
  align-items: center;
}

.slide__code-block {
  background: var(--code-bg, #1a1a2e);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: clamp(24px, 4vh, 48px) clamp(24px, 4vw, 48px);
  max-width: 900px;
  width: 100%;
  position: relative;
}

/* 11px on a solid accent fill. --bg works as ink only when --accent is the
   bright tone (dark themes); on a light theme --bg is cream and lands at ~3:1.
   Use the fill/on-fill pair so it holds in both. */
.slide__code-filename {
  position: absolute;
  top: -12px;
  left: 24px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 4px;
  background: var(--accent-fill, var(--accent));
  color: var(--accent-on-fill, var(--bg));
}

.slide__code-block pre {
  margin: 0;
  overflow-x: auto;
}

.slide__code-block code {
  font-family: var(--font-mono);
  font-size: clamp(14px, 1.6vw, 18px);
  line-height: 1.7;
  color: var(--code-text, #e6edf3);
}
```

### Quote Slide

36–48px serif with dramatic line-height. Oversized quotation mark as SVG or typographic decoration. Generous whitespace is the design.

```html
<section class="slide slide--quote">
  <div class="slide__quote-mark reveal">&ldquo;</div>
  <blockquote class="reveal">
    The best code is the code you don't have to write.
  </blockquote>
  <cite class="reveal">&mdash; Someone Wise</cite>
</section>
```

```css
.slide--quote {
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: clamp(60px, 10vh, 120px) clamp(60px, 12vw, 200px);
}

/* The glyph sits in the top half of its box, so line-height: 0.5 trims the
   empty space under it and the negative margin closes what's left. Both are
   fractions of the type size, not pixels — a px value tuned at the clamp's
   80px minimum leaves a 45px hole at 180px. */
.slide__quote-mark {
  font-size: clamp(80px, 14vw, 180px);
  line-height: 0.5;
  opacity: 0.08;
  font-family: Georgia, serif;
  pointer-events: none;
  margin-bottom: -0.25em;
}

.slide--quote blockquote {
  font-size: clamp(24px, 4vw, 48px);
  font-weight: 400;
  line-height: 1.35;
  font-style: italic;
  margin: 0;
}

.slide--quote cite {
  font-family: var(--font-mono);
  font-size: clamp(11px, 1.4vw, 14px);
  font-style: normal;
  margin-top: clamp(16px, 3vh, 32px);
  display: block;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-dim);
}
```

### Full-Bleed Slide

Background image (surf-generated or CSS gradient) dominates the viewport. Text overlay with gradient scrim ensuring contrast. Zero slide padding.

**This slide type is where readability fails most often.** Light text is committed up front, then the backdrop underneath it varies — a photo, a gradient, or nothing if the image fails to load. Three rules make it safe:

1. **The scrim is mandatory, not optional.** It is the only thing guaranteeing contrast over an image whose brightness you can't predict. Never ship a bleed slide without it.
2. **The gradient fallback is built from deep surface tones, never from `var(--accent)`.** An accent gradient under white text is the "white on pale green" failure in its purest form: Terminal Mono's `#50fa7b` measures **1.4:1**, Midnight Editorial's gold **2.2:1**, and a bright coral or amber lands around 2–3:1. Accents are ink on these slides, not ground.
3. **`.slide__bg` carries an opaque dark fallback color** so a failed image load leaves dark ground rather than the page background — which, on a light theme, would strand white text on cream.

```html
<section class="slide slide--bleed">
  <div class="slide__bg" style="background-image:url('data:image/png;base64,...')"></div>
  <div class="slide__scrim"></div>
  <div class="slide__content">
    <h2 class="slide__heading reveal">Headline Over Image</h2>
    <p class="slide__subtitle reveal">Supporting text</p>
  </div>
</section>
```

```css
.slide--bleed {
  padding: 0;
  justify-content: flex-end;
}

.slide__bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  /* Opaque dark fallback: if the image 404s, the light text still has ground */
  background-color: #14181f;
  z-index: 0;
}

/* Strongest where the text sits. Text is bottom-anchored, so the scrim is too. */
.slide__scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.78) 0%, rgba(0, 0, 0, 0.45) 35%, rgba(0, 0, 0, 0.1) 70%, transparent 100%);
  z-index: 1;
}

.slide--bleed .slide__content {
  position: relative;
  z-index: 2;
  padding: clamp(40px, 6vh, 80px) clamp(40px, 8vw, 120px);
  color: #f7f8fa;   /* near-white, not pure #fff */
}

/* Secondary text on a bleed slide: 0.7 alpha white over a 0.78 scrim still
   clears 4.5:1. Don't drop below 0.65 — and never use --text-dim here, since
   it's tuned for the page background, not for a photograph. */
.slide--bleed .slide__heading { color: #f7f8fa; }
.slide--bleed .slide__subtitle,
.slide--bleed .slide__label { color: rgba(247, 248, 250, 0.72); }

/* When no generated image: a deep, low-chroma gradient — NOT the accent.
   The accent appears as a hairline or a small mark on top, where it's ink. */
.slide__bg--gradient {
  background: linear-gradient(135deg, #0a1122 0%, #131c33 45%, #1d2a4a 100%);
}

/* If the aesthetic wants the accent hue in the ground, mix it DOWN into
   near-black rather than using it at full strength. */
.slide__bg--gradient-accent {
  background: linear-gradient(135deg,
    color-mix(in srgb, var(--accent) 18%, #0b0e14) 0%,
    color-mix(in srgb, var(--accent) 30%, #0b0e14) 100%);
}
```

**Light-ground bleed slides** are fine as a deliberate choice — a pale photograph or paper texture — but then the ink flips too. Swap the scrim to a light one and set the text in `--text-bright`; don't leave white text on a light backdrop and hope the scrim saves it:

```css
.slide--bleed-light .slide__scrim {
  background: linear-gradient(to top, rgba(250, 248, 244, 0.85) 0%, rgba(250, 248, 244, 0.4) 45%, transparent 100%);
}
.slide--bleed-light .slide__content,
.slide--bleed-light .slide__heading { color: var(--text-bright); }
```

## Decorative SVG Elements

Inline SVG accents lift slides from functional to editorial. Use sparingly — one or two per slide, never on every slide.

### Corner Accent

```html
<!-- Top-right corner mark -->
<svg class="slide__decor slide__decor--corner" width="120" height="120" viewBox="0 0 120 120">
  <line x1="120" y1="0" x2="120" y2="40" stroke="var(--accent)" stroke-width="2" opacity="0.2"/>
  <line x1="80" y1="0" x2="120" y2="0" stroke="var(--accent)" stroke-width="2" opacity="0.2"/>
</svg>
```

```css
.slide__decor {
  position: absolute;
  pointer-events: none;
  z-index: 0;
}

.slide__decor--corner {
  top: 0;
  right: 0;
}
```

### Section Divider Mark

```html
<!-- Horizontal rule with diamond -->
<svg class="slide__decor slide__decor--divider" width="200" height="20" viewBox="0 0 200 20">
  <line x1="0" y1="10" x2="85" y2="10" stroke="var(--accent)" stroke-width="1" opacity="0.3"/>
  <rect x="92" y="3" width="14" height="14" transform="rotate(45 99 10)" fill="none" stroke="var(--accent)" stroke-width="1" opacity="0.3"/>
  <line x1="115" y1="10" x2="200" y2="10" stroke="var(--accent)" stroke-width="1" opacity="0.3"/>
</svg>
```

### Geometric Background Pattern

```css
/* Faint grid dots behind a slide.
   Uses --pattern (not --border), and fades out where the text sits — a dot
   field running straight through 22px bullet copy is legible as dots, which
   means it's competing with the words. */
.slide--with-grid::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, var(--pattern) 1px, transparent 1px);
  background-size: 32px 32px;
  -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 50%, transparent 25%, #000 75%);
  mask-image: radial-gradient(ellipse 70% 60% at 50% 50%, transparent 25%, #000 75%);
  pointer-events: none;
  z-index: 0;
}
```

Dot fields are the safe pattern for slides — they break up flatness without producing continuous lines through the text. **Ruled and diagonal line patterns don't belong behind slide copy at all**: at presentation scale the lines are as thick as the letter strokes. If a deck's aesthetic needs linework, confine it to a border, a corner mark, or a panel the text doesn't sit on.

### Per-Slide Background Variation

Vary gradient direction and accent glow position across slides to create visual rhythm. Don't use a uniform background for every slide.

```css
/* Vary these per slide via inline style or nth-child */
.slide:nth-child(odd) {
  background-image: radial-gradient(ellipse at 20% 80%, var(--accent-dim) 0%, transparent 50%);
}

.slide:nth-child(even) {
  background-image: radial-gradient(ellipse at 80% 20%, var(--accent-dim) 0%, transparent 50%);
}
```

## Proactive Imagery

Slides should reach for visuals before defaulting to text alone. If a slide could be more compelling with an image, chart, or diagram, add one.

**surf-cli integration:** Check `which surf` at the start of every slide deck generation. If available, **generate 2–4 images minimum** for any deck over 10 slides. This is not optional when surf is available — a deck with AI-generated imagery is dramatically more compelling than one with only CSS gradients. Target these slides in priority order:

1. **Title slide** (always): background image that sets the deck's visual tone. Match the topic and palette. Use `--aspect-ratio 16:9`. Prompt example: "abstract dark geometric pattern with green accent lines, technical and minimal" for Terminal Mono preset.
2. **Full-bleed slide** (always if deck has one): immersive background for the deck's visual anchor moment. Style should match the preset — photo-realistic for Midnight Editorial, abstract/geometric for Swiss Clean, circuit-board or terminal aesthetic for Terminal Mono.
3. **Content slides with conceptual topics** (1–2 if the deck has room): illustration in the `.slide__aside` area for slides about abstract concepts. Use `--aspect-ratio 1:1`.

**Generate images before writing HTML** so they're ready to embed. The workflow:

```bash
# Check availability
which surf

# Generate (one per target slide)
surf gemini "descriptive prompt matching deck palette" --generate-image /tmp/hc-slide-title.png --aspect-ratio 16:9

# Base64 encode for self-containment (macOS)
TITLE_IMG=$(base64 -i /tmp/hc-slide-title.png)
# Linux: TITLE_IMG=$(base64 -w 0 /tmp/hc-slide-title.png)

# Embed in the slide
# <div class="slide__bg" style="background-image:url('data:image/png;base64,${TITLE_IMG}')"></div>

# Clean up
rm /tmp/hc-slide-title.png
```

**Prompt craft for slides:** Be specific about style, dominant colors, and mood. Pull colors from the preset's CSS variables. Examples:
- Terminal Mono: "dark abstract circuit board pattern, green (#50fa7b) traces on near-black (#0a0e14), minimal, technical"
- Midnight Editorial: "deep navy abstract composition, warm gold accent light, cinematic depth of field, premium editorial feel"
- Warm Signal: "warm cream textured paper with terracotta geometric accents, confident modern design"

**When surf fails or isn't available:** Degrade gracefully to CSS gradients and SVG decorations. Use the `.slide__bg--gradient` pattern with bold `linear-gradient` or `radial-gradient` backgrounds. The deck should stand on its own visually without generated images — they enhance, they don't carry. Note the fallback in an HTML comment (`<!-- surf unavailable, using CSS gradient fallback -->`) so future edits know to retry.

**Inline data visualizations:** Proactively add SVG sparklines next to numbers, mini-charts on dashboard slides, and small Mermaid diagrams on split slides even when not explicitly requested. A number with a sparkline next to it tells a better story than a number alone.

**When to skip images:** If surf isn't available, degrade gracefully — use CSS gradients and SVG decorations instead. Never error on missing surf. Pure structural or data-heavy decks (code reviews, table comparisons) may not need generated images.

## Compositional Variety

Consecutive slides must vary their spatial approach. Three centered slides in a row means push one off-axis.

**Composition patterns to alternate between:**
- Centered (title slides, quotes)
- Left-heavy: content on the left 60%, breathing room on the right
- Right-heavy: content on the right 60%, visual or whitespace on the left
- Edge-aligned: content pushed to bottom or top, large empty space opposite
- Split: two distinct panels filling the viewport
- Full-bleed: background dominates, minimal overlaid text

The agent should plan the slide sequence considering layout rhythm, not just content order. When outlining a deck, assign a composition to each slide before writing HTML.

## Presentation Readability

Slides get projected, screen-shared, viewed at distance. Design accordingly:

- **Minimum body text: 16px.** Nothing smaller except labels and captions.
- **One focal point per slide.** Not three competing elements.
- **Higher contrast than pages — 7:1 for body copy where you can get it.** A projector's black point is grey, a shared screen is recompressed, and the back row is 20 feet away; all three eat contrast that looked fine on your monitor. 4.5:1 is the floor, not the target.
- **Bullets and body copy use `--text`.** `--text-dim` is for captions, sources, and slide labels — never for the substance of the slide. A deck where the only content is set in dim grey is unreadable at distance even when it technically passes.
- **No light ink on bright fills.** Check every solid-filled badge, pill, KPI chip, and bleed slide. This is the failure that survives to delivery most often, because it looks intentional in a thumbnail.
- **Nothing important on a patterned ground.** Dot fields are fine behind slides; ruled and diagonal lines are not, at this type scale.
- **Nav chrome opacity.** Dots and progress bar must be visible on any slide background (light or dark) without being distracting — they're controls, so they need 3:1, not decoration alpha. Use the background-tint approach from the Nav Chrome section.
- **Simpler Mermaid diagrams.** Max 8–10 nodes, 18px+ labels, 2px+ edges. The diagram should be readable at presentation distance; click-to-expand remains available for detail inspection.

## Content Density Limits

Each slide must fit in exactly 100dvh. If content exceeds these limits, the agent splits across multiple slides — the slide itself never scrolls. A contained scroll region *inside* a slide (a wide table, a stacked pipeline on a narrow viewport) is the one carve-out, and only where the alternative is content clipped away with no way to reach it.

| Slide type | Max content |
|-----------|-------------|
| Title | 1 heading + 1 subtitle |
| Section Divider | 1 number + 1 heading + optional subhead |
| Content | 1 heading + 5–6 bullets (max 2 lines each) |
| Split | 1 heading + 2 panels, each follows its inner type's limits |
| Diagram | 1 heading + 1 Mermaid diagram (max 8–10 nodes) |
| Dashboard | 1 heading + 6 KPI cards. Hero values ≤6 chars (numbers, %, short labels). Longer strings belong in the label row. |
| Table | 1 heading + 8 rows; overflow paginates to next slide |
| Code | 1 heading + 10 lines of code |
| Quote | 1 short quote (~25 words / ~150 chars max) + 1 attribution. Longer quotes are content slides, not quote slides. |
| Full-Bleed | 1 heading + 1 subtitle over background |

## Responsive Height Breakpoints

Height-based scaling is more critical for slides than width. Each breakpoint progressively reduces padding, font sizes, and hides decorative elements.

```css
/* Compact viewports */
@media (max-height: 700px) {
  .slide {
    padding: clamp(24px, 4vh, 40px) clamp(32px, 6vw, 80px);
  }
  .slide__display { font-size: clamp(36px, 8vw, 72px); }
  .slide--divider .slide__number { font-size: clamp(80px, 16vw, 160px); }
}

/* Small tablets / landscape phones */
@media (max-height: 600px) {
  .slide__decor { display: none; } /* hide decorative SVGs */
  .slide--quote { padding: clamp(32px, 6vh, 60px) clamp(40px, 8vw, 100px); }
  .slide__quote-mark { display: none; }
}

/* Aggressive: landscape phones */
@media (max-height: 500px) {
  .slide {
    padding: clamp(16px, 3vh, 24px) clamp(24px, 5vw, 48px);
  }
  /* A column of 24px hit areas doesn't fit in 500px of height, and shrinking
     it back under the target floor just recreates the untappable dot. Drop the
     column instead — it only ever duplicated swipe, scroll, and arrow keys.
     The counter stays: it's the remaining "where am I" affordance, so never
     hide it in the same breakpoint. */
  .deck-dots { display: none; }
  .slide__display { font-size: clamp(28px, 7vw, 48px); }
}

/* Width breakpoint for grids */
@media (max-width: 768px) {
  .slide--content .slide__inner { grid-template-columns: 1fr; }

  /* The aside stacks under the text, it doesn't disappear. Proactive Imagery
     sends real generated illustrations to this slot, and `display: none` on a
     one-column layout deletes them for every phone reader. Bound the height so
     the image can't push the bullets off a fixed-height slide. */
  .slide--content .slide__aside {
    max-height: 26vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .slide--content .slide__aside > * {
    max-height: 26vh;
    max-width: 100%;
    height: auto;
    object-fit: contain;
  }

  .slide--split .slide__panels { grid-template-columns: 1fr; }
  .slide--dashboard .slide__kpis { grid-template-columns: repeat(2, 1fr); }
}
```

## Curated Presets

Starting points the agent can riff on. Each defines a font pairing, palette, and background treatment. The agent adapts these to the content — different decks with the same preset should still feel distinct.

Every preset carries the full token set from "The Contrast Contract" in `css-patterns.md`: `--accent` is the **ink** tone, `--accent-fill` is the tone that goes *under* text, and `--accent-on-fill` is the ink for that fill. When riffing, keep the three-part shape — swapping in a prettier `--accent` without adjusting the fill is how a deck ends up with white text on a pale ground.

### Midnight Editorial

Deep navy, serif display, warm gold accents. Cinematic, premium. Dark-first.

```css
:root {
  --font-body: 'Spectral', Georgia, serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', monospace;
  --bg: #0f1729;
  --surface: #162040;
  --surface2: #1d2b52;
  --surface-elevated: #243362;
  --border: rgba(200, 180, 140, 0.08);
  --border-bright: rgba(200, 180, 140, 0.16);
  --text: #e8e4d8;
  --text-bright: #f8f6ef;
  --text-dim: #a49e8d;
  --pattern: rgba(232, 228, 216, 0.04);
  --accent: #d4a73a;          /* bright ink on navy — 8.3:1 */
  --accent-fill: #6b5210;     /* deep gold ground for light ink */
  --accent-on-fill: #fdf8e8;  /* 8.0:1 on the fill (white on #d4a73a is 2.2:1) */
  --accent-dim: rgba(212, 167, 58, 0.1);
  --code-bg: #0a0f1e;
  --code-text: #d4d0c4;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #faf8f2;
    --surface: #fffefa;
    --surface2: #f5f0e6;
    --surface-elevated: #fffdf5;
    --border: rgba(30, 30, 50, 0.08);
    --border-bright: rgba(30, 30, 50, 0.16);
    --text: #1a1814;
    --text-bright: #0d0b08;
    --text-dim: #6d675c;      /* 5.5:1 — #7a7468 was 4.4:1, just under */
    --pattern: rgba(26, 24, 20, 0.045);
    --accent: #8a6508;        /* 5.3:1 — #b8860b is only 3.3:1 as text */
    --accent-fill: #8a6508;
    --accent-on-fill: #fdf8e8;
    --accent-dim: rgba(138, 101, 8, 0.09);
    --code-bg: #2a2520;
    --code-text: #e8e4d8;
  }
}
```

Background: radial gold glow at top center. Decorative corner marks in gold. Title slides use dramatic serif at max scale.

### Warm Signal

Cream paper, bold sans, terracotta/coral accents. Confident and modern. Light-first.

```css
:root {
  --font-body: 'Schibsted Grotesk', system-ui, sans-serif;
  --font-mono: 'Azeret Mono', 'SF Mono', monospace;
  --bg: #faf6f0;
  --surface: #ffffff;
  --surface2: #f5ece0;
  --surface-elevated: #fffdf5;
  --border: rgba(60, 40, 20, 0.08);
  --border-bright: rgba(60, 40, 20, 0.16);
  --text: #2c2a25;
  --text-bright: #16150f;
  --text-dim: #6f685d;        /* 5.5:1 — #7c756a was 4.2:1 */
  --pattern: rgba(44, 42, 37, 0.045);
  --accent: #c2410c;          /* 4.9:1 as ink on cream */
  --accent-fill: #c2410c;
  --accent-on-fill: #fff5ef;  /* 4.9:1 on the fill */
  --accent-dim: rgba(194, 65, 12, 0.08);
  --code-bg: #2c2520;
  --code-text: #f5ece0;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1c1916;
    --surface: #262220;
    --surface2: #302b28;
    --surface-elevated: #3a3430;
    --border: rgba(200, 180, 160, 0.08);
    --border-bright: rgba(200, 180, 160, 0.16);
    --text: #f0e8dc;
    --text-bright: #fdf9f3;
    --text-dim: #a09888;
    --pattern: rgba(240, 232, 220, 0.04);
    --accent: #e85d2a;          /* bright ink on warm near-black */
    --accent-fill: #8f3311;     /* deep terracotta ground (white on #e85d2a is 3.5:1) */
    --accent-on-fill: #fff5ef;
    --accent-dim: rgba(232, 93, 42, 0.1);
    --code-bg: #141210;
    --code-text: #f0e8dc;
  }
}
```

Background: warm radial glow at bottom left. Full 1px terracotta-tinted borders on key cards (never side-stripes). Section divider numbers in ultra-light coral.

### Terminal Mono

Dark, monospace everything, green/cyan accents, faint grid. Developer-native. Dark-first.

```css
:root {
  --font-body: 'Geist Mono', 'SF Mono', Consolas, monospace;
  --font-mono: 'Geist Mono', 'SF Mono', Consolas, monospace;
  --bg: #0a0e14;
  --surface: #12161e;
  --surface2: #1a1f2a;
  --surface-elevated: #222836;
  --border: rgba(80, 250, 123, 0.06);
  --border-bright: rgba(80, 250, 123, 0.12);
  --text: #c8d6e5;
  --text-bright: #eaf2fa;
  --text-dim: #8a9bab;        /* 6.5:1 — #5a6a7a was 3.5:1 on this near-black */
  --pattern: rgba(200, 214, 229, 0.04);
  --accent: #50fa7b;          /* bright ink — 14:1 on near-black */
  --accent-fill: #0d5c2c;     /* deep green ground; white on #50fa7b is 1.4:1 */
  --accent-on-fill: #e9fff0;  /* 8.6:1 on the fill */
  --accent-dim: rgba(80, 250, 123, 0.08);
  --code-bg: #060a10;
  --code-text: #c8d6e5;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #f4f6f8;
    --surface: #fdfeff;
    --surface2: #eaecf0;
    --surface-elevated: #f8f9fa;
    --border: rgba(0, 80, 40, 0.08);
    --border-bright: rgba(0, 80, 40, 0.16);
    --text: #1a2332;
    --text-bright: #0b1119;
    --text-dim: #566475;      /* 6.0:1 on --surface */
    --pattern: rgba(26, 35, 50, 0.045);
    --accent: #0d7a3e;        /* 5.2:1 as ink */
    --accent-fill: #0d7a3e;
    --accent-on-fill: #f0fff6;
    --accent-dim: rgba(13, 122, 62, 0.08);
    --code-bg: #1a2332;
    --code-text: #c8d6e5;
  }
}
```

Background: faint dot grid. Everything in mono. Title slides use large weight-400 mono instead of bold display. Code slides feel native.

**Terminal Mono's trap:** `#50fa7b` is a superb ink and a terrible ground. It's the brightest accent in any preset here, so white or light text over it measures **1.4:1** — the single worst combination the skill can produce. Keep it for text, borders, small marks, and dark-ink-on-bright badges (`background: var(--accent); color: var(--bg)` is 14:1 and looks great); use `--accent-fill` whenever light ink has to sit on top.

### Swiss Clean

White, geometric sans, single bold accent, visible grid. Minimal and precise. Light-first.

```css
:root {
  --font-body: 'Familjen Grotesk', system-ui, sans-serif;
  --font-mono: 'Fira Code', 'SF Mono', monospace;
  /* Swiss means precise, not literally #fff/#000 — these carry a 1% cool tint
     toward the blue accent, which reads as "clean" rather than "unset". */
  --bg: #fdfdfe;
  --surface: #f7f8fa;
  --surface2: #eff1f4;
  --surface-elevated: #ffffff;
  --border: rgba(10, 12, 20, 0.09);
  --border-bright: rgba(10, 12, 20, 0.17);
  --text: #101318;
  --text-bright: #05070a;
  --text-dim: #5c6472;        /* 5.9:1 on --surface */
  --pattern: rgba(16, 19, 24, 0.05);
  --accent: #0046d1;          /* 7.0:1 — #0055ff is 4.9:1 and vibrates on white */
  --accent-fill: #0046d1;
  --accent-on-fill: #f2f6ff;  /* 6.7:1 on the fill */
  --accent-dim: rgba(0, 70, 209, 0.07);
  --code-bg: #18181b;
  --code-text: #e4e4e7;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0f1013;
    --surface: #191b1f;
    --surface2: #212429;
    --surface-elevated: #2a2d33;
    --border: rgba(240, 244, 255, 0.09);
    --border-bright: rgba(240, 244, 255, 0.17);
    --text: #f0f1f4;
    --text-bright: #fbfcfe;
    --text-dim: #9aa2b0;      /* 6.9:1 — #888 on #111 is 5.9:1 but drops on cards */
    --pattern: rgba(240, 241, 244, 0.04);
    --accent: #7dabff;        /* bright ink for dark ground */
    --accent-fill: #1e40af;   /* deep blue ground (white on #3b82f6 is 3.7:1) */
    --accent-on-fill: #eef4ff;
    --accent-dim: rgba(125, 171, 255, 0.1);
    --code-bg: #0a0a0c;
    --code-text: #e4e4e7;
  }
}
```

Background: clean white or near-black, no gradients. Visible grid lines (the `--with-grid` pattern). Tight geometric layouts. Single accent color used sparingly for emphasis. Data-heavy and analytical content shines here.
