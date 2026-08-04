---
name: visual-explainer
description: Generate self-contained HTML pages that visually explain systems, code changes, plans, and data — and single-file interactive tools that round-trip their result back as text. Use when the user asks for a diagram, architecture overview, comparison table, or any visual explanation of technical concepts; wants to browse a collection of documents or reports; wants several design or implementation options laid out side by side; or needs a throwaway editor for the data at hand — a triage board, config editor, parameter tuner, curation table, or annotator. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead.
license: MIT
compatibility: Requires a browser to view generated HTML files. Optional surf-cli for AI image generation.
metadata:
  author: nicobailon
  version: "0.10.0"
---

# Visual Explainer

Generate self-contained HTML files for technical diagrams, visualizations, data tables, and interactive tools. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (4+ rows or 3+ columns — comparisons, audits, feature matrices, status reports, requirement audits, API inventories), generate an HTML page instead without waiting to be asked. A brief text summary in chat is fine, but the table itself belongs in the browser.

## Available Commands

Detailed prompt templates in `./commands/`, invoked as slash commands namespaced by harness (e.g. `/visual-explainer:diff-review` in Claude Code, `/diff-review` in Pi).

| Command | What it does |
|---------|-------------|
| `generate-web-diagram` | Generate an HTML diagram for any topic |
| `generate-visual-plan` | Generate a visual implementation plan for a feature |
| `generate-slides` | Generate a magazine-quality slide deck |
| `diff-review` | Visual diff review with architecture comparison and code review |
| `plan-review` | Compare a plan against the codebase with risk assessment |
| `project-recap` | Mental model snapshot for context-switching back to a project |
| `browse-docs` | Document browser for perusing a corpus of docs/reports with nav, search, and facets |
| `make-tool` | Throwaway single-file editor (triage board, config editor, tuner, annotator) with a round-trip export |
| `explore-options` | Exploration grid — distinctly different approaches side by side, each labeled with its tradeoff |
| `index` | Build/refresh the launcher index for `~/.agent/diagrams` — grouped by repo and date, staleness-flagged |
| `fact-check` | Verify accuracy of a document against actual code |
| `share-page` | Deploy an HTML page to Vercel and get a live URL |

## Workflow

### 1. Think (5 seconds, not 5 minutes)

Before writing HTML, commit to a direction. Don't default to "dark theme with blue accents" every time.

**Visual is always default.** Even essays, blog posts, and articles get visual treatment — extract structure into cards, diagrams, grids, tables. Prose patterns (lead paragraphs, pull quotes, callout boxes) are **accent elements** within visual pages, not a separate mode — see "Prose Page Elements" in `./references/css-patterns.md`.

**Match the weight to the question.** Scale the page to what's being asked: a quick "what's happening" deserves one focused table or a single section, not a ten-section report. A small page that answers the question is a complete output, not an incomplete one — save the full multi-section treatment for when the content earns it.

**Who is looking?** A developer understanding a system? A PM seeing the big picture? A team reviewing a proposal? This shapes information density and visual complexity.

**What type of content?** Architecture, flowchart, sequence, data flow, schema/ER, state machine, mind map, class diagram, C4 architecture, data table, timeline, dashboard, or prose-first page. Each has distinct layout needs and rendering approaches (see Diagram Types below).

**What aesthetic?** Pick one and commit. The constrained aesthetics are safer — they have specific requirements that prevent generic output.

**Constrained aesthetics (prefer these):**
- Blueprint (technical drawing feel, subtle grid background, deep slate/blue palette, monospace labels, precise borders)
- Editorial (expressive serif headlines — pick from `./references/libraries.md`, generous whitespace, muted earth tones or deep navy + gold)
- Paper/ink (warm cream `#faf7f5` background, terracotta/sage accents, informal feel)
- Monochrome terminal (green/amber on near-black, monospace everything, CRT glow optional)
- Engraved ledger (formal document-of-record: ivory paper, thin double-rule borders and a centered small-caps title block, oxblood + deep-green ink accents, numbered clauses/figures, `tabular-nums` everywhere — dignity through restraint, zero ornament beyond the rules)
- Risograph zine (playful print: exactly two saturated spot colors — e.g. fluorescent pink + teal, or orange + royal blue — plus paper white, faint grain texture via CSS noise, chunky rounded sans headlines, sticker-style badges, the occasional ≤1.5° rotation on a label; body text always set in the darker ink — the bright ink is for shapes and badges only; the two-ink constraint is what keeps it charming instead of chaotic)
- Field guide (naturalist specimen plate: soft warm paper, moss/fern/bark greens with one berry accent, numbered figures with keyed legends ("Fig. 3 — job runner"), italic serif captions under every diagram, thin single-rule frames — calm, observational, precise)

