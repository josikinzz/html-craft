# CSS Patterns for Diagrams

Reusable patterns for layout, connectors, theming, and visual effects in self-contained HTML diagrams.

## The Contrast Contract

Read this before picking a single color. Almost every unreadable generated page traces to one of three mistakes, and all three are structural — they survive any amount of eyeballing.

**1. One accent doing two jobs.** A color bright enough to read as text on a dark page is far too bright to sit *under* white text. `#50fa7b`, `#22d3ee`, `#fb923c`, `#d4a73a`, `#34d399` all measure **1.4–2.7:1** against white. That is the "white text on pale green" failure. Split every accent in two:

| Token | Job | Requirement |
|---|---|---|
| `--accent` | **ink** — text, icons, borders, chart strokes | ≥4.5:1 on `--surface` |
| `--accent-fill` | **fill** — a background with text on top | ≥4.5:1 against `--accent-on-fill` |
| `--accent-on-fill` | the ink that sits on `--accent-fill` | near-black for bright fills, near-white for deep fills |
| `--accent-dim` | 8–12% tint for wash backgrounds | text on it must still be `--accent`, and `--accent` must clear 4.5:1 over the *tinted* result |

The reflex to avoid: `background: var(--accent); color: #fff`. It passes in whichever theme you happened to look at and fails in the other.

**2. Small type in weak color.** Badges, chips, tags, and captions run 10–12px, where contrast matters *more*, not less. On a light surface, the popular mid-tone semantics all fail as text: `#059669` (3.7:1), `#0891b2` (3.6:1), `#d97706` (3.1:1), `#ef4444` (3.3:1). Drop a step: `#15803d`, `#0f766e`, `#b45309`, `#dc2626` all clear 4.5:1 against white while reading as the same hue.

**3. `--text-dim` used as a body color.** Dim is for provenance stamps, timestamps, and captions — information a reader can skip. Bullets, card descriptions, and table cells go in `--text`; build hierarchy with size and weight, not by fading the words. `--text-dim` still has to clear 4.5:1 on every surface it lands on.

**Floors:** 4.5:1 for anything read in sequence and for all text under ~19px; 3:1 for display type 24px+ and for meaningful non-text (borders, icons, focus rings, chart strokes). Decorative-only marks (watermark numerals, oversized quote glyphs) are exempt precisely because they carry no information — keep them at or below 0.08 opacity so they can't compete with the text over them.

**Verify, don't estimate:**

```bash
python3 ~/.claude/skills/visual-explainer/scripts/check-contrast.py ~/.agent/diagrams/page.html
```

It resolves the custom properties for both themes and reports every pair below its floor. Contrast is arithmetic — check it rather than judging it.

## Theme Setup

Always define both light and dark palettes via custom properties. Start with whichever fits the chosen aesthetic, ensure both work.

Every accent below appears three times — ink, fill, and the ink that goes on the fill. That redundancy is the point: it makes the unreadable combination impossible to write by accident.

```css
:root {
  --font-body: 'Familjen Grotesk', system-ui, sans-serif;
  --font-mono: 'Fira Code', 'SF Mono', Consolas, monospace;

  /* Neutrals tinted toward the accent hue — never pure #fff/#000 */
  --bg: #f5f8f9;
  --surface: #fcfdfe;
  --surface-elevated: #fdfeff;
  --border: rgba(0, 0, 0, 0.08);
  --border-bright: rgba(0, 0, 0, 0.15);
  --text: #14202b;        /* body copy — 4.5:1 minimum, and it should beat that comfortably */
  --text-bright: #070f16; /* headings and emphasis, one step darker than --text */
  --text-dim: #5b6672;    /* captions/provenance ONLY — still clears 4.5:1 on --surface */

  /* Decoration alpha — deliberately separate from --border.
     Border alpha is tuned for a crisp 1px edge; reused at 24-48px repeat
     spacing it reads as an aggressive ruled grid behind the content. */
  --pattern: rgba(20, 32, 43, 0.045);

  /* Accents: ink reads as text, fill sits under text, on-fill is the ink for the fill */
  --accent: #0f766e;          /* 5.5:1 on --surface  */
  --accent-fill: #0f766e;
  --accent-on-fill: #f0fdfa;  /* 5.2:1 on --accent-fill */
  --accent-dim: rgba(15, 118, 110, 0.10);

  /* Semantic accents for diagram elements — same three-part shape */
  --node-a: #0f766e;
  --node-a-dim: rgba(15, 118, 110, 0.10);
  --node-b: #15803d;
  --node-b-dim: rgba(21, 128, 61, 0.10);
  --node-c: #b45309;
  --node-c-dim: rgba(180, 83, 9, 0.10);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --surface-elevated: #1c2333;
    --border: rgba(255, 255, 255, 0.06);
    --border-bright: rgba(255, 255, 255, 0.12);
    --text: #e6edf3;
    --text-bright: #f6f9fc;
    --text-dim: #9dabb8;     /* lifted from the usual #8b949e — dim must still clear 4.5:1 */
    --pattern: rgba(230, 237, 243, 0.04);

    /* Ink flips bright on dark. Fill stays DEEP so light ink can sit on it —
       the bright ink tone is never reused as a fill. */
    --accent: #22d3ee;
    --accent-fill: #0e5b6b;
    --accent-on-fill: #ecfeff;
    --accent-dim: rgba(34, 211, 238, 0.12);
    --node-a: #22d3ee;
    --node-a-dim: rgba(34, 211, 238, 0.12);
    --node-b: #34d399;
    --node-b-dim: rgba(52, 211, 153, 0.12);
    --node-c: #fbbf24;
    --node-c-dim: rgba(251, 191, 36, 0.12);
  }
}
```

**Using a fill.** Whenever an accent becomes a background with text on it, both tokens travel together — never one without the other:

```css
/* RIGHT — the pair guarantees contrast in both themes */
.badge-solid {
  background: var(--accent-fill);
  color: var(--accent-on-fill);
}

/* WRONG — white on whatever tone --accent happens to be.
   Light theme: 3.7:1. Dark theme: 1.8:1. Both fail. */
.badge-solid {
  background: var(--accent);
  color: #fff;
}
```

