# Structures and Item Motifs

How to choose the **structural shape** of a page's content, and how to build the shapes this skill does not already cover.

A composition decomposes into three orthogonal choices:

- **Structure** — the layout skeleton: how N units are arranged (funnel, quadrant, pyramid, snake path…).
- **Item** — the repeating motif that renders one unit (indexed card, pill badge, circle node…).
- **Theme** — palette and typography. Covered in `SKILL.md` and [`css-patterns.md`](css-patterns.md); this file leaves it alone.

Structure and Item combine freely. A funnel of pill badges and a funnel of progress cards are different pages. Rotating the Item is the cheapest way to stop two pages reading as siblings — palette alone will not do it.

## Content → Structure

Pick from the content's semantics, not from what looks good.

| Content shape | Structure | Notes |
|---|---|---|
| Narrowing, attrition, drop-off at each stage | **Funnel** | Stage width must encode the real number. |
| Positioning on two independent axes, tradeoffs | **Quadrant** | Needs both poles of both axes named. |
| Part-whole priority stack, layered dependency (each tier rests on the one below) | **Pyramid** | Base = broadest/most foundational. Inverted only for narrowing. |
| One concept with satellites, hub-and-spoke, facets of a whole | **Radial / sector** | 4–8 satellites. Past 8, use a grid. |
| Ordered sequence, ≤5 steps | **Steps** (horizontal pipeline) | `css-patterns.md` → Pipeline. |
| Ordered sequence, 4–8 steps, each needing a paragraph | **Zigzag steps** | Alternating sides give each step room without a monotonous stack. |
| Ordered sequence, 8+ short steps | **Snake path** or **roadmap** | Wraps across rows so a long sequence stays scannable instead of becoming an endless vertical list. |
| Ordered sequence carrying real dates | **Timeline** | `SKILL.md` → Timeline / Roadmap Views. |
| Unordered peers, uniform size | **Grid** | `css-patterns.md` → Card Grid. |
| Unordered peers, one line each | **List rows** | |
| Unordered peers, varying text length | **Waterfall stagger** | Offsetting alternate items breaks the ruled-grid monotony of equal cards. |
| A vs B | **Binary compare** with a center divider spine | Two panels plus a labelled spine; `css-patterns.md` → Before/After for the diff-colored variant. |
| Hierarchy, containment | **Tree** | `css-patterns.md` → Directory Tree for file-shaped trees. |
| Relationships, network, arbitrary edges | **Mermaid** | [`mermaid.md`](mermaid.md). Hand-written CSS loses to a layout engine the moment edges cross. |

Two structures on one page is a strong page. Four is a scrapbook.

## Structure recipes

All recipes assume the tokens in [`css-patterns.md`](css-patterns.md) (`--surface`, `--border`, `--accent`, the ink/fill pairs, `.ve-card` depth tiers). Every grid and flex child below carries `min-width: 0`; content wraps rather than clipping horizontally.

### Funnel

Stage width encodes the value. Labels live in a side column so text never sits on a sloped edge.

```css
.funnel { display: grid; gap: 4px; max-width: 640px; margin: 0 auto; }
.funnel__row { display: grid; grid-template-columns: 1fr 180px; gap: 16px; align-items: center; }
.funnel__row > * { min-width: 0; }

/* --w = this stage's width %, --wn = the next stage's. Both from real data. */
.funnel__seg {
  height: 68px;
  background: var(--accent-fill);
  clip-path: polygon(
    calc(50% - var(--w) / 2) 0,   calc(50% + var(--w) / 2) 0,
    calc(50% + var(--wn) / 2) 100%, calc(50% - var(--wn) / 2) 100%
  );
  display: grid; place-items: center;
  color: var(--accent-on-fill);
  font-variant-numeric: tabular-nums;
}
.funnel__meta { font-size: 13px; color: var(--text); }
.funnel__meta b { display: block; font-family: var(--font-mono); }
```

The fill stays flat because stage width already encodes the value. A tint ramp on top of it repeats that encoding and drags the ink below the contrast floor.