**Flexible aesthetics (use with caution):**
- IDE-inspired (borrow a real, named color scheme: Dracula, Nord, Catppuccin Mocha/Latte, Solarized Dark/Light, Gruvbox, One Dark, Rosé Pine) — commit to the actual palette, don't approximate
- Data-dense (small type, tight spacing, maximum information, muted colors)

Never pick a forbidden aesthetic — see Anti-Patterns (AI Slop) below before choosing.

Vary the choice each time — and vary *structure*, not just palette. Two pages with different colors but the same stagger animation, label recipe, and card grammar still read as siblings from the same generator. Rotate the structural grammar too: labeling voice (mono tabs / small-caps / serif italic), motion (staggered reveals on one page, deliberately motionless the next), and composition (card grid / swimlanes / annotation rail). If the last diagram was dark and technical, make the next one light and editorial.

### 2. Structure

**Read the reference material** before generating. Don't memorize it — read it each time to absorb the patterns. Templates teach *patterns*, not prose: every example name, figure, and sentence in a template is scaffolding to replace with the real subject's content. Template filler surviving into a delivered page is a defect.
- For text-heavy architecture overviews (card content matters more than topology): read `./templates/architecture.html`
- For any Mermaid diagram (flowcharts, sequence, ER, state machines, mind maps, class, C4): read `./references/mermaid.md` and `./templates/mermaid-flowchart.html`
- For data tables, comparisons, audits, feature matrices: read `./templates/data-table.html`
- For slide decks: see Slide Deck Mode below
- For prose-heavy publishable pages (READMEs, articles, essays): read "Prose Page Elements" in `./references/css-patterns.md` and "Typography by Content Voice" in `./references/libraries.md`
- For interactive tools (triage boards, config editors, tuners, curation tables, annotators): read `./references/tool-patterns.md`

**For CSS/layout patterns and SVG connectors**, read `./references/css-patterns.md`.

**For pages with 4+ sections** (reviews, recaps, dashboards), also read `./references/responsive-nav.md` for section navigation with sticky sidebar TOC on desktop and horizontal scrollable bar on mobile.

**Choosing a rendering approach:**

| Content type | Approach | Why |
|---|---|---|
| Architecture (text-heavy) | CSS Grid cards + flow arrows | Rich card content (descriptions, code, tool lists) needs CSS control |
| Architecture (topology-focused) | **Mermaid** | Visible connections between components need automatic edge routing |
| Flowchart / pipeline | **Mermaid** | Automatic node positioning and edge routing |
| Sequence diagram | **Mermaid** | Lifelines, messages, and activation boxes need automatic layout |
| Data flow | **Mermaid** with edge labels | Connections and data descriptions need automatic edge routing |
| ER / schema diagram | **Mermaid** | Relationship lines between many entities need auto-routing |
| State machine | **Mermaid** | State transitions with labeled edges need automatic layout |
| Mind map | **Mermaid** | Hierarchical branching needs automatic positioning |
| Class diagram | **Mermaid** | Inheritance, composition, aggregation lines with automatic routing |
| C4 architecture | **Mermaid** | Use `graph TD` + `subgraph` (not native `C4Context` — it ignores themes) |
| Data table | HTML `<table>` | Semantic markup, accessibility, copy-paste behavior |
| Timeline | CSS (central line + cards) | Simple linear layout doesn't need a layout engine |
| Dashboard | CSS Grid + Chart.js | Card grid with embedded charts |
| Document corpus | HTML + client-side JS browser | Many docs need nav, search, and facet filtering — see `./references/browser-patterns.md` |
| Interactive tool | HTML + client-side JS + export | Editing state must round-trip back as text — see `./references/tool-patterns.md` |

**Mermaid rules live in `./references/mermaid.md`** — theming, the required `diagram-shell` container pattern, zoom/pan/export controls, export safety, scaling limits, and syntax caveats. Read it before writing any Mermaid. The two rules worth repeating: **never use bare `<pre class="mermaid">`** (copy the `diagram-shell` pattern from `./templates/mermaid-flowchart.html` wholesale), and never cram 15+ elements into one diagram (use the hybrid pattern — see Architecture below).

**AI-generated illustrations (optional).** If surf-cli is available (`which surf`), you can generate and embed images for hero banners and conceptual illustrations — see `./references/imagery.md` for the workflow, when to use it, and prompt craft. Degrade gracefully: if surf isn't available, skip images without erroring.

### 3. Style

Apply these principles to every diagram:

**Typography is the diagram.** Pick a distinctive font pairing from the list in `./references/libraries.md`. Every page should use a different pairing from recent generations. Load via `<link>` in `<head>`, with a system font fallback in the stack for offline resilience. Before choosing, write down 2-3 concrete words for the content's voice ("dense and unimpressed", "calm and careful") and pick to match those words — not the font you reached for last time. Good starting points:
- Sora + Spline Sans Mono (technical, precise)
- Besley + Martian Mono (editorial, sharp)
- Hanken Grotesk + JetBrains Mono (reliable, readable)
- Bricolage Grotesque + Fragment Mono (bold, characterful)
- Gabarito + Victor Mono (rounded, approachable)