If an aesthetic genuinely calls for a bright fill (a risograph spot color, a terminal green badge), keep it — but flip the ink to the palette's near-black rather than reaching for white:

```css
.badge-bright {
  background: var(--node-c);          /* #fbbf24 amber */
  color: var(--bg);                   /* near-black — 11:1, not 1.8:1 */
}
```

## Background Atmosphere

Flat backgrounds feel dead. Use subtle gradients or patterns.

Two rules govern all of them. **Patterns use `--pattern`, never `--border`** — border alpha is calibrated for a crisp 1px edge and turns into hard ruled lines when repeated. And **patterns live behind surfaces, not behind prose**: a page background may carry texture as long as the reading content sits on opaque `--surface` cards. Text floating directly over stripes is a defect regardless of how faint they are, because the lines cut through the letterforms.

Keep decoration at or below 0.06 alpha in light themes and 0.05 in dark, and keep repeat spacing at 24px or wider — tighter than that and it reads as stripes rather than texture.

```css
/* Radial glow behind focal area — the safest option, no linework at all */
body {
  background: var(--bg);
  background-image: radial-gradient(ellipse at 50% 0%, var(--accent-dim) 0%, transparent 60%);
}

/* Faint dot grid */
body {
  background-color: var(--bg);
  background-image: radial-gradient(circle, var(--pattern) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* Diagonal subtle lines — wide spacing, pattern alpha, and content must sit on cards */
body {
  background-color: var(--bg);
  background-image: repeating-linear-gradient(
    -45deg, transparent, transparent 47px,
    var(--pattern) 47px, var(--pattern) 48px
  );
}

/* Gradient mesh (pick 2-3 positioned radials) */
body {
  background: var(--bg);
  background-image:
    radial-gradient(at 20% 20%, var(--node-a-dim) 0%, transparent 50%),
    radial-gradient(at 80% 60%, var(--node-b-dim) 0%, transparent 50%);
}
```

**Dropping the pattern out behind text.** When prose has to sit on the page background rather than a card, give it its own opaque backdrop instead of turning the pattern down until it's invisible everywhere:

```css
.prose-on-pattern {
  background: var(--bg);   /* opaque — masks the body pattern behind this block */
  border-radius: 12px;
  padding: 24px 28px;
}
```

**Patterned fills inside content** — hatched "blocked time" bars, striped progress segments, cross-hatch legend swatches — are the worst offender, because they put stripes directly under a label. Keep the stripes at `--pattern` strength over a solid wash, and set the label in `--text`:

```css
/* RIGHT — texture reads, label stays on a solid wash */
.bar-blocked {
  background-color: var(--node-c-dim);
  background-image: repeating-linear-gradient(
    135deg, transparent, transparent 7px,
    var(--pattern) 7px, var(--pattern) 8px
  );
  color: var(--text);
}

/* WRONG — 6px hard stripes in a mid-tone, dim ink on top */
.bar-blocked {
  background: repeating-linear-gradient(135deg, var(--node-c), var(--node-c) 6px, transparent 6px, transparent 12px);
  color: var(--text-dim);
}
```

## Link Styling

**Never rely on browser default link colors.** The default blue (`#0000EE`) has poor contrast on dark backgrounds. Style links with `color: var(--accent)` and keep underlines for discoverability — the underline is what makes links identifiable without relying on color.

On dark backgrounds, use bright accents (`#22d3ee`, `#34d399`, `#fbbf24`). On light backgrounds, go genuinely deep — `#0f766e`, `#15803d`, `#b45309`, `#be123c`. The half-step tones that look deep enough (`#0891b2`, `#059669`, `#d97706`) all land near 3.5:1 on white and fail as body-size text.

## Section / Card Components

The fundamental building block. A colored card representing a system component, pipeline step, or data entity.

**IMPORTANT: Never use `.node` as a CSS class name.** Mermaid.js internally uses `.node` on its SVG `<g>` elements with `transform: translate(x, y)` for positioning. Any page-level `.node` styles (hover transforms, box-shadows, transitions) will leak into Mermaid diagrams and break their layout. Use `.ve-card` instead (namespaced to avoid collisions with CSS frameworks like Bootstrap/Tailwind that also use `.card`).

```css
.ve-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 20px;
  position: relative;
}

/* Colored accent variant — full tinted border + faint background wash
   (side-stripes are banned; see Anti-Patterns in SKILL.md) */
.ve-card--accent-a {
  border-color: color-mix(in srgb, var(--node-a) 45%, var(--border));
  background: color-mix(in srgb, var(--node-a) 6%, var(--surface));
}

/* --- Depth tiers: vary card depth to signal importance --- */

/* Elevated: KPIs, key sections, anything that should pop */
.ve-card--elevated {
  background: var(--surface-elevated);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
}

/* Recessed: code blocks, secondary content, detail panels */
.ve-card--recessed {
  background: color-mix(in srgb, var(--bg) 70%, var(--surface) 30%);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
  border-color: var(--border);
}

/* Hero: executive summaries, focal elements — demands attention */
.ve-card--hero {
  background: color-mix(in srgb, var(--surface) 92%, var(--accent) 8%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.04);
  border-color: color-mix(in srgb, var(--border) 50%, var(--accent) 50%);
}

/* Glass: special-occasion overlay effect (use sparingly) */
.ve-card--glass {
  background: color-mix(in srgb, var(--surface) 60%, transparent 40%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Section label (monospace, uppercase, small) */
.ve-card__label {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--node-a);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Colored dot indicator */
.ve-card__label::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}
```

## Code Blocks

Code blocks need explicit whitespace preservation and a max-height constraint. Without these, code runs together and long files overwhelm the page.

### Basic Pattern

```css
.code-block {
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.5;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  /* CRITICAL: preserve line breaks and indentation */
  white-space: pre-wrap;
  word-break: break-word;
}

/* Constrain height for long code */
.code-block--scroll {
  max-height: 400px;
  overflow-y: auto;
}
```

```html
<pre class="code-block code-block--scroll"><code>// Your code here
function example() {
  return true;
}</code></pre>
```

### With File Header