Variant — a pale ramp, for pages that want the progression visible as color. A pale fill takes `var(--text)`, never `var(--accent-on-fill)`:

```css
/* --i counts from 0 at the widest stage */
.funnel__seg--pale {
  background: color-mix(in srgb, var(--accent) calc(18% - var(--i) * 4%), var(--surface));
  color: var(--text);
}
```

```html
<div class="funnel">
  <div class="funnel__row">
    <div class="funnel__seg" style="--w:100%; --wn:62%">12,400</div>
    <div class="funnel__meta"><b>Visited</b>100% of cohort</div>
  </div>
  <div class="funnel__row">
    <div class="funnel__seg" style="--w:62%; --wn:24%">7,690</div>
    <div class="funnel__meta"><b>Signed up</b>62% · −38%</div>
  </div>
</div>
```

Caveats: percentages inside `clip-path: polygon()` resolve against the element's own box, so the stage must be full-width and the taper drawn inside it. Below ~560px, drop the side column (`grid-template-columns: 1fr`) and move the label above its stage.

### Quadrant

Grid for the four cells, absolute positioning for plotted items.

```css
.quad {
  display: grid;
  grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr;
  aspect-ratio: 1; position: relative;
  border: 1px solid var(--border-bright); border-radius: 12px; overflow: hidden;
}
/* Surface and border come from .ve-card; only geometry lives here. */
.quad__cell { padding: 14px; min-width: 0; }
.quad__cell h4 { font-size: 12px; text-transform: uppercase; letter-spacing: 1.2px; color: var(--text); margin: 0; }
.quad__cell--hi { background: color-mix(in srgb, var(--accent) 6%, var(--surface)); }

/* Plotted item: --x and --y are 0–100 in data space, y measured upward. */
.quad__item {
  position: absolute;
  left: calc(var(--x) * 1%); bottom: calc(var(--y) * 1%);
  transform: translate(-50%, 50%);
  padding: 5px 11px; border-radius: 999px;
  background: var(--accent-fill); color: var(--accent-on-fill);
  font-size: 12px; white-space: nowrap;
}

/* Axis poles — four labels, one per direction. */
.quad-wrap { display: grid; grid-template-columns: auto 1fr; grid-template-rows: auto 1fr auto; gap: 8px; align-items: center; }
.quad-wrap > * { min-width: 0; }
.quad-wrap__y { writing-mode: vertical-rl; transform: rotate(180deg); text-align: center; font-size: 11px; color: var(--text); }
.quad-wrap__x { grid-column: 2; text-align: center; font-size: 11px; color: var(--text); }
```

```html
<div class="quad">
  <div class="ve-card quad__cell"><h4>Quick wins</h4></div>
  <div class="ve-card quad__cell quad__cell--hi"><h4>Big bets</h4></div>
</div>
```

The cell names and the axis poles are the data, so they take `var(--text)`. Uppercase and letterspacing carry the secondary read instead.

Caveats: `aspect-ratio: 1` keeps the two axes commensurate — a stretched quadrant misreads distances. Items near an edge overflow their translate; give the container `padding` or clamp `--x`/`--y` to 6–94. On narrow viewports keep the square and shrink the item font rather than reflowing, since position *is* the content.

### Pyramid

Tiers widen toward the base. Text sits in a full-width inner box, never on the sloped edge.

```css
.pyr { display: grid; gap: 6px; max-width: 620px; margin: 0 auto; }
.pyr__tier {
  /* --i counts from 0 at the apex */
  width: calc(38% + var(--i) * 16%);
  margin: 0 auto;
  padding: 14px 20px;
  border-radius: 8px;
  text-align: center;
  background: var(--accent-fill);
  color: var(--accent-on-fill);
}
.pyr__tier b { display: block; font-size: 14px; }
.pyr__tier span { font-size: 12px; }

@media (max-width: 640px) { .pyr__tier { width: 100%; } }  /* stack of equal bars keeps labels readable */
```

Tier width already encodes the tier, so the fill stays flat. For a page that wants the depth visible as color, use the pale ramp and flip the ink to `var(--text)` — a pale fill never takes `var(--accent-on-fill)`:

