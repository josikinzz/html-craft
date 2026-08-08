# External Libraries (CDN)

Optional CDN libraries for cases where pure CSS/HTML isn't enough. Only include what the diagram actually needs — most diagrams need zero external JS.

## Mermaid.js — Diagramming Engine

All Mermaid guidance (CDN import, ELK layout, deep theming, CSS overrides, syntax rules, container/zoom/export patterns) lives in [`mermaid.md`](mermaid.md). Read that file before writing any Mermaid.

## Chart.js — Data Visualizations

Use for bar charts, line charts, pie/doughnut charts, radar charts, and other data-driven visualizations in dashboard-type diagrams. Overkill for static numbers — use pure SVG/CSS for simple progress bars and sparklines.

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>

<div class="chart-container"><canvas id="myChart"></canvas></div>

<script>
  // Read the page's own tokens at runtime — the chart then follows the palette
  // in both color schemes for free, with no hardcoded hexes to drift.
  const token = (name, fallback) => getComputedStyle(document.documentElement)
    .getPropertyValue(name).trim() || fallback;

  const accent = token('--accent', '#0f766e');
  const accentFill = `color-mix(in srgb, ${accent} 55%, transparent)`;
  const textColor = token('--text-dim', '#6b7280');
  const gridColor = token('--border', 'rgba(0,0,0,0.06)');
  const fontFamily = token('--font-body', 'system-ui, sans-serif');

  new Chart(document.getElementById('myChart'), {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      datasets: [{
        label: 'Feedback Items',
        data: [45, 62, 78, 91, 120],
        // Palette tokens, never Tailwind indigo/violet defaults
        backgroundColor: accentFill,
        borderColor: accent,
        borderWidth: 1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,  // fill the container's height, set in CSS below
      plugins: {
        legend: { labels: { color: textColor, font: { family: fontFamily } } },
      },
      scales: {
        x: { ticks: { color: textColor, font: { family: fontFamily } }, grid: { color: gridColor } },
        y: { ticks: { color: textColor, font: { family: fontFamily } }, grid: { color: gridColor } },
      }
    }
  });
</script>
```

The canvas sits in a styled container, and **the container is what sets the size**. With `responsive: true` Chart.js measures its parent and writes the canvas's own width/height itself — sizing the `<canvas>` in CSS (or with `width`/`height` attributes) fights that and produces stretched or thrashing re-renders on resize:

```css
.chart-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  position: relative;
  height: 300px;   /* size here, never on the canvas */
}
```

## anime.js — Orchestrated Animations

Use when a diagram has 10+ elements and you want a choreographed entrance sequence (staggered reveals, path drawing, count-up numbers). For simpler diagrams, CSS `animation-delay` staggering is sufficient.

**anime.js *replaces* the CSS entrance — it never layers on top of it.** The kit's default `fadeUp` already animates opacity and transform on `.hc-card` (see `css-patterns.md`, "Staggered Fade-In on Load"). Running both means two entrances fighting over the same two properties. So give the choreographed elements their own `.anime-in` class, and cancel `fadeUp` wherever the two meet.

Put the CDN tag and the gate together in `<head>` — the gate must run before the elements paint, or they flash at full opacity and then jump to hidden:

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js"></script>
<script>
  // Only hide the targets once anime has actually loaded and motion is welcome.
  // If the CDN is blocked, this class is never added and the page renders
  // fully visible with no animation — the degradation tier doing its job.
  if (window.anime && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.documentElement.classList.add('anime-ready');
  }
</script>
```

Then the choreography itself, at the end of `<body>`:

```html
<script>
  if (document.documentElement.classList.contains('anime-ready')) {
    anime({
      targets: '.anime-in',
      opacity: [0, 1],
      translateY: [12, 0],   // same offset as the kit's fadeUp — entrances match
      delay: anime.stagger(80, { start: 200 }),
      easing: 'easeOutCubic',
      duration: 500,
    });

    anime({
      targets: '.connector path',
      strokeDashoffset: [anime.setDashoffset, 0],
      easing: 'easeInOutCubic',
      duration: 800,
      delay: anime.stagger(150, { start: 600 }),
    });

    document.querySelectorAll('[data-count]').forEach(el => {
      anime({
        targets: { val: 0 },
        val: parseInt(el.dataset.count),
        round: 1,
        duration: 1200,
        delay: 400,
        easing: 'easeOutExpo',
        update: (anim) => { el.textContent = anim.animations[0].currentValue; }
      });
    });
  }
</script>
```

The matching CSS. Note that the hide is scoped under `html.anime-ready` — a bare `.anime-in { opacity: 0 }` would leave every element permanently invisible the moment the CDN fails:

```css
/* Hidden only when anime.js is present and about to animate them */
html.anime-ready .anime-in { opacity: 0; }

/* Cancel the kit's CSS entrance on anything anime.js is driving,
   so the two don't fight over opacity and transform */
.hc-card.anime-in { animation: none; }

@media (prefers-reduced-motion: reduce) {
  .anime-in { opacity: 1 !important; transform: none !important; }
}
```

## Icons — Iconify Web Component (Lucide)

When an icon genuinely earns its place (source/channel marks, status glyphs), use the Iconify web component with **Lucide** as the default icon set. The component is a single ~10KB script that fetches only the icons actually used on the page, on demand, from the Iconify API — never bundle or preload an icon set.

```html
<script src="https://code.iconify.design/iconify-icon/2.3.0/iconify-icon.min.js"></script>

<iconify-icon icon="lucide:git-branch" aria-hidden="true"></iconify-icon> main
```

Rules:
- Prefer `lucide:*` names throughout a page — one consistent icon family, stroke-styled, matches technical content. Reach for another set only when Lucide lacks the concept (e.g. `simple-icons:*` for brand logos).
- Size and color via CSS on the element: `iconify-icon { font-size: 14px; color: var(--text-dim); }`. Icons inherit `currentColor`, so they follow the palette for free.
- Icons decorate labels, they never replace them — mark them `aria-hidden="true"` and keep the text beside them, so the page degrades cleanly if the script or API is unreachable.
- A handful of icons per page, purposefully placed. An icon above every heading is the templated-page tell (see SKILL.md Anti-Patterns).

## Google Fonts — Typography

Always load with `display=swap` for fast rendering. Pick a distinctive pairing — body + mono at minimum, optionally a display font for the title.

The forbidden `--font-body` choices (Inter, Roboto, Arial, Helvetica, bare system-ui) are listed in SKILL.md's Anti-Patterns (AI Slop) section — check it before committing a pairing.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Martian+Mono:wght@400;500&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Define as CSS variables for easy reference:
```css
:root {
  --font-body: 'Hanken Grotesk', system-ui, sans-serif;
  --font-mono: 'Martian Mono', 'SF Mono', Consolas, monospace;
}
```

**Font pairings** (rotate — never use the same pairing twice in a row). These deliberately avoid the monoculture reflex fonts listed in SKILL.md's Anti-Patterns. Pick the row whose feel matches your voice-words, not the top row by habit:

| Body / Headings | Mono / Labels | Feel | Use for |
|---|---|---|---|
| Sora | Spline Sans Mono | Technical, precise | Blueprint, ER diagrams, schemas |
| Besley | Martian Mono | Editorial, sharp | Plan reviews, decision logs |
| Hanken Grotesk | JetBrains Mono | Reliable, readable | Architecture diagrams |
| Bricolage Grotesque | Fragment Mono | Bold, characterful | Data tables, dashboards |
| Gabarito | Victor Mono | Rounded, approachable | Status reports, audits |
| Familjen Grotesk | Fira Code | Clean geometric, modern | Flowcharts, pipelines |
| Spectral | Sometype Mono | Scholarly, serious | RFC reviews, specs |
| Vollkorn | Source Code Pro | Warm, distinctive | Project recaps |
| Geist | Geist Mono | Vercel-inspired, sharp | Modern API docs |
| Red Hat Display | Red Hat Mono | Cohesive family | System overviews |
| Libre Franklin | Inconsolata | Classic, reliable | Data-dense tables |
| Zilla Slab | Kode Mono | Sturdy, slab-serif contrast | Executive summaries |
| Schibsted Grotesk | Azeret Mono | Newsy, confident | Diff reviews, changelogs |
| Libre Caslon Text | Courier Prime | Formal, engraved | Engraved ledger, records, sign-offs |
| Baloo 2 | Chivo Mono | Chunky, friendly | Risograph zine, playful explainers |
| Gelasio | Cousine | Bookish, observational | Field guide, specimen-style pages |

Vary across consecutive diagrams. If a pairing here starts feeling like *your* default, that's the same monoculture problem one level up — browse Google Fonts with the content's voice-words in mind and substitute.

### Typography by Content Voice

For prose-heavy pages (documentation, articles, essays), match typography to the content's voice:

| Voice | Fonts | Best For |
|-------|-------|----------|
| **Literary / Thoughtful** | Literata, Spectral, Vollkorn, Petrona | Essays, personal posts, long-form articles |
| **Technical / Precise** | Sora + Spline Sans Mono, Geist + Geist Mono, Source family | Documentation, READMEs, API references |
| **Bold / Contemporary** | Bricolage Grotesque, Familjen Grotesk, Schibsted Grotesk | Product pages, feature announcements |
| **Minimal / Focused** | Source Serif 4 + Source Sans 3, Karla + Inconsolata | Tutorials, how-tos, focused reading |

**Literata** deserves special mention — it has optical sizing designed specifically for screen reading. Google's answer to Georgia, but modernized.