```css
.code-file {
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.code-file__header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-dim);
}

.code-file__body {
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.5;
  padding: 16px;
  background: var(--surface-elevated);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 500px;
  overflow: auto;
}
```

```html
<div class="code-file">
  <div class="code-file__header">
    <span>src/extension.ts</span>
  </div>
  <pre class="code-file__body"><code>export function activate() {
  // ...
}</code></pre>
</div>
```

### Implementation Plans: Don't Dump Full Files

For implementation plans and architecture docs, **don't display entire source files inline**. Instead:

1. **Show structure, not code:**
   ```html
   <div class="file-structure">
     <div class="file-structure__path">src/extension.ts</div>
     <ul class="file-structure__outline">
       <li><code>BOOMERANG_INSTRUCTIONS</code> — System prompt for autonomous mode</li>
       <li><code>clearState()</code> — Reset extension state</li>
       <li><code>updateStatus()</code> — Update UI status indicator</li>
       <li><code>/boomerang</code> command — Start autonomous task</li>
       <li><code>/boomerang-cancel</code> command — Cancel active task</li>
       <li><code>before_agent_start</code> hook — Inject instructions</li>
       <li><code>agent_end</code> hook — Generate summary</li>
     </ul>
   </div>
   ```

2. **Use collapsible sections for full code:**
   ```html
   <details class="collapsible">
     <summary>Full implementation (87 lines)</summary>
     <pre class="code-file__body"><code>...</code></pre>
   </details>
   ```

3. **Show key snippets only:**
   ```html
   <p>The core logic intercepts task completion:</p>
   <pre class="code-block"><code>pi.on("agent_end", async () => {
     const summary = generateSummary(workEntries);
     boomerangComplete = true;
   });</code></pre>
   ```

**Anti-patterns:**
- Displaying full source files inline (100+ lines overwhelming the page)
- Code blocks without `white-space: pre-wrap` (code runs together into unreadable wall)
- No height constraint on long code (page becomes endless scroll)

If someone needs the full file, put it in a collapsible section or link to it.

## Directory Tree

For file structures, use `<pre>` with monospace + `white-space: pre`. Tree connectors (`├──`, `└──`, `│`) only work when vertically aligned — they become noise if text wraps.

```css
.dir-tree {
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.7;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px 20px;
  overflow-x: auto;
  white-space: pre;
}

.dir-tree .ann { color: var(--text-dim); font-size: 11px; font-style: italic; }
.dir-tree .hl  { color: var(--accent); font-weight: 600; }
```

```html
<pre class="dir-tree">my-project/
├── src/
│   ├── <span class="hl">index.ts</span>       <span class="ann">— entry point</span>
│   ├── services/
│   │   └── <span class="hl">api.py</span>     <span class="ann">(142 lines)</span>
│   └── utils/
├── tests/            <span class="ann">(14 test files)</span>
└── README.md</pre>
```

For labeled trees, wrap in a card. For side-by-side comparisons, put two cards in a grid:

```css
.dir-tree-card { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
.dir-tree-card__header {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 16px; background: var(--surface); border-bottom: 1px solid var(--border);
  font-family: var(--font-mono); font-size: 11px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 1.5px;
}
.dir-tree-card .dir-tree { border: none; border-radius: 0; }

/* Side-by-side: two .dir-tree-card in a grid */
.dir-compare { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: start; }
@media (max-width: 900px) { .dir-compare { grid-template-columns: 1fr; } }
```

**Never** render tree connectors inside wrapping text (`white-space: normal`), flex children, or grid items — the vertical pipes lose alignment and the hierarchy becomes unreadable.

## Overflow Protection

Grid and flex children default to `min-width: auto`, which prevents them from shrinking below their content width. Long text, inline code badges, and non-wrapping elements will blow out containers.

### Global rules

```css
/* Every grid/flex child must be able to shrink */
.grid > *, .flex > *,
[style*="display: grid"] > *,
[style*="display: flex"] > * {
  min-width: 0;
}

/* Long text wraps instead of overflowing */
body {
  overflow-wrap: break-word;
}
```

### Side-by-side comparison panels

```css
.comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.comparison > * {
  min-width: 0;
  overflow-wrap: break-word;
}

@media (max-width: 768px) {
  .comparison { grid-template-columns: 1fr; }
}
```

### Never use `display: flex` on `<li>` for marker characters

Using `display: flex` on a list item to position a `::before` marker creates an anonymous flex item for the remaining text content. That anonymous flex item gets `min-width: auto` and you **cannot** set `min-width: 0` on anonymous boxes. Lines with many inline `<code>` badges will overflow their container with no CSS fix possible.

Use absolute positioning for markers instead:

```css
/* WRONG — causes overflow with inline code badges */
li {
  display: flex;
  align-items: baseline;
  gap: 6px;
}
li::before {
  content: '›';
  flex-shrink: 0;
}

/* RIGHT — text wraps normally */
li {
  padding-left: 14px;
  position: relative;
}
li::before {
  content: '›';
  position: absolute;
  left: 0;
}
```

### List markers overlapping container borders

By default, `list-style-position: outside` places list markers (bullets, numbers) outside the content box. When lists are inside bordered containers (cards, callout boxes), the markers can overlap or extend beyond the border.

```css
/* WRONG — markers overlap container border */
.card ol, .card ul {
  padding-left: 20px;  /* Not enough for outside markers */
}

/* RIGHT — use inside positioning */
.card ol, .card ul {
  list-style-position: inside;
}

/* OR — adequate padding for outside markers */
.card ol, .card ul {
  padding-left: 2em;  /* ~32px gives room for markers */
}

/* OR — custom markers with absolute positioning (most control) */
.card ol {
  list-style: none;
  padding-left: 0;
  counter-reset: item;
}
.card ol li {
  counter-increment: item;
  padding-left: 2em;
  position: relative;
}
.card ol li::before {
  content: counter(item) ".";
  position: absolute;
  left: 0;
  color: var(--accent);
  font-weight: 600;
}
```

**Rule of thumb:** Any `<ol>` or `<ul>` inside a bordered container needs either `list-style-position: inside` or `padding-left: 2em` minimum. The default 20px padding is not enough for outside-positioned markers.