```css
.pyr__tier--pale {
  background: color-mix(in srgb, var(--accent) calc(18% - var(--i) * 4%), var(--surface));
  color: var(--text);
}
```

For a true triangular silhouette rather than stepped bars, clip each tier with the funnel's `polygon()` using `--w`/`--wn` and inverted ordering. Prefer the stepped version: it holds text at any width.

### Radial / sector

Satellites orbit a hub. Angles come from `--n` (count) and `--k` (index).

```css
.radial { position: relative; width: min(520px, 100%); aspect-ratio: 1; margin: 0 auto; }
.radial__hub {
  position: absolute; inset: 32%;
  display: grid; place-items: center; text-align: center;
  border-radius: 50%; background: var(--accent-fill); color: var(--accent-on-fill);
  font-weight: 600;
}
.radial__spoke {
  position: absolute; top: 50%; left: 50%;
  --angle: calc(var(--k) / var(--n) * 360deg);
  transform:
    rotate(var(--angle)) translate(38%) rotate(calc(-1 * var(--angle)))
    translate(-50%, -50%);
  /* Surface, border, and shadow come from .ve-card .ve-card--elevated. */
  width: 128px; max-width: 40%; padding: 10px 12px;
  font-size: 12px; text-align: center;
  overflow-wrap: break-word; hyphens: auto;
}
/* Spoke lines: one absolutely positioned SVG overlay, per css-patterns.md → Connectors. */

@media (max-width: 620px) {
  .radial { aspect-ratio: auto; }
  .radial__hub { position: static; inset: auto; border-radius: 12px; padding: 16px; }
  .radial__spoke { position: static; transform: none; width: auto; margin-top: 8px; text-align: left; }
}
```

```html
<div class="radial" style="--n:6">
  <div class="radial__hub">Core</div>
  <div class="ve-card ve-card--elevated radial__spoke" style="--k:0">Ingest</div>
  <div class="ve-card ve-card--elevated radial__spoke" style="--k:1">Validate</div>
</div>
```

Caveats: the translate percentage resolves against the spoke's own width. Give every spoke a fixed `width`, then tune `translate()` until the ring clears the hub. Write the spokes in the DOM in reading order (clockwise from 12 o'clock) — visual position carries no meaning for a screen reader. The narrow-viewport block above turns the ring into a list; ship it.

### Waterfall / staggered list

Peer items, offset so the eye moves rather than scanning a ruled grid.

```css
.waterfall { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; align-items: start; }
.waterfall > * { min-width: 0; }
.waterfall > :nth-child(2n)   { transform: translateY(28px); }
.waterfall > :nth-child(3n+1) { transform: translateY(12px); }

@media (max-width: 700px) { .waterfall > * { transform: none; } }
```

Caveats: `transform` does not affect layout, so the last row's offset items hang past the container — add `padding-bottom: 32px` on the wrapper. Kill the offsets in one column, where they read as misalignment.

### Zigzag steps

Alternating sides, one step per row, index in the gutter.

```css
.zig { display: grid; gap: 28px; position: relative; }
.zig::before {                     /* spine */
  content: ''; position: absolute; left: 50%; top: 0; bottom: 0;
  width: 1px; background: var(--border-bright);
}
.zig__step {
  display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: center;
  position: relative;
}
.zig__step > * { min-width: 0; overflow-wrap: break-word; }
.zig__step > .zig__body { grid-column: 1; text-align: right; }
.zig__step > .zig__aside { grid-column: 2; }
.zig__step:nth-child(even) > .zig__body  { grid-column: 2; text-align: left; }
.zig__step:nth-child(even) > .zig__aside { grid-column: 1; }
.zig__step::after {                /* index bead on the spine */
  content: counter(zig); counter-increment: zig;
  position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%);
  width: 30px; height: 30px; border-radius: 50%;
  display: grid; place-items: center;
  background: var(--accent-fill); color: var(--accent-on-fill);
  font-family: var(--font-mono); font-size: 12px;
}
.zig { counter-reset: zig; }

@media (max-width: 760px) {
  .zig::before { left: 15px; }
  .zig__step { grid-template-columns: 1fr; }
  .zig__step > *, .zig__step:nth-child(even) > * { grid-column: 1; text-align: left; padding-left: 44px; }
  .zig__step::after { left: 15px; top: 0; transform: translate(-50%, 0); }
}
```