Hierarchy needs contrast: keep at least a 1.25× size ratio between type-scale steps (fewer sizes, more contrast beats many near-identical sizes). Cap body text at ~65-75ch. On dark backgrounds, add 0.05-0.1 to your normal line-height — light-on-dark type reads lighter and needs the room.

**Color tells a story.** Use CSS custom properties for the full palette. Define at minimum: `--bg`, `--surface`, `--border`, `--pattern`, `--text`, `--text-bright`, `--text-dim`, and 3-5 accent colors, each with a dim variant and a fill/on-fill pair. Name variables semantically (`--pipeline-step` not `--blue-3`). Support both themes.

Good accent palettes — these are the **light-theme ink** tones, deep enough to carry 11px badge text (the tightest constraint on the page). On dark themes the ink flips bright, and the fill tone stays deep in both:
- Terracotta + sage (`#c2410c`, `#4c7a0b`) — warm, earthy
- Teal + slate (`#0f766e`, `#0369a1`) — technical, precise
- Rose + cranberry (`#be123c`, `#881337`) — editorial, refined
- Amber + emerald (`#b45309`, `#15803d`) — data-focused
- Deep blue + gold (`#1e3a5f`, `#8a6508`) — premium, sophisticated

The half-step versions of these (`#65a30d`, `#0891b2`, `#d97706`, `#059669`, `#d4a73a`) are the reflex picks and all land at 3.1–3.7:1 on a light surface. They're excellent as *dark-theme* ink and as bright fills under dark text — just not as light-theme text.

Prefer OKLCH (or `color-mix`) when constructing palettes — equal lightness steps actually *look* equal, unlike HSL. As colors approach white or black, reduce chroma; high chroma at extreme lightness looks garish. Tint every neutral — backgrounds, surfaces, near-black text — toward the page's accent hue (even 1-2% is perceptible and makes surfaces and accents feel like one system). On colored backgrounds, set secondary text in a shade of the background's hue rather than gray.

**Every accent needs two tones.** A single `--accent` cannot be both a readable text color and a background fill — that's the root of almost every unreadable page. Define each accent as a pair:

- `--accent` — the **ink** tone. Used for text, icons, borders. Must clear **4.5:1 against `--surface`**. On light pages this means a deep tone (`#0f766e`, not `#14b8a6`); on dark pages a bright one.
- `--accent-fill` — the **fill** tone, used as a background behind text. Pair it with `--accent-on-fill`, the ink that sits *on* it — near-black for light/bright fills, near-white for deep fills. Never `#fff` by reflex.

The failure this prevents: a bright accent (`#50fa7b`, `#fb923c`, `#d4a73a`, `#22d3ee`) used as a solid fill with white text on top lands at **1.4–2.7:1** — unreadable. Bright accents take dark ink. Only deep, desaturated fills take light ink.

**The contrast floor is not negotiable.** Every text/background pair on the page must clear:

| Text | Floor | Applies to |
|---|---|---|
| Body copy, bullets, card descriptions | **4.5:1** | Anything a reader reads in sequence |
| Labels, badges, chips, captions under 14px | **4.5:1** | Small type needs *more* contrast, not less |
| Large display type (24px+, or 19px+ bold) | **3:1** | Headings, hero numbers |
| Borders, icons, focus rings, chart strokes | **3:1** | Non-text UI that carries meaning |

`--text-dim` is for genuinely secondary information — captions, timestamps, provenance. It is **not** a body-copy color. If bullets, descriptions, or table cells are set in `--text-dim`, the page is under-contrast by construction; use `--text` and create hierarchy with size and weight instead. And `--text-dim` itself must still clear 4.5:1 against every surface it lands on.

Full palette scaffolding — the token set, the ink/fill pairs, and a runnable checker — is in "The Contrast Contract" in `./references/css-patterns.md`.

**Decoration stays behind surfaces, never behind prose.** Grid lines, diagonal rules, dot fields, and hatch patterns belong to the *page* background, at an alpha low enough to read as texture rather than lines (≤0.06 in light, ≤0.05 in dark). Text sitting directly on a patterned background is a defect: either put the text on an opaque `--surface` card, or drop the pattern out from behind it. Never reuse `--border` as the pattern color — border alpha is tuned for a crisp 1px edge, and at 24–48px repeat spacing it reads as an aggressive ruled grid.

Fonts and colors have hard exclusions — check the Anti-Patterns (AI Slop) section before committing a pairing or palette.

Put your primary aesthetic in `:root` and the alternate in the media query:

```css
/* Light-first (editorial, paper/ink, blueprint): */
:root { /* light values */ }
@media (prefers-color-scheme: dark) { :root { /* dark values */ } }

/* Dark-first (IDE-inspired, terminal): */
:root { /* dark values */ }
@media (prefers-color-scheme: light) { :root { /* light values */ } }
```

**Surfaces whisper, they don't shout.** Build depth through subtle lightness shifts (2-4% between levels), not dramatic color changes. Borders should be low-opacity rgba (`rgba(255,255,255,0.08)` in dark mode, `rgba(0,0,0,0.08)` in light) — visible when you look, invisible when you don't.

**Backgrounds create atmosphere.** Don't use flat solid colors for the page background. Subtle gradients, faint grid patterns via CSS, or gentle radial glows behind focal areas. The background should feel like a space, not a void.

**Visual weight signals importance.** Not every section deserves equal visual treatment. Executive summaries and key metrics should dominate the viewport on load (larger type, more padding, subtle accent-tinted background zone). Reference sections (file maps, dependency lists, decision logs) should be compact and stay out of the way. Use `<details>/<summary>` for sections that are useful but not primary — the collapsible pattern is in `./references/css-patterns.md`.

**Surface depth creates hierarchy.** Vary card depth to signal what matters: hero sections elevated with accent-tinted backgrounds (`ve-card--hero`), body content flat (default `.ve-card`), code blocks recessed (`ve-card--recessed`). See the depth tiers in `./references/css-patterns.md`. When everything pops, nothing does.

**Animation earns its place.** Staggered fade-ins on page load are almost always worth it — they guide the eye through the diagram's hierarchy. Mix animation types by role: `fadeUp` for cards, `fadeScale` for KPIs and badges, `drawIn` for SVG connectors, `countUp` for hero numbers. Hover transitions on interactive-feeling elements make the diagram feel alive. Always respect `prefers-reduced-motion`. CSS handles most cases; for orchestrated multi-element sequences, anime.js via CDN is available (see `./references/libraries.md`). Keep animation purposeful — entrance reveals, hover feedback, user-initiated interactions; the forbidden motion patterns are in Anti-Patterns below.

### 4. Verify

Do not deliver until every check passes:

- **The squint test**: Blur your eyes. Can you still perceive hierarchy? Are sections visually distinct?
- **The contrast pass**: Run `python3 ~/.claude/skills/visual-explainer/scripts/check-contrast.py <file.html>`. It resolves the CSS custom properties for both themes and reports every text/background pair below its floor, plus hardcoded light-ink-on-accent-fill and over-intense background patterns. Fix every `FAIL` before delivering; `WARN` needs a deliberate reason to keep. This catches what the eye doesn't — a 3.2:1 badge looks fine in isolation and is unreadable in context.
- **Text on decoration**: Scan for prose sitting directly on a striped, ruled, or dot-grid background with no surface between them. If the pattern is legible as *lines* behind a sentence, it's too strong.
- **The swap test**: Would replacing your fonts and colors with a generic dark theme make this indistinguishable from a template? If yes, push the aesthetic further.
- **The slop test**: Review the page against the Anti-Patterns (AI Slop) section below. Two or more slop signals means regenerate with a different aesthetic direction.
- **Both themes**: Toggle your OS between light and dark mode. Both should look intentional, not broken.
- **Information completeness**: Does the diagram actually convey what the user asked for? Pretty but incomplete is a failure.
- **No overflow**: Resize the browser to different widths. No content should clip or escape its container. Every grid and flex child needs `min-width: 0`. Side-by-side panels need `overflow-wrap: break-word`. Never use `display: flex` on `<li>` for marker characters. See Overflow Protection in `./references/css-patterns.md`.
- **Mermaid opens fully visible**: Every diagram must show its *entire* graph on load — scaled down to fit, never opened zoomed into a corner with the rest off-screen. Check the zoom label reads `fit` (or `capped` on a small diagram); a reading above 100% on anything but a tiny diagram means the contain-fit was broken in adaptation. On slides, confirm nothing runs off the bottom — there's no scrolling to recover it. If a diagram is too small to read once it fits, cut nodes or split it; don't scale it up past the container.
- **Mermaid interaction**: On scrollable pages, every `.mermaid-wrap` carries the full engine — zoom controls, a non-clipping `WebP` export button, Ctrl/Cmd+scroll zoom, drag panning, and click-to-expand; test the expanded tab and WebP output per the export-safety checklist in `./references/mermaid.md`. On slide decks, diagrams are click-to-expand only (see `./references/slide-patterns.md`).
- **No template filler**: Search the page for the templates' example content — names, metrics, subject matter. Every word must come from the actual subject.
- **Look at the render**: When browser automation is available, open the file and screenshot it — run the squint test on the actual render, not your mental model of it.
- **File opens cleanly**: No console errors, no broken font loads, no layout shifts.
- **Single self-contained file** (see File Structure): no local-file references. `grep -oE '(src|href)="[^"]*"' file.html` must show only `data:` URIs and `https://` URLs — never a local path (`./img.png`, `assets/…`, an absolute disk path).