## Mermaid Containers

The full Mermaid container pattern (centering, scaling, zoom/pan controls, diagram-shell HTML and JS) lives in [`mermaid.md`](mermaid.md), with `templates/mermaid-flowchart.html` as the canonical implementation.

## Grid Layouts

### Architecture Diagram (2-column with sidebar)
```css
.arch-grid {
  display: grid;
  grid-template-columns: 260px 1fr;
  grid-template-rows: auto;
  gap: 20px;
  max-width: 1100px;
  margin: 0 auto;
}

.arch-grid__sidebar { grid-column: 1; }
.arch-grid__main { grid-column: 2; }
.arch-grid__full { grid-column: 1 / -1; }
```

### Pipeline (horizontal steps)
```css
.pipeline {
  display: flex;
  align-items: stretch;
  gap: 0;
  overflow-x: auto;
  padding-bottom: 8px;
}

.pipeline__step {
  min-width: 130px;
  flex-shrink: 0;
}

.pipeline__arrow {
  display: flex;
  align-items: center;
  padding: 0 4px;
  color: var(--border-bright);
  font-size: 18px;
  flex-shrink: 0;
}

/* Parallel branch within a pipeline */
.pipeline__parallel {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
```

### Card Grid (dashboard / metrics)
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}
```

### Data Tables

Use real `<table>` elements for tabular data. Wrap in a scrollable container for wide tables.

```css
/* Scrollable wrapper for wide tables */
.table-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

.table-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Base table */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  line-height: 1.5;
}

/* Header */
.data-table thead {
  position: sticky;
  top: 0;
  z-index: 2;
}

.data-table th {
  background: var(--surface-elevated, var(--surface2, var(--surface)));
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-dim);
  text-align: left;
  padding: 12px 16px;
  border-bottom: 2px solid var(--border-bright);
  white-space: nowrap;
}

/* Cells */
.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
  color: var(--text);
}

/* Let text-heavy columns wrap naturally */
.data-table .wide {
  min-width: 200px;
  max-width: 500px;
}

/* Right-align numeric columns */
.data-table td.num,
.data-table th.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-family: var(--font-mono);
}

/* Alternating rows */
.data-table tbody tr:nth-child(even) {
  background: var(--accent-dim);
}

/* Row hover */
.data-table tbody tr {
  transition: background 0.15s ease;
}

.data-table tbody tr:hover {
  background: var(--border);
}

/* Last row: no bottom border (container handles it) */
.data-table tbody tr:last-child td {
  border-bottom: none;
}

/* Code inside cells */
.data-table code {
  font-family: var(--font-mono);
  font-size: 11px;
  background: var(--accent-dim);
  color: var(--accent);
  padding: 1px 5px;
  border-radius: 3px;
}

/* Secondary detail text */
.data-table small {
  display: block;
  color: var(--text-dim);
  font-size: 11px;
  margin-top: 2px;
}
```

#### Status Indicators

Styled spans for match/gap/warning states. Never use emoji.

These run at 11px on a tint of their own hue — the exact place contrast quietly fails. The semantic defaults below are one step deeper than the reflex picks (`#059669` → `#15803d`, `#ef4444` → `#dc2626`, `#d97706` → `#b45309`), which reads as the same color while clearing 4.5:1 on a light surface. In dark themes the ink flips bright and the same rule applies in reverse.

```css
.status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;  /* 500 at 11px in a hue is thin — 600 buys back apparent contrast */
  padding: 3px 10px;
  border-radius: 6px;
  white-space: nowrap;
}

/* Fallbacks are the deep tones. Never fall back to #059669/#ef4444/#d97706 —
   all three sit near 3:1 as 11px text on white. */
.status--match {
  background: var(--green-dim, rgba(21, 128, 61, 0.1));
  color: var(--green, #15803d);
}

.status--gap {
  background: var(--red-dim, rgba(220, 38, 38, 0.1));
  color: var(--red, #dc2626);
}

.status--warn {
  background: var(--orange-dim, rgba(180, 83, 9, 0.1));
  color: var(--orange, #b45309);
}

.status--info {
  background: var(--accent-dim);
  color: var(--accent);
}

/* Dot variant (compact, no text).
   A dot alone is color-as-sole-indicator — always pair it with a text label
   or a title attribute so it survives color blindness and grayscale printing. */
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot--match { background: var(--green, #15803d); }
.status-dot--gap { background: var(--red, #dc2626); }
.status-dot--warn { background: var(--orange, #b45309); }
```

**Solid-fill status badges.** If the design wants filled pills rather than tints, the ink is the palette's near-black or near-white — not `#fff` by default:

```css
.status--solid-match {
  background: var(--green, #15803d);
  color: var(--surface);       /* deep fill → light ink: 5.0:1 */
}

.status--solid-warn {
  background: var(--orange-bright, #fbbf24);
  color: var(--text-bright);   /* bright fill → dark ink: 11:1 (white here would be 1.9:1) */
}
```

Usage in table cells:
```html
<td><span class="status status--match">Match</span></td>
<td><span class="status status--gap">Gap</span></td>
<td><span class="status status--warn">Partial</span></td>
```

#### Table Summary Row

For totals, counts, or aggregate status at the bottom:

```css
.data-table tfoot td {
  background: var(--surface-elevated, var(--surface2, var(--surface)));
  font-weight: 600;
  font-size: 12px;
  border-top: 2px solid var(--border-bright);
  border-bottom: none;
  padding: 12px 16px;
}
```

#### Sticky First Column (for very wide tables)

```css
.data-table th:first-child,
.data-table td:first-child {
  position: sticky;
  left: 0;
  z-index: 1;
  background: var(--surface);
}

.data-table tbody tr:nth-child(even) td:first-child {
  background: color-mix(in srgb, var(--surface) 95%, var(--accent) 5%);
}
```

## Connectors

### CSS Arrow (vertical, between stacked sections)
```css
.flow-arrow {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  color: var(--text-dim);
  font-family: var(--font-mono);
  font-size: 12px;
  padding: 6px 0;
}

/* Down arrow via SVG icon */
.flow-arrow svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: var(--border-bright);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
```