Caveat: a CSS counter draws the number but leaves it out of the DOM, where assistive technology cannot reach it. Build the sequence as an `<ol>`, or carry the number as `data-step` and print it with `content: attr(data-step)`.

Caveat: right-aligned text is hard to read past two lines. Keep the left column short, or use `text-align: left` on both sides and let the spine alone carry the alternation.

### Binary compare with center spine

```css
.versus {
  display: grid; grid-template-columns: 1fr auto 1fr; gap: 0;
  align-items: stretch;
}
.versus > * { min-width: 0; overflow-wrap: break-word; }
.versus__side { padding: 20px 24px; }   /* surface and border come from .ve-card */
.versus__side--a { border-radius: 12px 0 0 12px; }
.versus__side--b { border-radius: 0 12px 12px 0; background: color-mix(in srgb, var(--accent) 5%, var(--surface)); }
.versus__spine {
  width: 1px; background: var(--border-bright);
  position: relative;
}
.versus__spine::before {
  content: 'VS';
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  padding: 6px 9px; border-radius: 999px;
  background: var(--bg); border: 1px solid var(--border-bright);
  font-family: var(--font-mono); font-size: 10px; letter-spacing: 1px; color: var(--text-dim);
}
/* Row-aligned attributes: one .versus grid per attribute keeps the two sides comparable. */

@media (max-width: 720px) {
  .versus { grid-template-columns: 1fr; }
  .versus__spine { width: auto; height: 1px; }
  .versus__side--a { border-radius: 12px 12px 0 0; }
  .versus__side--b { border-radius: 0 0 12px 12px; }
}
```

```html
<div class="versus">
  <div class="ve-card versus__side versus__side--a">Build in house</div>
  <div class="versus__spine"></div>
  <div class="ve-card versus__side versus__side--b">Buy the vendor</div>
</div>
```

Caveat: side-by-side panels only compare if their rows line up. For more than three attributes, use one `.versus` grid per attribute (or a two-column table) rather than two free-running columns of prose.

### Snake path / roadmap

Long sequences wrap across rows; alternate rows reverse so the reading path is continuous.

```css
.snake { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; list-style: none; margin: 0; padding: 0; }
.snake > * { min-width: 0; overflow-wrap: break-word; }
/* Reverse every second row of 4 — items 5–8, 13–16, … */
.snake > :nth-child(8n+5) { grid-column: 4; }
.snake > :nth-child(8n+6) { grid-column: 3; }
.snake > :nth-child(8n+7) { grid-column: 2; }
.snake > :nth-child(8n+8) { grid-column: 1; }

.snake__stop {                          /* surface and border come from .ve-card */
  padding: 14px 16px;
  font-size: 13px;
}
.snake__stop::before {
  content: counter(stop); counter-increment: stop;   /* or attr(data-step) — see the caveat */
  display: block; font-family: var(--font-mono); font-size: 11px; color: var(--accent); margin-bottom: 4px;
}
.snake { counter-reset: stop; }

@media (max-width: 900px) { .snake { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) {
  .snake { grid-template-columns: 1fr; }
  .snake > * { grid-column: 1 !important; }   /* clear the reversal */
}
```

```html
<ol class="snake">
  <li class="ve-card snake__stop">Intake</li>
  <li class="ve-card snake__stop">Triage</li>
</ol>
```

Caveats: the `grid-column` reversal is tied to the column count. Each breakpoint that changes the count must reset it, and the `!important` above does that. A CSS counter draws the stop number but leaves it out of the DOM, where assistive technology cannot reach it — build the sequence as an `<ol>`, or carry the number as `data-step` and print it with `content: attr(data-step)`. DOM order stays the true sequence order, so keyboard and screen-reader traversal is correct even where the visual row runs right-to-left. Draw the connecting arrows with an absolutely positioned SVG overlay (`css-patterns.md` → Connectors) or omit them; the numbered stops already carry the order.