### 5. Deliver

**Output location:** Write to `~/.agent/diagrams/`. Use a descriptive filename based on content: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. The directory persists across sessions.

**Ship one file** (see File Structure): confirm every local asset is a `data:` URI before delivering — a CDN `<link>` is fine.

**Optional — embed fonts for offline/CSP hardening.** Only when the page must also render with no network or on a strict-CSP host (e.g. claude.ai Artifacts):

```bash
python3 ~/.claude/skills/visual-explainer/scripts/embed-fonts.py ~/.agent/diagrams/filename.html
```

It fetches the Google Fonts `<link>`s, embeds the `latin`/`latin-ext` woff2 subsets as base64 `@font-face`, and strips the external `<link>`/`preconnect` tags. Pass `--subsets latin,latin-ext,cyrillic` (or `all`) for glyphs outside those subsets (e.g. `№`, Greek). Mermaid and Chart.js still need the network; a fully offline page should avoid them.

**Stamp provenance:** End the page with a small dim footer — generation date, the git branch and short commit hash when the subject is a repository, and the key files or documents the page was built from. Explainers describe moving targets; the stamp makes staleness self-evident and gives `fact-check` an anchor.

**Open in browser:**
- macOS: `open ~/.agent/diagrams/filename.html`
- Linux: `xdg-open ~/.agent/diagrams/filename.html`

**Tell the user** the file path so they can re-open or share it.

**Refresh the index in the background:** after delivering, launch a background subagent to rebuild the launcher page per `./commands/index.md` — never block or interleave the main task on it.

## Diagram Types

### Architecture / System Diagrams
Three approaches depending on complexity:

**Simple topology (under 10 elements):** Use Mermaid. A `graph TD` with custom `themeVariables` produces readable diagrams with automatic edge routing.

**Text-heavy overviews (under 15 elements):** CSS Grid with explicit row/column placement. Sections as rounded cards with colored borders and monospace labels. Vertical flow arrows between sections. The reference template at `./templates/architecture.html` demonstrates this pattern. Use when cards need descriptions, code references, tool lists, or other rich content that Mermaid nodes can't hold.

**Complex architectures (15+ elements):** Use the **hybrid pattern** — a simple Mermaid overview (5-8 nodes showing module relationships) followed by detailed CSS Grid cards for each module's internals. This gives you visual topology AND readable details. Never try to cram 15+ elements into a single Mermaid diagram — it will render unreadably small even with zoom controls.

### Flowcharts / Pipelines
**Use Mermaid.** Automatic node positioning and edge routing produces proper diagrams with connecting lines, decision diamonds, and parallel branches. Prefer `graph TD`; use `graph LR` only for simple 3-4 node linear flows. Color-code node types with `classDef` or rely on `themeVariables`.

### Sequence Diagrams
**Use Mermaid** `sequenceDiagram` syntax. Style actors and messages via CSS overrides on `.actor`, `.messageText`, `.activation`.

### Data Flow Diagrams
**Use Mermaid.** `graph TD` with edge labels for data descriptions. Thicker, colored edges for primary flows; source/sink nodes styled differently from transform nodes via `classDef`.

### Schema / ER Diagrams
**Use Mermaid** `erDiagram` syntax with entity attributes. Style via `themeVariables` and CSS overrides on `.er.entityBox` and `.er.relationshipLine`.

### State Machines / Decision Trees
**Use Mermaid** `stateDiagram-v2` for states with labeled transitions. **Caveat:** transition labels have a strict parser — if labels need colons, parentheses, or line breaks, use `flowchart TD` instead. See "stateDiagram-v2 Label Limitations" in `./references/mermaid.md`. Decision trees can use `graph TD` with diamond decision nodes.

### Mind Maps / Hierarchical Breakdowns
**Use Mermaid** `mindmap` syntax. Mermaid handles the radial layout automatically; style node colors per depth level via `themeVariables`.

### Class Diagrams
**Use Mermaid** `classDiagram` syntax for domain modeling and OOP design with typed properties, methods, multiplicity labels, and `<<interface>>`/`<<abstract>>` markers. For simple entity boxes without OOP semantics, prefer `erDiagram` — it produces cleaner output for pure data modeling.

### C4 Architecture Diagrams
**Use Mermaid flowchart syntax — NOT native `C4Context`** (it hardcodes its own fonts and colors and ignores `themeVariables`). Use `graph TD` with `subgraph` blocks for C4 boundaries. The full flowchart-as-C4 node mapping is in `./references/mermaid.md`.