Down arrow SVG (reuse inline):
```html
<svg viewBox="0 0 20 20"><path d="M10 4 L10 16 M6 12 L10 16 L14 12"/></svg>
```

### CSS Arrow (horizontal, between inline steps)
Use `::after` or a literal arrow character:
```css
.h-arrow::after {
  content: '→';
  color: var(--border-bright);
  font-size: 18px;
  padding: 0 4px;
}
```

### SVG Curved Connector (between arbitrary nodes)
For connections that aren't simple vertical/horizontal, use an absolutely positioned SVG overlay:
```html
<svg class="connectors" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;">
  <path d="M 150,100 C 150,200 350,100 350,200" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"/>
  <!-- Arrowhead -->
  <polygon points="348,195 352,205 356,195" fill="var(--accent)"/>
</svg>
```

Position the parent container as `position: relative` to scope the SVG overlay.

## Animations

### Staggered Fade-In on Load

Define the keyframe once, then stagger via a `--i` CSS variable set per element. This approach works regardless of DOM nesting or interleaved non-animated elements (unlike `nth-child` which breaks when siblings aren't all the same type).

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.ve-card {
  animation: fadeUp 0.4s ease-out both;
  animation-delay: calc(var(--i, 0) * 0.05s);
}
```

Set `--i` per element in the HTML to control stagger order:

```html
<div class="ve-card" style="--i: 0">First</div>
<div class="connector">...</div>
<div class="ve-card" style="--i: 1">Second</div>
<div class="connector">...</div>
<div class="ve-card" style="--i: 2">Third</div>
```

### Hover Lift
```css
.ve-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ve-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

### Scale-Fade (for KPI cards, badges, status indicators)

```css
@keyframes fadeScale {
  from { opacity: 0; transform: scale(0.92); }
  to { opacity: 1; transform: scale(1); }
}

.kpi-card {
  animation: fadeScale 0.35s ease-out both;
  animation-delay: calc(var(--i, 0) * 0.06s);
}
```

### SVG Draw-In (for connectors, progress rings, path elements)

```css
@keyframes drawIn {
  from { stroke-dashoffset: var(--path-length); }
  to { stroke-dashoffset: 0; }
}

/* Set --path-length to the path's getTotalLength() value */
.connector path {
  stroke-dasharray: var(--path-length);
  animation: drawIn 0.8s ease-in-out both;
  animation-delay: calc(var(--i, 0) * 0.1s);
}
```

### CSS Counter (for hero numbers without JS)

Uses `@property` to animate a custom property as an integer, then display it via `counter()`. No JS required. Falls back to showing the final value immediately in browsers without `@property` support.

```css
@property --count {
  syntax: '<integer>';
  initial-value: 0;
  inherits: false;
}

@keyframes countUp {
  to { --count: var(--target); }
}

.kpi-card__value--animated {
  --target: 247;
  counter-reset: val var(--count);
  animation: countUp 1.2s ease-out forwards;
}

.kpi-card__value--animated::after {
  content: counter(val);
}
```

### Choreography

Don't use the same animation for everything. Mix types by element role, with easing stagger (fast-then-slow, not linear):

- **Cards**: `fadeUp` — the default entrance, reliable and subtle
- **KPI / badges**: `fadeScale` — scale draws the eye to important numbers
- **SVG connectors**: `drawIn` — reveals flow direction, pairs with card stagger
- **Hero numbers**: `countUp` — counting motion signals "this number matters"
- **Stagger timing**: `calc(var(--i) * 0.06s)` with lower `--i` values on important elements so they appear first

### Respect Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Sparklines and Simple Charts (Pure SVG)

For simple inline visualizations without a library:

```html
<!-- Sparkline -->
<svg viewBox="0 0 100 30" style="width:100px;height:30px;">
  <polyline points="0,25 15,20 30,22 45,10 60,15 75,5 90,12 100,8"
    fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round"/>
</svg>

<!-- Progress bar -->
<div style="height:6px;background:var(--border);border-radius:3px;overflow:hidden;">
  <div style="height:100%;width:72%;background:var(--accent);border-radius:3px;"></div>
</div>
```

## Responsive Breakpoint

Include a single breakpoint for narrow viewports:

```css
@media (max-width: 768px) {
  .arch-grid { grid-template-columns: 1fr; }
  .pipeline { flex-wrap: wrap; gap: 8px; }
  .pipeline__arrow { display: none; }
  body { padding: 16px; }
}
```

## Badges and Tags

Small inline labels for categorizing elements:

```css
.tag {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 500;
  padding: 2px 7px;
  border-radius: 4px;
  background: var(--node-a-dim);
  color: var(--node-a);
}
```

## Lists Inside Nodes

For tool listings, feature lists, table columns:

```css
.node-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 12px;
  line-height: 1.8;
}

.node-list li {
  padding-left: 14px;
  position: relative;
}

.node-list li::before {
  content: '›';
  color: var(--text-dim);
  font-weight: 600;
  position: absolute;
  left: 0;
}

.node-list code {
  font-family: var(--font-mono);
  font-size: 11px;
  background: var(--accent-dim);
  color: var(--accent);
  padding: 1px 5px;
  border-radius: 3px;
}
```

## KPI / Metric Cards

Large hero number with trend indicator and label. For dashboards, review summaries, and impact sections.

```css
.kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.kpi-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.kpi-card__value {
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -1px;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.kpi-card__label {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-dim);
  margin-top: 6px;
}

.kpi-card__trend {
  font-family: var(--font-mono);
  font-size: 12px;
  margin-top: 4px;
}

/* 12px semantic text — needs the deep tones, and a glyph so the up/down
   distinction doesn't rest on color alone. */
.kpi-card__trend--up { color: var(--node-b, #15803d); }
.kpi-card__trend--down { color: var(--red, #dc2626); }
.kpi-card__trend--up::before { content: '▲ '; font-size: 9px; }
.kpi-card__trend--down::before { content: '▼ '; font-size: 9px; }
```

```html
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-card__value">247</div>
    <div class="kpi-card__label">Lines Added</div>
    <div class="kpi-card__trend kpi-card__trend--up">+34%</div>
  </div>
  <!-- ... more cards -->
</div>
```

## Before / After Panels

Two-column comparison with diff-colored headers. For review pages, migration docs, and feature comparisons.

```css
.diff-panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

.diff-panels > * { min-width: 0; overflow-wrap: break-word; }

.diff-panel__header {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 10px 16px;
}

/* 11px uppercase mono on a tint of its own hue — use the deep tones.
   Before/after also carries a word, so the panels don't rely on color alone. */
.diff-panel__header--before {
  background: var(--red-dim, rgba(220, 38, 38, 0.08));
  color: var(--red, #dc2626);
  border-bottom: 2px solid var(--red, #dc2626);
}

.diff-panel__header--after {
  background: var(--green-dim, rgba(21, 128, 61, 0.08));
  color: var(--green, #15803d);
  border-bottom: 2px solid var(--green, #15803d);
}

.diff-panel__body {
  padding: 16px;
  background: var(--surface);
  font-size: 13px;
  line-height: 1.6;
}

/* Highlight changed items within a panel */
.diff-changed {
  background: var(--accent-dim);
  border-radius: 3px;
  padding: 0 3px;
}

@media (max-width: 768px) {
  .diff-panels { grid-template-columns: 1fr; }
}
```

```html
<div class="diff-panels">
  <div class="diff-panel__header diff-panel__header--before">Before</div>
  <div class="diff-panel__header diff-panel__header--after">After</div>
  <div class="diff-panel__body">Previous implementation...</div>
  <div class="diff-panel__body">New implementation...</div>
</div>
```

## Collapsible Sections

Native `<details>/<summary>` with styled disclosure. Zero JS, accessible. For lower-priority content: file maps, decision logs, reference sections.

```css
details.collapsible {
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

details.collapsible summary {
  padding: 14px 20px;
  background: var(--surface);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text);
  transition: background 0.15s ease;
}

details.collapsible summary:hover {
  background: var(--surface-elevated, var(--surface));
}

details.collapsible summary::-webkit-details-marker { display: none; }

/* Chevron indicator */
details.collapsible summary::before {
  content: '▸';
  font-size: 11px;
  color: var(--text-dim);
  transition: transform 0.15s ease;
}

details.collapsible[open] summary::before {
  transform: rotate(90deg);
}

details.collapsible .collapsible__body {
  padding: 16px 20px;
  border-top: 1px solid var(--border);
  font-size: 13px;
  line-height: 1.6;
}
```

```html
<details class="collapsible">
  <summary>File Map (14 files changed)</summary>
  <div class="collapsible__body">
    <!-- content here -->
  </div>
</details>
```

## Interactive Controls

Patterns for tool pages (see `tool-patterns.md`) and any page with real inputs — browsers' search fields and facet pills included. Controls are where the contrast contract gets broken most: a button is a fill with text on it, a focus ring is meaningful non-text (3:1 floor), and native sliders ignore your palette entirely unless restyled per-engine. Everything below runs on the same tokens as the rest of the page.

### Buttons

One primary button per view — on a tool page that's the export button. Everything else steps down:

```css
button {
  font: inherit;              /* buttons don't inherit font by default */
  cursor: pointer;
  border-radius: 6px;
  padding: 7px 14px;
  border: 1px solid transparent;
  transition: background 0.15s ease, border-color 0.15s ease,
              filter 0.15s ease, transform 0.1s ease;
}
button:active { transform: translateY(1px); }
button:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }

.btn-primary {                /* the export button — the fill pair, never accent + #fff */
  background: var(--accent-fill);
  color: var(--accent-on-fill);
}
.btn-primary:hover { filter: brightness(1.08); }

.btn-secondary {
  background: var(--surface);
  color: var(--text);
  border-color: var(--border-bright);
}
.btn-secondary:hover { border-color: var(--accent); color: var(--accent); }

.btn-ghost {                  /* tertiary: ink only, background appears on hover */
  background: transparent;
  color: var(--accent);
}
.btn-ghost:hover { background: var(--accent-dim); }

@media (pointer: coarse) {    /* 44px touch floor on touch-primary devices */
  button { min-height: 44px; }
}
```

**Copied feedback:** on export, swap the button's label to "Copied ✓" for ~1.5s by toggling a class — keep the button's width fixed (`min-width` set to its widest label) so the page doesn't reflow under the cursor, and give the button `aria-live="polite"` so the swap is announced to screen readers.

### Focus rings

Every interactive element gets a visible `:focus-visible` ring — it's the keyboard path's only affordance, and it's non-text UI carrying meaning, so it has the 3:1 floor against the surface it sits on:

```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

The `--accent` ink already clears 4.5:1 as text, so it clears the 3:1 ring floor for free. Never `outline: none` without a replacement.

### Text inputs, selects, textareas

```css
input[type="text"], input[type="search"], select, textarea {
  font: inherit;              /* form controls don't inherit font either */
  color: var(--text);
  background: var(--surface);
  border: 1px solid var(--border-bright);
  border-radius: 6px;
  padding: 7px 10px;
}
input:disabled, select:disabled, textarea:disabled { opacity: 0.55; cursor: not-allowed; }

input::placeholder { color: var(--text-dim); }  /* skippable info — dim is correct here */

textarea { resize: vertical; min-height: 90px; line-height: 1.55; }

@media (pointer: coarse) {
  input, select, textarea { font-size: max(16px, 1em); }  /* below 16px, iOS Safari zooms on focus */
}
```

Editable code/prompt panes (tuners, template editors) take `font-family: var(--font-mono)` and the recessed treatment from Code Blocks; keep `tab-size: 2`.

### Range sliders

Native tracks and thumbs are engine-drawn and ignore the palette; restyle both engines or the slider is the one off-brand element on the page:

```css
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  height: 4px;
  background: var(--border-bright);
  border-radius: 2px;
}
input[type="range"]::-moz-range-track {   /* Firefox draws its own track unless told not to */
  background: transparent;
  height: 4px;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--accent);
  border: none;
  cursor: grab;
}
input[type="range"]::-moz-range-thumb {
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--accent);
  border: none;
  cursor: grab;
}
input[type="range"]:active::-webkit-slider-thumb { cursor: grabbing; }
input[type="range"]:active::-moz-range-thumb { cursor: grabbing; }
```

Every slider pairs with a live readout — `var(--font-mono)`, `tabular-nums`, updated on `input` — because in a parameter sandbox the number *is* the deliverable.

### Toggles

A checkbox styled as a switch; the on-state uses the fill pair:

```css
.switch { position: relative; width: 34px; height: 20px; display: inline-block; }
.switch input { opacity: 0; width: 100%; height: 100%; margin: 0; cursor: pointer; }
.switch .knob {
  position: absolute; inset: 0;
  background: var(--border-bright);
  border-radius: 10px;
  pointer-events: none;
  transition: background 0.15s ease;
}
.switch .knob::after {
  content: '';
  position: absolute; top: 2px; left: 2px;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--surface);
  transition: transform 0.15s ease;
}
.switch input:checked + .knob { background: var(--accent-fill); }
.switch input:checked + .knob::after { transform: translateX(14px); }
.switch input:disabled { cursor: not-allowed; }
.switch input:disabled + .knob { opacity: 0.55; }
```

Pair every switch with a visible text label — the switch alone fails the squint test as "which way is on?".

### Drag states

Three states, all driven by classes the JS toggles — and all with a keyboard twin (selected + arrow keys), which reuses the same visual states:

```css
.card.is-dragging, .card.is-grabbed {   /* pointer drag and keyboard pickup look the same */
  opacity: 0.85;
  transform: scale(1.02);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
  cursor: grabbing;
}

