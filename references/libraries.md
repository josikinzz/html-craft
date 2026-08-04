# External Libraries (CDN)

Optional CDN libraries for cases where pure CSS/HTML isn't enough. Only include what the diagram actually needs — most diagrams need zero external JS.

## Mermaid.js — Diagramming Engine

All Mermaid guidance (CDN import, ELK layout, deep theming, CSS overrides, syntax rules, container/zoom/export patterns) lives in [`mermaid.md`](mermaid.md). Read that file before writing any Mermaid.

## Chart.js — Data Visualizations

Use for bar charts, line charts, pie/doughnut charts, radar charts, and other data-driven visualizations in dashboard-type diagrams. Overkill for static numbers — use pure SVG/CSS for simple progress bars and sparklines.

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>

<canvas id="myChart" width="600" height="300"></canvas>

<script>
  const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const textColor = isDark ? '#8b949e' : '#6b7280';
  const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
  const fontFamily = getComputedStyle(document.documentElement)
    .getPropertyValue('--font-body').trim() || 'system-ui, sans-serif';

  new Chart(document.getElementById('myChart'), {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      datasets: [{
        label: 'Feedback Items',
        data: [45, 62, 78, 91, 120],
        // Pull chart colors from the page palette — never Tailwind indigo/violet defaults
        backgroundColor: isDark ? 'rgba(8, 145, 178, 0.55)' : 'rgba(3, 105, 161, 0.55)',
        borderColor: isDark ? '#22b8d4' : '#0369a1',
        borderWidth: 1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
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

Wrap the canvas in a styled container:
```css
.chart-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  position: relative;
}

.chart-container canvas {
  max-height: 300px;
}
```

## anime.js — Orchestrated Animations

Use when a diagram has 10+ elements and you want a choreographed entrance sequence (staggered reveals, path drawing, count-up numbers). For simpler diagrams, CSS `animation-delay` staggering is sufficient.

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js"></script>

<script>
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!prefersReduced) {
    anime({
      targets: '.ve-card',
      opacity: [0, 1],
      translateY: [20, 0],
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

When using anime.js, set initial opacity to 0 in CSS so elements don't flash before the animation:
```css
.ve-card { opacity: 0; }

@media (prefers-reduced-motion: reduce) {
  .ve-card { opacity: 1 !important; }
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