### Data Tables / Comparisons / Audits
Use a real `<table>` element — not CSS Grid pretending to be a table. Tables get accessibility, copy-paste behavior, and column alignment for free. The reference template at `./templates/data-table.html` demonstrates all patterns below. This is the format for the proactive ASCII-table replacement described at the top of this skill.

Layout patterns:
- Sticky `<thead>` so headers stay visible when scrolling long tables
- Alternating row backgrounds via `tr:nth-child(even)` (subtle, 2-3% lightness shift)
- First column optionally sticky for wide tables with horizontal scroll
- Responsive wrapper with `overflow-x: auto` for tables wider than the viewport
- Column width hints via `<colgroup>` or `th` widths — let text-heavy columns breathe
- Row hover highlight for scanability

Status indicators (use styled `<span>` elements, never emoji):
- Match/pass/yes: colored dot or checkmark with green background
- Gap/fail/no: colored dot or cross with red background
- Partial/warning: amber indicator
- Neutral/info: dim text or muted badge

Cell content:
- Wrap long text naturally — don't truncate or force single-line
- Use `<code>` for technical references within cells
- Secondary detail text in `<small>` with dimmed color
- Keep numeric columns right-aligned with `tabular-nums`

### Timeline / Roadmap Views
Vertical or horizontal timeline with a central line (CSS pseudo-element). Phase markers as circles on the line. Content cards branching left/right (alternating) or all to one side. Date labels on the line. Color progression from past (muted) to future (vivid).

### Dashboard / Metrics Overview
One dominant metric owns the view (large numerals, accent color); supporting figures ride inline in a sentence or a compact strip — a uniform grid of identical KPI cards is the hero-metric cliché (see Anti-Patterns). Sparklines via inline SVG `<polyline>`. Progress bars via CSS `linear-gradient` on a div. For real charts (bar, line, pie), use **Chart.js via CDN** (see `./references/libraries.md`). Trend indicators (up/down arrows, percentage deltas) attach to the figures they describe.

### Implementation Plans

For visualizing implementation plans, extension designs, or feature specifications. The goal is **understanding the approach**, not reading the full source code.

**Don't dump full files.** Displaying entire source files inline overwhelms the page and defeats the purpose of a visual explanation. Instead:
- Show **file structure with descriptions** — list functions/exports with one-line explanations
- Show **key snippets only** — the 5-10 lines that illustrate the core logic
- Use **collapsible sections** for full code if truly needed

**Code blocks require explicit formatting.** Without `white-space: pre-wrap`, code runs together into an unreadable wall. See "Code Blocks" in `./references/css-patterns.md`.

**Structure for implementation plans:**
1. Overview/purpose (what problem does this solve?)
2. Flow diagram (Mermaid or CSS cards)
3. File structure with descriptions (not full code)
4. Key implementation details (snippets)
5. API/interface summary
6. Usage examples

### Document Browsers (Corpora of Reports, Notes, Writeups)

When the user has a **corpus** — many documents to peruse rather than one thing to explain — build a browser: nav + search + facet filters + reader pane, full corpus embedded, all interaction client-side. Read `./references/browser-patterns.md` before building one; it holds the layout spectrum (reader-first / corpus-first / table-first), the master–detail skeleton, the facet-derivation rule, and the browser-specific verify checks.

### Interactive Tools (Throwaway Editors)

When the user needs to **act on** data rather than read about it — reorder tickets, edit a config, tune parameters, curate rows, annotate a transcript, pick a hard-to-type value — build a throwaway tool: a single-file editor purpose-built for that one dataset and job, pre-filled with your best guess, ending in an export button that **round-trips** the result back as text to paste into the conversation or commit to a file. Read `./references/tool-patterns.md` before building one; it holds the round-trip contract, the tool-type catalog, state/export mechanics, and the tool-specific verify checks.

### Documentation (READMEs, Library Docs, API References)

When visualizing documentation, extract structure into visual elements:

| Content | Visual Treatment |
|---------|------------------|
| Features | Card grid (2-3 columns) |
| Install/setup steps | Numbered cards or vertical flow |
| API endpoints/commands | Table with sticky header |
| Config options | Table |
| Architecture | Mermaid diagram or CSS card layout |
| Comparisons | Side-by-side panels or table |
| Warnings/notes | Callout boxes |

Don't just format the prose — transform it. A feature list becomes a card grid. Install steps become a numbered flow. An API reference becomes a table.

### Prose Accent Elements

Use these sparingly within visual pages to highlight key points or provide breathing room. See "Prose Page Elements" in `./references/css-patterns.md` for CSS patterns.

- **Lead paragraph** — larger intro text to set context before diving into cards/grids
- **Pull quote** — highlight a key insight; one per page maximum
- **Callout box** — warnings, tips, important notes
- **Section divider** — visual break between major sections