.column.is-drop-target {
  background: var(--accent-dim);
  outline: 1.5px dashed var(--accent);
  outline-offset: -1.5px;
}
```

The drop target gets a wash plus dashed outline — a state change a colorblind user still reads from the outline alone.

### Validation and warnings

Constraint violations (a flag enabled without its prerequisite, a regex that doesn't compile) sit **with the field**, appearing as the violation happens:

```css
.field.is-invalid input { border-color: var(--node-c); }

.field-warning {
  margin-top: 5px;
  font-size: 12px;
  color: var(--node-c);              /* ink tone — clears 4.5:1 like any small text */
  background: var(--node-c-dim);
  border: 1px solid color-mix(in srgb, var(--node-c) 30%, transparent);
  border-radius: 5px;
  padding: 5px 9px;
}
```

Full tinted border and wash — the message reads as attached to its field. A warning that only changes a border color fails the squint test; the text is what says *why*.

Wire it for assistive tech too: point the input at its message with `aria-describedby`, and give the message container `role="status"` so a warning that appears mid-edit is announced without stealing focus.

## Prose Page Elements

Patterns for documentation, articles, blog posts, and other reading-first content. The key difference from visual explanations: optimize for sustained reading, not scanning.

### Body Text Settings

```css
/* Comfortable reading baseline */
.prose {
  font-size: clamp(17px, 1.1vw + 14px, 19px);
  line-height: 1.7;
  max-width: 65ch;  /* ~600-680px */
  text-wrap: pretty;
}