## Item motifs

The repeating unit. Pick independently of Structure, and pick a different one than the last page.

| Motif | What it is |
|---|---|
| **Indexed card** | `.ve-card` with a large mono numeral in the corner. Ordered structures. |
| **Pill badge** | Rounded capsule, one line. Dense peer sets, quadrant plots, tag rows. |
| **Progress card** | Card with a value bar underneath (`css-patterns.md` → Sparklines). Anything with a magnitude. |
| **Circle node** | Fixed-size disc with a glyph or number. Radial spokes, snake stops, step beads. |
| **Checkmark item** | Row with a leading ✓ / ✗ mark in a semantic tone. Checklists, coverage, done-state. |
| **Arrow connector** | The unit *between* items — chevron, line, or SVG path. Sequences. |
| **Capsule** | Tall rounded bar holding stacked label + value. Funnel stages, sector legends. |
| **Ribbon / letter card** | Card with a folded-corner or banner header carrying a single letter or tier grade. Pyramid tiers, ranked sets. |

Sketches for the less obvious ones:

```css
/* Indexed card — numeral as a watermark, decorative so it stays under 0.08 alpha */
.item-indexed { position: relative; overflow: hidden; }
.item-indexed::before {
  content: attr(data-index);
  position: absolute; right: -6px; top: -18px;
  font-size: 76px; font-weight: 800; line-height: 1;
  color: var(--accent); opacity: 0.07; pointer-events: none;
}

/* Circle node */
.item-circle {
  width: 52px; height: 52px; border-radius: 50%;
  display: grid; place-items: center;
  background: var(--accent-fill); color: var(--accent-on-fill);
  font-family: var(--font-mono); font-size: 14px; flex-shrink: 0;
}

/* Checkmark item — glyph plus color, never color alone */
.item-check { padding-left: 26px; position: relative; }
.item-check::before { content: '✓'; position: absolute; left: 0; color: var(--green, #15803d); font-weight: 700; }
.item-check--no::before { content: '✗'; color: var(--red, #dc2626); }

/* Ribbon / letter card */
.item-ribbon { position: relative; padding-top: 34px; }
.item-ribbon::before {
  content: attr(data-grade);
  position: absolute; top: 0; left: 16px;
  padding: 4px 12px 5px; border-radius: 0 0 6px 6px;
  background: var(--accent-fill); color: var(--accent-on-fill);
  font-family: var(--font-mono); font-size: 12px; font-weight: 700;
}
```

## Integrity and accessibility

These shapes imply quantities and relationships, so they carry a higher burden than a card grid.

- **Encoded size states its value.** A funnel stage's width, a pyramid tier's width, a sector's angle, a bar's length: each comes from the real number. Print that number as text beside it. Sizes chosen for looks are decoration impersonating a chart.
- **Name both poles of both quadrant axes** ("Low effort → High effort", "Low impact → High impact"), and label the four cells. An unlabelled quadrant is four boxes.
- **DOM order is reading order.** Radial, snake, and zigzag place items by transform and grid-column; keep the source order the true sequence so keyboard and screen-reader traversal match the meaning.
- **Reflow geometry to a list under ~620px.** Radial rings, snakes, and zigzags become a single readable column. The quadrant is the exception — its positions are the data, so it stays square and shrinks.
- **Text sits on an opaque wash.** No labels over hatching, gradients, or sloped clip edges; the sloped-edge case is why every recipe above keeps the label in its own box.
- **Redundant encoding.** Anything told by color alone also carries a glyph, a word, or a number (`css-patterns.md` → Status Indicators).
- **Contrast floors hold everywhere**: 4.5:1 for text under 19px, 3:1 for meaningful non-text such as spines, beads, and stage edges. Decorative watermark numerals stay at or below 0.08 alpha.