## Slide Deck Mode

An alternative output format presenting content as a magazine-quality slide deck instead of a scrollable page. **Opt-in only** — generate slides when the user invokes `/generate-slides`, passes `--slides` to another command (same data-gathering, slide presentation, same breadth of coverage), or explicitly asks for a deck. Never auto-select slide format.

**Before generating any slides**, read `./references/slide-patterns.md` — the planning process (inventory the source, map every item to slides, verify coverage: every section, decision, and data point must appear in the deck), the slide engine CSS/JS, the 10 slide types, presets, imagery workflow, and compositional-variety rules all live there. Also read `./templates/slide-deck.html` (reference implementation), `./references/css-patterns.md`, and `./references/mermaid.md` if the deck contains diagrams.

## File Structure

Every diagram is a **single self-contained `.html` file** — one file that can be sent on its own and open correctly. The rule is about *local* assets, not the network: every generated image or asset is inlined as a `data:` URI, never referenced by a local path. CDN `<link>`/`<script>` URLs (fonts, Mermaid, Chart.js, icons) are allowed — they add no sidecar files. Fonts can optionally be embedded too (Deliver step) for offline/CSP hardening.

**Degradation tiers.** CDN links are progressive enhancement — the page must stay readable with every one of them blocked: fonts fall back to the system stack (always include one), icons vanish but their text labels remain, Mermaid failures render the diagram source via a `.catch` fallback, and charts sit beside the figures they visualize rather than replace them. **Hosting caveat:** claude.ai Artifacts and other strict-CSP hosts block all external requests, so CDN-dependent pages break there — for those targets, embed the fonts (Deliver step) and skip Mermaid/Chart.js.

Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Title</title>
  <!-- CDN font link is fine — ships as a single file -->
  <link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties, theme, layout, components — all inline */
  </style>
</head>
<body>
  <!-- Semantic HTML: sections, headings, lists, tables, inline SVG -->
  <!-- Optional: <script> for Mermaid, Chart.js, or anime.js when used -->
</body>
</html>
```

## Sharing Pages

Pages can be deployed to a public Vercel URL (no account needed) via `scripts/share.sh` when a Pi-compatible `vercel-deploy` skill is installed. Usage, install paths, requirements, and caveats are in `./commands/share-page.md`. Remember: deployments are public — anyone with the URL can view.

## Anti-Patterns (AI Slop)

The single home for everything forbidden. These patterns signal "AI-generated template" and undermine the skill's purpose of producing distinctive, high-quality pages. Review every generated page against this list (the slop test in Verify).

### Typography

**Forbidden fonts as primary `--font-body`:**
- Inter — the single most overused AI default
- Roboto, Arial, Helvetica — generic system fallbacks promoted to primary
- system-ui, sans-serif alone — no character, no intent

**Monoculture fonts — avoid as reflex picks.** These are training-data defaults that make every AI-generated page look related: Instrument Serif, Instrument Sans, DM Sans, DM Serif Display/Text, IBM Plex (Sans/Serif/Mono), Plus Jakarta Sans, Space Grotesk, Space Mono, Outfit, Fraunces, Playfair Display, Crimson Pro/Text, Cormorant, Newsreader, Lora, Syne. They aren't broken fonts — but if one of these is your first instinct, that's the trained reflex talking.

**Required:** Pick from the font pairings in `./references/libraries.md`. Every generation should use a different pairing from the last.

### Color Palette

**Forbidden accent colors:**
- Indigo-500/violet-500 (`#8b5cf6`, `#7c3aed`, `#a78bfa`) — Tailwind's default purple range
- Fuchsia (`#d946ef`) and the cyan + magenta + pink neon gradient combination (`#06b6d4` → `#d946ef` → `#f472b6`)
- Any palette that could be described as "Tailwind defaults with purple/pink/cyan accents"

**Forbidden color effects:**
- Gradient text on headings (`background: linear-gradient(...); background-clip: text;`) — this screams AI-generated
- Multiple overlapping radial glows in accent colors creating a "neon haze"
- Pure `#000` backgrounds or pure `#fff` text/backgrounds — always tint toward the palette's hue
- Gray text sitting on a colored background — it reads washed out; use a shade of the background hue

**Required:** Build palettes from the good accent palettes in the Style step or derive from real IDE themes (Dracula, Nord, Solarized, Gruvbox, Catppuccin). Accents should feel intentional, not default.

### Contrast & Legibility

Unreadable is worse than ugly. A page that looks striking in a screenshot and can't be read is a failed page.