.prose p {
  margin-bottom: 1.5em;
}

/* Narrow column for essays/literary content */
.prose--narrow {
  max-width: 60ch;
  line-height: 1.8;
}

/* Wide column for technical content with code */
.prose--wide {
  max-width: 75ch;
  line-height: 1.6;
}
```

### Lead Paragraph

Opening paragraph styled distinctly from body text.

```css
/* Larger size */
.lead {
  font-size: 20px;
  line-height: 1.6;
  color: var(--text-bright);
  margin-bottom: 32px;
}

/* With drop cap */
.lead--dropcap::first-letter {
  float: left;
  font-family: var(--font-display);
  font-size: 64px;
  font-weight: 600;
  line-height: 0.85;
  padding-right: 12px;
  padding-top: 6px;
  color: var(--accent);
}
```

### Pull Quotes

Key insights pulled out for emphasis. Use sparingly — one or two per article maximum.

```css
/* Indented with oversized quote mark */
.pullquote {
  margin: 48px 0;
  padding-left: 56px;
  position: relative;
}
.pullquote::before {
  content: '\201C';
  position: absolute;
  left: 0;
  top: -8px;
  font-family: var(--font-display);
  font-size: 64px;
  line-height: 1;
  color: var(--accent);
}
.pullquote p {
  font-size: 22px;
  font-style: italic;
  line-height: 1.4;
  color: var(--text-bright);
  margin: 0;
}

/* Centered with quotation mark */
.pullquote--centered {
  margin: 56px 0;
  padding: 32px 40px;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  text-align: center;
  position: relative;
}
.pullquote--centered::before {
  content: '"';
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--bg);
  padding: 0 16px;
  font-family: var(--font-display);
  font-size: 48px;
  color: var(--accent);
  line-height: 1;
}
```

### Section Dividers

```css
/* Horizontal rule */
hr {
  border: none;
  height: 1px;
  background: var(--border);
  margin: 48px 0;
}

/* Ornamental divider — use: <div class="divider">✦ ✦ ✦</div> */
.divider {
  text-align: center;
  margin: 48px 0;
  color: var(--text-dim);
  font-size: 18px;
  letter-spacing: 12px;
}
```

### Article Hero Patterns

```css
/* Centered minimal — essays, personal posts */
.hero--centered {
  text-align: center;
  padding: 80px 24px 64px;
  max-width: 800px;
  margin: 0 auto;
}
.hero__category {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--accent);
  margin-bottom: 16px;
}
.hero__title {
  font-size: clamp(32px, 5vw, 48px);
  font-weight: 600;
  line-height: 1.15;
  margin-bottom: 16px;
}
.hero__subtitle {
  font-size: 20px;
  font-style: italic;
  color: var(--text-dim);
  max-width: 600px;
  margin: 0 auto 24px;
}
.hero__meta {
  font-size: 13px;
  color: var(--text-dim);
}

