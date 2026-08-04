# Diagram Types

Per-type detail for each content type. The decision table in `../SKILL.md` (content type → rendering approach) picks the approach; this file holds the specifics of building it. For the page's overall structural shape (funnel, quadrant, pyramid, waterfall, zigzag, …) see `./structures.md`.

## Architecture / System Diagrams

Three approaches by complexity:

- **Simple topology (under 10 elements):** Mermaid. A `graph TD` with custom `themeVariables` gives readable output with automatic edge routing.
- **Text-heavy overviews (under 15 elements):** CSS Grid with explicit row/column placement. Sections as rounded cards with colored borders and monospace labels; vertical flow arrows between sections. See `../templates/architecture.html`. Use when cards need descriptions, code references, tool lists, or other rich content Mermaid nodes can't hold.
- **Complex architectures (15+ elements):** the **hybrid pattern** — a simple Mermaid overview (5–8 nodes showing module relationships) followed by detailed CSS Grid cards for each module's internals. This gives visual topology and readable detail. A single Mermaid diagram with 15+ elements renders unreadably small even with zoom controls; split it.

## Flowcharts / Pipelines

Mermaid. Automatic node positioning and edge routing produce connecting lines, decision diamonds, and parallel branches. Prefer `graph TD`; use `graph LR` only for simple 3–4 node linear flows. Color-code node types with `classDef` or rely on `themeVariables`.

## Sequence Diagrams

Mermaid `sequenceDiagram`. Style actors and messages via CSS overrides on `.actor`, `.messageText`, `.activation`.

## Data Flow Diagrams

Mermaid `graph TD` with edge labels for data descriptions. Thicker, colored edges for primary flows; source/sink nodes styled differently from transform nodes via `classDef`.

## Schema / ER Diagrams

Mermaid `erDiagram` with entity attributes. Style via `themeVariables` and CSS overrides on `.er.entityBox` and `.er.relationshipLine`.

## State Machines / Decision Trees

Mermaid `stateDiagram-v2` for states with labeled transitions. **Caveat:** transition labels have a strict parser — if labels need colons, parentheses, or line breaks, use `flowchart TD` instead. See "stateDiagram-v2 Label Limitations" in `./mermaid.md`. Decision trees can use `graph TD` with diamond decision nodes.

## Mind Maps / Hierarchical Breakdowns

Mermaid `mindmap`. Mermaid handles the radial layout; style node colors per depth level via `themeVariables`.

## Class Diagrams

Mermaid `classDiagram` for domain modeling and OOP design with typed properties, methods, multiplicity labels, and `<<interface>>`/`<<abstract>>` markers. For simple entity boxes without OOP semantics, prefer `erDiagram` — cleaner output for pure data modeling.

## C4 Architecture Diagrams

Use Mermaid flowchart syntax, not native `C4Context` — `C4Context` hardcodes its own fonts and colors and ignores `themeVariables`. Use `graph TD` with `subgraph` blocks for C4 boundaries. The full flowchart-as-C4 node mapping is in `./mermaid.md`.

## Data Tables / Comparisons / Audits

Use a real `<table>` element — CSS Grid pretending to be a table loses accessibility, copy-paste behavior, and column alignment. `../templates/data-table.html` demonstrates every pattern below. This is the format for the proactive ASCII-table replacement.

Layout:
- Sticky `<thead>` so headers stay visible when scrolling long tables
- Alternating row backgrounds via `tr:nth-child(even)` (subtle, 2–3% lightness shift)
- First column optionally sticky for wide tables with horizontal scroll
- Responsive wrapper with `overflow-x: auto` for tables wider than the viewport
- Column width hints via `<colgroup>` or `th` widths — let text-heavy columns breathe
- Row hover highlight for scanability

Status indicators — styled `<span>` elements, never emoji:
- Match/pass/yes: colored dot or checkmark with green background
- Gap/fail/no: colored dot or cross with red background
- Partial/warning: amber indicator
- Neutral/info: dim text or muted badge

Cell content:
- Long text wraps naturally; keep it whole rather than truncating
- `<code>` for technical references within cells
- Secondary detail text in `<small>` with dimmed color
- Numeric columns right-aligned with `tabular-nums`

## Timeline / Roadmap Views

Vertical or horizontal timeline with a central line (CSS pseudo-element). Phase markers as circles on the line. Content cards branching left/right (alternating) or all to one side. Date labels on the line. Color progression from past (muted) to future (vivid).

## Dashboard / Metrics Overview

One dominant metric owns the view (large numerals, accent color); supporting figures ride inline in a sentence or a compact strip. A uniform grid of identical KPI cards is the hero-metric cliché — see `./anti-patterns.md`. Sparklines via inline SVG `<polyline>`. Progress bars via CSS `linear-gradient` on a div. For real charts (bar, line, pie), use Chart.js via CDN (see `./libraries.md`). Trend indicators (arrows, percentage deltas) attach to the figures they describe.

## Implementation Plans

The goal is **understanding the approach**, not reading the full source. Full files inline overwhelm the page and defeat the visual explanation. Instead:
- Show **file structure with descriptions** — functions/exports with a one-line explanation each
- Show **key snippets only** — the 5–10 lines that carry the core logic
- Use collapsible sections for full code when it is genuinely needed

Code blocks require `white-space: pre-wrap`; without it code runs together into a wall. See "Code Blocks" in `./css-patterns.md`.

Structure:
1. Overview/purpose (what problem does this solve?)
2. Flow diagram (Mermaid or CSS cards)
3. File structure with descriptions
4. Key implementation details (snippets)
5. API/interface summary
6. Usage examples

## Document Browsers (Corpora of Reports, Notes, Writeups)

When the user has a **corpus** — many documents to peruse rather than one thing to explain — build a browser: nav + search + facet filters + reader pane, full corpus embedded, all interaction client-side. Read `./browser-patterns.md` first; it holds the layout spectrum (reader-first / corpus-first / table-first), the master–detail skeleton, the facet-derivation rule, and the browser-specific verify checks.

## Interactive Tools (Throwaway Editors)

When the user needs to **act on** data rather than read about it — reorder tickets, edit a config, tune parameters, curate rows, annotate a transcript, pick a hard-to-type value — build a throwaway tool: a single-file editor for that one dataset and job, pre-filled with your best guess, ending in an export button that **round-trips** the result back as text. Read `./tool-patterns.md` first; it holds the round-trip contract, the tool-type catalog, state/export mechanics, and the tool-specific verify checks.

## Documentation (READMEs, Library Docs, API References)

Transform the prose into structure rather than reformatting it:

| Content | Visual treatment |
|---------|------------------|
| Features | Card grid (2–3 columns) |
| Install/setup steps | Numbered cards or vertical flow |
| API endpoints/commands | Table with sticky header |
| Config options | Table |
| Architecture | Mermaid diagram or CSS card layout |
| Comparisons | Side-by-side panels or table |
| Warnings/notes | Callout boxes |

## Prose Accent Elements

Use these sparingly within visual pages to highlight key points or provide breathing room. CSS patterns are in "Prose Page Elements" in `./css-patterns.md`.

- **Lead paragraph** — larger intro text setting context before the cards/grids
- **Pull quote** — one key insight; one per page maximum
- **Callout box** — warnings, tips, important notes
- **Section divider** — visual break between major sections