**Forbidden:**
- **White or near-white text on a mid-tone or bright fill** — white on pale green, mint, amber, sky, coral, or lime. This is the most common readability failure in generated pages; the bright accents that look great as *text on dark* land at 1.4–2.7:1 as *fills under white*. Bright fill takes dark ink.
- `color: #fff` (or `var(--bg)`) hardcoded on top of `background: var(--accent)` without checking which tone the accent actually is. It passes in one theme and fails in the other.
- Accent-colored text at 10–12px on a tint of that same accent (status badges, tags, code chips, callout titles). Deep-enough-to-read on light backgrounds means deep — `#059669`, `#d97706`, and `#0891b2` all sit at 3.1–3.7:1 and fail.
- Body copy, bullets, or table cells set in `--text-dim`.
- Free-floating text over a striped, hatched, ruled, or dot-grid background — including text over a repeating-gradient "dead time" bar or a patterned progress segment.
- Background line patterns drawn in `--border`, or at above ~0.06 alpha, or at a repeat spacing tight enough (under ~20px) to read as stripes rather than texture.
- Decorative watermark numerals or quote marks behind text at an opacity high enough to compete with it (keep ≤0.08).
- Text over a background image or bold gradient with no scrim between them.

**Required:** Two-tone accents (ink + fill), the contrast floors from the Style step, decoration behind surfaces rather than behind prose, and a scrim under any text over imagery. Verify with `scripts/check-contrast.py` rather than by eye — the failures are systematic, not obvious.

### Motion

**Forbidden animations:**
- Animated glowing box-shadows (`@keyframes glow { box-shadow: 0 0 20px... }`)
- Pulsing/breathing effects on static content
- Continuous animations that run after page load (except progress indicators)

Nothing should glow or pulse on its own.

### Section Headers

**Forbidden:**
- Emoji icons in section headers (🏗️, ⚙️, 📁, 💻, 📅, 🔗, ⚡, 🔧, 📦, 🚀, etc.)
- Section headers that all use the same icon-in-rounded-box pattern

**Required:** Vary the labeling voice between generations — numbered mono tabs, small-caps headers, serif italic labels, asymmetric section dividers (the templates each demonstrate a different one). If an icon is genuinely needed, use a Lucide icon via the Iconify web component (see "Icons" in `./references/libraries.md`) or a palette-matched inline SVG — not emoji.

### Accent Side-Stripes

**Forbidden:** `border-left` (or `border-right`) wider than 1px used as a colored accent stripe on cards, callouts, alerts, list items, or pull quotes — hard-coded colors and CSS variables alike (`border-left: 3px solid var(--accent)` is just as banned as `border-left: 4px solid red`). This is the single most recognizable AI "design touch" in dashboards and docs; it never looks intentional regardless of color or radius.

**Required:** Rewrite the element with a different structure entirely — a full 1px border tinted toward the accent, an accent-tinted background (`color-mix(in srgb, var(--accent) 8%, transparent)`), a leading label/number/dot in the accent color, or no indicator at all. Don't just swap the stripe for an inset box-shadow. (A 2px active-state indicator in a nav/TOC is a functional affordance, not a decorative stripe — that's fine.)

### Layout & Hierarchy

**Forbidden:**
- Perfectly centered everything with uniform padding
- All cards styled identically with the same border-radius, shadow, and spacing
- Every section getting equal visual treatment — no hero/primary vs. secondary distinction
- Symmetric layouts where left and right halves mirror each other

**Required:** Vary visual weight. Hero sections should dominate (larger type, more padding, accent-tinted background). Reference sections should feel compact. Use the depth tiers (hero → elevated → default → recessed). Asymmetric layouts create interest.

### Template Patterns

**Forbidden:**
- Three-dot window chrome (red/yellow/green dots) on code blocks — this is a cliché
- KPI cards where every metric has identical gradient text treatment
- "Neon Dashboard" as an aesthetic choice (cyan + magenta + purple on dark) — it always produces AI slop
- Gradient meshes with pink/purple/cyan blobs in the background

**Required:** Code blocks use a simple header with filename or language label. KPI cards vary by importance — hero numbers for the primary metric, subdued treatment for supporting metrics. Pick aesthetics with natural constraints (Blueprint, Editorial, Paper/ink).

### The Slop Test

**Would a developer looking at this page immediately think "AI generated this"?** The telltale signs:

1. Inter or Roboto font with purple/violet gradient accents
2. Every heading has `background-clip: text` gradient
3. Emoji icons leading every section
4. Glowing cards with animated shadows
5. Cyan-magenta-pink color scheme on dark background
6. Perfectly uniform card grid with no visual hierarchy
7. Three-dot code block chrome
8. Colored accent stripes (`border-left: 3px+`) on cards and callouts
9. The same two or three "safe" fonts (Instrument Serif, DM Sans, IBM Plex) as every generation before

If two or more of these are present, the page is slop. Regenerate with a different aesthetic direction — Editorial, Blueprint, Paper/ink, or a specific IDE theme. These constrained aesthetics are harder to mess up because they have specific visual requirements that prevent defaulting to generic patterns.