/* Left-aligned editorial — features, documentation */
.hero--editorial {
  padding: 100px 40px 60px;
  max-width: 1000px;
  margin: 0 auto;
}
.hero--editorial .hero__title {
  font-size: clamp(40px, 7vw, 72px);
  font-weight: 800;
  line-height: 1.0;
  letter-spacing: -2px;
}
```

### Author Byline

```css
.byline {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 24px;
}
.byline__avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.byline__name {
  font-weight: 600;
  color: var(--text-bright);
  display: block;
}
.byline__meta {
  font-size: 13px;
  color: var(--text-dim);
}
```

### Callout Boxes

For warnings, tips, notes, and key takeaways.

```css
/* Full tinted border + background wash */
.callout {
  padding: 16px 20px;
  border-radius: 8px;
  border: 1px solid color-mix(in srgb, var(--callout-border) 35%, transparent);
  background: var(--callout-bg);
  margin: 24px 0;
}

.callout--info {
  --callout-border: var(--accent);
  --callout-bg: color-mix(in srgb, var(--accent) 10%, transparent);
}

.callout--warning {
  --callout-border: var(--amber);
  --callout-bg: color-mix(in srgb, var(--amber) 10%, transparent);
}

.callout--success {
  --callout-border: var(--green);
  --callout-bg: color-mix(in srgb, var(--green) 10%, transparent);
}

/* Title takes the accent's INK tone, not the border tone — the border color is
   chosen to read as a 1px edge (3:1 is enough there) and is usually too light
   to carry text. They're often the same value; when they differ, ink wins. */
.callout__title {
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--callout-ink, var(--callout-border));
}

/* Callout body stays in --text. Setting it in the accent hue or in --text-dim
   is the most common way a callout ends up less readable than the prose
   around it — which inverts the whole point of a callout. */
.callout p,
.callout li {
  color: var(--text);
}

/* Lists inside callouts need padding fix */
.callout ul, .callout ol {
  padding-left: 1.5em;
  margin: 8px 0 0 0;
}
```

### Theme Toggle

Use `data-theme` attribute for user-controllable light/dark modes. Random initial theme adds variety.

```css
:root, [data-theme="light"] {
  --bg: #faf9f7;
  --surface: #fffefc;
  --text: #1c1917;
  --text-dim: #6b635c;      /* 5.9:1 on --surface */
  --border: #e7e5e4;
  --pattern: rgba(28, 25, 23, 0.045);
  --accent: #0f766e;        /* 5.4:1 — #0d9488 is only 3.7:1 */
  --accent-fill: #0f766e;
  --accent-on-fill: #f0fdfa;
}

[data-theme="dark"] {
  --bg: #0c0a09;
  --surface: #1c1917;
  --text: #fafaf9;
  --text-dim: #a8a29e;
  --border: #292524;
  --pattern: rgba(250, 249, 249, 0.04);
  --accent: #14b8a6;        /* bright ink for dark surfaces */
  --accent-fill: #115e56;   /* fill stays deep so light ink can sit on it */
  --accent-on-fill: #f0fdfa;
}
```

Both themes must be checked, not just the one you designed in. A `[data-theme]` toggle makes this cheap — flip it and re-run the contrast check.

```javascript
// Random initial theme
const themes = ['light', 'dark'];
document.documentElement.setAttribute('data-theme', themes[Math.floor(Math.random() * 2)]);

// Toggle function
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  document.documentElement.setAttribute('data-theme', current === 'light' ? 'dark' : 'light');
}
```

```html
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
  <svg class="theme-toggle__sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
  </svg>
  <svg class="theme-toggle__moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
  </svg>
</button>
```

```css
.theme-toggle {
  position: fixed;
  top: 20px;
  right: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  z-index: 100;
}
[data-theme="light"] .theme-toggle__moon { display: none; }
[data-theme="dark"] .theme-toggle__sun { display: none; }
```

### Prose Anti-Patterns

Avoid these in reading-first content:
- Body text smaller than 16px
- Line-height below 1.5
- Measure wider than 75ch (text spanning full viewport)
- Pull quotes every other paragraph
- Drop caps on every section
- Busy background patterns behind text — prose needs an opaque surface under it, always
- Body copy set in `--text-dim`, or in an accent hue, "for warmth" — warmth comes from tinted neutrals and accented headings, not from fading the words
- Pull quotes and lead paragraphs in a lighter tone than the body they're meant to emphasize (they use `--text-bright`, which is *darker* than `--text` on light themes)

## Generated Images

For AI-generated illustrations embedded as base64 data URIs via `surf gemini --generate-image`. Use sparingly — hero banners, conceptual illustrations, educational diagrams, decorative accents.

### Hero Banner

Full-width image cropped to a fixed height with a gradient fade into the page background. Place at the top of the page before the title, or between the title and the first content section.

```css
.hero-img-wrap {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 24px;
}

.hero-img-wrap img {
  width: 100%;
  height: 240px;
  object-fit: cover;
  display: block;
}

/* Gradient fade into page background */
.hero-img-wrap::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(to top, var(--bg), transparent);
  pointer-events: none;
}
```

```html
<div class="hero-img-wrap">
  <img src="data:image/png;base64,..." alt="Descriptive alt text">
</div>
```

Generate with `--aspect-ratio 16:9` for hero banners.

### Inline Illustration

Centered image with border, shadow, and optional caption. Use within content sections for conceptual or educational illustrations.

```css
.illus {
  text-align: center;
  margin: 24px 0;
}

.illus img {
  max-width: 480px;
  width: 100%;
  border-radius: 10px;
  border: 1px solid var(--border);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.illus figcaption {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-dim);
  margin-top: 8px;
}
```

```html
<figure class="illus">
  <img src="data:image/png;base64,..." alt="Descriptive alt text">
  <figcaption>How the message queue routes events between services</figcaption>
</figure>
```

Generate with `--aspect-ratio 1:1` or `--aspect-ratio 4:3` for inline illustrations.

### Side Accent

Small image floated beside a section. Use when the illustration supports but doesn't dominate the content.

```css
.accent-img {
  float: right;
  max-width: 200px;
  margin: 0 0 16px 24px;
  border-radius: 10px;
  border: 1px solid var(--border);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

@media (max-width: 768px) {
  .accent-img {
    float: none;
    max-width: 100%;
    margin: 0 0 16px 0;
  }
}
```

```html
<img class="accent-img" src="data:image/png;base64,..." alt="Descriptive alt text">
```
