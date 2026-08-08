---
name: html-craft
description: Craft self-contained HTML pages that keep the user in the loop on their own work — diagrams, plans with a live task ledger, data tables, doc browsers, slide decks, and single-file interactive tools that round-trip their result back as text. Use when the user asks for a diagram, comparison table, or any visual explanation of technical concepts; asks for a slide deck; wants an implementation plan tracked as work proceeds; wants to browse a corpus of docs or reports; wants several approaches laid out side by side; or needs a throwaway editor for the data at hand. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead.
license: MIT
compatibility: Requires a browser to view generated HTML files. Optional surf-cli for AI image generation.
metadata:
  author: josikinzz
  upstream: nicobailon/visual-explainer
  version: "1.0.0"
---

# HTML Craft

**The page is a working surface, not a report.** It keeps the user in the loop on their own work, and it does that two ways — most pages do both — while the conversation carries a third.

**Check.** Lead with the conclusion, then attach what it rests on. A claim about a real artifact — the user's code, their data, the state of their work — carries the evidence a reader would ask for next: the `file.py:88`, the command, the commit, the number instead of "significantly faster", the checklist in its real state instead of "mostly done". The reader takes the conclusion and checks it only if they want to. A page that explains a concept rather than asserting something about the user's work has nothing to audit, and this half does not bind it. A short answer in chat alongside a page carrying the detail is the normal split, not a failure to summarize.

**Steer.** The page is where the user gets back into the work, so give them something to act on and a way to hand it back: options to choose between, a status to correct, a list to reorder, a value to tune, a claim to mark wrong. Timing is the lever — a page delivered after the work is finished can only be audited, while the same page at a decision point changes what happens next. When a decision is live, put the page in front of the user before you commit to an answer. The round-trip export is the strongest form of this: the user edits, exports, and the result re-enters the work as text (`./references/tool-patterns.md`). Any page that asks the user to approve or pick must let them reject the framing, not only choose among your options — the full contract is "Asking the user" in `./references/tool-patterns.md`.

**Ask.** The conversation has its own channel, for decisions that cannot wait for a page. A **fork** is a decision that changes what you build or what a plan commits to, and that the request, the conversation, and the material leave open — scope, audience, which of two readings, whether a risky step belongs in the plan. Settle a fork by asking, not by guessing: use the harness's structured question tool (AskUserQuestion in Claude Code, a plain-text question elsewhere), with options that are genuinely different answers and your recommendation listed first, marked, with its one-line reason — the same contract as "Asking the user" in `./references/tool-patterns.md`. Bundle the open forks into one call rather than a drip of interruptions. Everything else — aesthetic, fonts, structure, weight — is yours to decide, and most sessions have no fork at all. A fork whose options carry tradeoffs worth seeing side by side outgrows the question box: build the `explore-options` grid instead.

**Proactive table rendering.** When you are about to present tabular data as an ASCII box-drawing table in the terminal (4+ rows or 3+ columns — comparisons, audits, feature matrices, status reports, requirement audits, API inventories), generate an HTML page instead. Do not wait to be asked. A brief text summary in chat is fine. The table belongs in the browser.

## Available Commands

Prompt templates in `./commands/`, invoked as slash commands namespaced by harness: `/html-craft:diff-review` in Claude Code, `/diff-review` in Pi. In Codex, if `~/.codex/prompts/` holds the templates, use `/prompts:diff-review`. Otherwise name the skill and describe the workflow.

| Command | What it does |
|---------|-------------|
| `generate-web-diagram` | Generate an HTML diagram for any topic |
| `generate-visual-plan` | Generate a visual implementation plan for a feature |
| `generate-slides` | Generate a magazine-quality slide deck |
| `diff-review` | Visual diff review with architecture comparison and code review |
| `plan-review` | Compare a plan against the codebase with risk assessment |
| `project-recap` | Mental model snapshot for context-switching back to a project |
| `browse-docs` | Document browser for a corpus of docs/reports with nav, search, and facets |
| `make-tool` | Throwaway single-file editor (triage board, config editor, tuner, annotator) with a round-trip export |
| `explore-options` | Exploration grid — distinctly different approaches side by side, each labeled with its tradeoff |
| `index` | Build/refresh the launcher index for `~/.agent/diagrams` — grouped by repo and date, staleness-flagged |
| `fact-check` | Verify accuracy of a document against actual code |
| `share-page` | Deploy an HTML page to Vercel and get a live URL |
| `publish-html-craft` | Publish a page to the private html-craft-pages repo — live at josiekins.xyz/html-craft/, unlisted and noindex |

## Workflow

### 1. Think (5 seconds, not 5 minutes)

Commit to a direction before writing HTML.

**What must the reader be able to check?** Name the claims the page makes about a real artifact, and the evidence each one needs. That list drives structure: the evidence sits next to its claim, not in an appendix.

**What is the reader about to decide?** Name the open decision, if there is one, and give it a handle on the page — the options side by side, the status they can correct, the export that carries their edit back. If the decision is already made and the work is done, the page is a record and only the check half applies.

**Visual is always default.** Essays, blog posts, and articles get visual treatment too — extract structure into cards, diagrams, grids, tables. Prose patterns (lead paragraphs, pull quotes, callout boxes) are **accent elements** within visual pages, not a separate mode — see "Prose Page Elements" in `./references/css-patterns.md`.

**Match the weight to the question.** A quick "what's happening" deserves one focused table or a single section. A small page that answers the question is a complete output. Save the multi-section treatment for content that earns it.

**Who is looking?** A developer understanding a system, a PM seeing the big picture, a team reviewing a proposal — this sets information density and visual complexity.

**What aesthetic?** Pick one and commit, then read its full recipe in `./references/aesthetics.md` before writing any CSS — the recipe's specific requirements are what block generic output.

**Constrained aesthetics (prefer these):** Blueprint (technical drawing, slate/blue, monospace labels) · Editorial (expressive serif, generous whitespace) · Paper/ink (warm cream, terracotta/sage, informal) · Monochrome terminal (green/amber on near-black) · Engraved ledger (formal document-of-record, ivory + oxblood) · Risograph zine (two spot inks, playful print) · Field guide (naturalist specimen plate, keyed figures).

**Flexible aesthetics (use with caution):** IDE-inspired (a real named scheme, committed to exactly) · Data-dense (small type, tight spacing, muted colors).

Fonts, colors, and aesthetics have hard exclusions — read `./references/anti-patterns.md` before committing a pairing, a palette, or a direction.

Vary the choice each time — and vary *structure*, not just palette. Two pages with different colors but the same label recipe and card grammar still read as siblings from the same generator. Rotate the structural grammar too: labeling voice (mono tabs / small-caps / serif italic) and composition (card grid / swimlanes / annotation rail). If the last diagram was dark and technical, make the next one light and editorial.

**Done when:** you can state, in one sentence each, the audience, the aesthetic, and the claim the reader most needs to check.

### 2. Structure

**Choose the page's structural shape first.** `./references/structures.md` holds the content→shape taxonomy — funnel, quadrant, pyramid, radial/sector, waterfall stagger, zigzag steps, binary-compare-with-center-divider, snake/roadmap. Read it and pick the shape whose logic matches the content's logic. A generic card grid is the fallback, not the default.

**Read the reference material** before generating — read it each time to absorb the patterns rather than working from memory. Templates teach *patterns*, not prose: every example name, figure, and sentence in a template is scaffolding to replace with the real subject's content. Template filler surviving into a delivered page is a defect.
- Text-heavy architecture overviews (card content matters more than topology): `./templates/architecture.html`
- Any Mermaid diagram (flowcharts, sequence, ER, state machines, mind maps, class, C4): `./references/mermaid.md` and `./templates/mermaid-flowchart.html`
- Data tables, comparisons, audits, feature matrices: `./templates/data-table.html`
- Slide decks: see Slide Deck Mode below
- Prose-heavy publishable pages (READMEs, articles, essays): "Prose Page Elements" in `./references/css-patterns.md` and "Typography by Content Voice" in `./references/libraries.md`
- Interactive tools (triage boards, config editors, tuners, curation tables, annotators): `./references/tool-patterns.md`
- CSS/layout patterns and SVG connectors: `./references/css-patterns.md`
- Pages with 4+ sections (reviews, recaps, dashboards): `./references/responsive-nav.md` for section navigation — sticky sidebar TOC on desktop, horizontal scrollable bar on mobile

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
| C4 architecture | **Mermaid** | Use `graph TD` + `subgraph` — the C4 entry in `./references/mermaid.md` has the pattern |
| Data table | HTML `<table>` | Semantic markup, accessibility, copy-paste behavior |
| Timeline | CSS (central line + cards) | Simple linear layout does not need a layout engine |
| Dashboard | CSS Grid + Chart.js | Card grid with embedded charts |
| Document corpus | HTML + client-side JS browser | Many docs need nav, search, and facet filtering — `./references/browser-patterns.md` |
| Interactive tool | HTML + client-side JS + export | Editing state must round-trip back as text — `./references/tool-patterns.md` |

**Per-type construction detail** — the architecture complexity tiers and hybrid pattern, table/timeline/dashboard specifics, implementation-plan structure, documentation transforms, prose accent elements — is in `./references/diagram-types.md`. Read the entry for the type you are building.

**Mermaid rules live in `./references/mermaid.md`** — theming, the required `diagram-shell` container pattern (copied wholesale from `./templates/mermaid-flowchart.html`), zoom/pan/export controls, export safety, the node-count ceiling, and syntax caveats. Read it before writing any Mermaid.

**AI-generated illustrations (optional).** If surf-cli is available (`which surf`), generate and embed images for hero banners and conceptual illustrations — see `./references/imagery.md` for the workflow and prompt craft. If surf is absent, skip images and continue.

**Done when:** every section of the page has a chosen shape and a chosen rendering approach, and you have read the reference file for each one in use.

### 3. Style

**Typography is the diagram.** Pick a distinctive font pairing from the tables in `./references/libraries.md`, different from recent generations. Load via `<link>` in `<head>`, with a system font fallback in the stack for offline resilience. Before choosing, write down 2–3 concrete words for the content's voice ("dense and unimpressed", "calm and careful") and pick the pairing whose voice words match.

Hierarchy needs contrast: keep at least a 1.25× size ratio between type-scale steps (fewer sizes with more contrast beats many near-identical sizes). Cap body text at ~65–75ch. On dark backgrounds, add 0.05–0.1 to your normal line-height — light-on-dark type reads lighter and needs the room.

**Spacing has a scale too.** Take every gap, margin, and pad from the two tiers in "Spatial Scale" in `./references/css-patterns.md` — the rhythm scale between elements, the half-steps inside a component — rather than inventing a near-miss value.

**Color tells a story.** Use CSS custom properties for the full palette. Define at minimum: `--bg`, `--surface`, `--border`, `--pattern`, `--text`, `--text-bright`, `--text-dim`, and 3–5 accent colors, each with a dim variant and a fill/on-fill pair. Name variables semantically (`--pipeline-step`, not `--blue-3`). Support both themes.

Good accent palettes — these are the **light-theme ink** tones, deep enough to carry 11px badge text (the tightest constraint on the page). On dark themes the ink flips bright. The fill tone stays deep in both:
- Terracotta + sage (`#c2410c`, `#4c7a0b`) — warm, earthy
- Teal + slate (`#0f766e`, `#0369a1`) — technical, precise
- Rose + cranberry (`#be123c`, `#881337`) — editorial, refined
- Amber + emerald (`#b45309`, `#15803d`) — data-focused
- Deep blue + gold (`#1e3a5f`, `#8a6508`) — premium, sophisticated

The half-step versions (`#65a30d`, `#0891b2`, `#d97706`, `#059669`, `#d4a73a`) are the reflex picks and all land at 3.1–3.7:1 on a light surface. Use them as *dark-theme* ink and as bright fills under dark text, never as light-theme text.

Prefer OKLCH (or `color-mix`) when constructing palettes — equal lightness steps actually *look* equal, unlike HSL. As colors approach white or black, reduce chroma. High chroma at extreme lightness looks garish. Tint every neutral — backgrounds, surfaces, near-black text — toward the page's accent hue (even 1–2% is perceptible and makes surfaces and accents feel like one system). On colored backgrounds, set secondary text in a shade of the background's hue rather than gray.

**The contrast contract.** This is the single source of truth for contrast on the page. The Verify step checks it and adds nothing to it.

*Every accent needs two tones.* One `--accent` cannot be both a readable text color and a background fill — that is the root of almost every unreadable page. Define each accent as a pair:

- `--accent` — the **ink** tone, for text, icons, borders. Must clear **4.5:1 against `--surface`**. Deep on light pages (`#0f766e`, not `#14b8a6`), bright on dark pages.
- `--accent-fill` — the **fill** tone, used as a background behind text. Pair it with `--accent-on-fill`, the ink that sits *on* it — near-black for light/bright fills, near-white for deep fills. Choose it by measuring, not by reflex.

Bright accents (`#50fa7b`, `#fb923c`, `#d4a73a`, `#22d3ee`) as a solid fill with white text land at **1.4–2.7:1**. Bright fill takes dark ink. Only deep, desaturated fill takes light ink.

*The floors are not negotiable.* Every text/background pair must clear:

| Text | Floor | Applies to |
|---|---|---|
| Body copy, bullets, card descriptions | **4.5:1** | Anything a reader reads in sequence |
| Labels, badges, chips, captions under 14px | **4.5:1** | Small type needs *more* contrast, not less |
| Large display type (24px+, or 19px+ bold) | **3:1** | Headings, hero numbers |
| Borders, icons, focus rings, chart strokes | **3:1** | Non-text UI that carries meaning |

`--text-dim` is for genuinely secondary information — captions, timestamps, provenance. Set bullets, descriptions, and table cells in `--text` and create hierarchy with size and weight. `--text-dim` itself must still clear 4.5:1 against every surface it lands on.

Full palette scaffolding — the token set, the ink/fill pairs, and a runnable checker — is in "The Contrast Contract" in `./references/css-patterns.md`.

**Decoration stays behind surfaces, never behind prose.** Grid lines, diagonal rules, dot fields, and hatch patterns belong to the *page* background, at an alpha low enough to read as texture rather than lines (≤0.06 in light, ≤0.05 in dark). Text sitting directly on a patterned background is a defect: put the text on an opaque `--surface` card, or drop the pattern out from behind it. Give the pattern its own `--pattern` token. `--border` alpha is tuned for a crisp 1px edge, and at 24–48px repeat spacing it reads as an aggressive ruled grid.

Put your primary aesthetic in `:root` and the alternate in the media query:

```css
/* Light-first (editorial, paper/ink, blueprint): */
:root { /* light values */ }
@media (prefers-color-scheme: dark) { :root { /* dark values */ } }

/* Dark-first (IDE-inspired, terminal): */
:root { /* dark values */ }
@media (prefers-color-scheme: light) { :root { /* light values */ } }
```

**Surfaces whisper, they do not shout.** Build depth through subtle lightness shifts (2–4% between levels), not dramatic color changes. Borders are low-opacity rgba (`rgba(255,255,255,0.08)` in dark mode, `rgba(0,0,0,0.08)` in light) — visible when you look, invisible when you do not.

**Backgrounds create atmosphere.** Give the page background a subtle gradient, a faint CSS grid pattern, or a gentle radial glow behind the focal area. The background must feel like a space, not a void.

**Visual weight signals importance.** Executive summaries and key metrics dominate the viewport on load (larger type, more padding, subtle accent-tinted background zone). Reference sections (file maps, dependency lists, decision logs) stay compact and out of the way. Use `<details>/<summary>` for sections that are useful but not primary — the collapsible pattern is in `./references/css-patterns.md`.

**Surface depth creates hierarchy.** Vary card depth to signal what matters: hero sections elevated with accent-tinted backgrounds (`hc-card--hero`), body content flat (default `.hc-card`), code blocks recessed (`hc-card--recessed`). See the depth tiers in `./references/css-patterns.md`. When everything pops, nothing does.

**Pages are static.** The page renders complete and at rest, like print — no entrance animations, no staggered reveals, no count-ups, no decorative hover. A transition appears only as feedback on a genuinely interactive control (button, row, input, `<details>`), stays under 0.2s, and moves nothing that carries layout. The forbidden motion patterns are in `./references/anti-patterns.md`.

#### Page Voice

These rules govern the **body copy and labels** on the generated page — card text, captions, callouts, table cells, tooltips, button labels. Display headlines in an expressive aesthetic are exempt. Derived from ASD-STE100 Simplified Technical English. Copy that survives one read is copy a reader can check against the thing it describes.

- **Length.** No instruction sentence over 20 words. No explanation sentence over 25. One fact per sentence — split a sentence that carries two.
- **One word per concept, page-wide.** Choose `run` or `execute` or `invoke` and use only that one everywhere. Same for show/display/render, remove/delete/drop, error/failure/fault. Rotation reads as three different things.
- **Active voice, simple tenses.** "The worker retries the job." Not "the job is retried" or "will have been retried".
- **Use can, will, must.** Readers and models both read *should*, *may*, and *might* as optional, so state the real modality: `must` for a requirement, `will` for what happens, `can` for what is possible.
- **Condition before command:** "If the build fails, read the log." In a warning, reverse it — command first, risk second: "Stop the server before you edit the config. The file can corrupt."
- **Every word carries a fact.** Delete *simply*, *robust*, *seamlessly*, *powerful*, *blazingly*, *just*, *easily*. Replace vagueness with the number or the actual behavior: "retries three times, then stops", not "gracefully handles errors". Write "renders in 40ms", not "blazingly fast".
- **Keep articles and "that".** Write "the request that failed", not "request failed" — short, not telegraphic.
- **Technical nouns stay nouns.** `webhook`, `idempotent`, `mutex` are welcome as nouns and adjectives. Keep them out of verb position ("send a webhook", not "webhook the endpoint"). Code, identifiers, flags, paths, and quoted error strings appear exactly as they are in the source, inside `<code>`.

**Done when:** the palette defines an ink/fill pair per accent, one aesthetic is committed in `:root` with the alternate in the media query, and every sentence of body copy satisfies the Page Voice specs.

### 4. Delegate

The parent agent decides what the page **says**. A subagent does the work that needs no judgment about content. If the harness supports subagents, delegate. Otherwise do the work inline.

**Delegate:** the contrast script run, the render screenshot and squint check, the overflow sweep across widths, plan-tracker checkbox flips and timestamp updates, reopening the page in the browser, deployment and sharing, and the index refresh.

**Keep:** reading the source material, choosing the structure and aesthetic, writing the HTML content, and fixing everything verification flags.

A delegated check whose report you never read is not a check — collect and read every report before Deliver.

**Done when:** every Verify check below has an owner — dispatched to a subagent or kept for yourself.

### 5. Verify

Deliver only after every check passes.

- **The contrast pass**: run `python3 ~/.claude/skills/html-craft/scripts/check-contrast.py <file.html>`. It resolves the CSS custom properties for both themes and reports every pair that misses the contrast contract in Style. It also flags hardcoded light-ink-on-accent-fill and over-intense background patterns. Fix every `FAIL`. Keep a `WARN` only with a deliberate reason. This catches what the eye does not — a 3.2:1 badge looks fine in isolation and is unreadable in context.
- **The squint test**: blur your eyes. Hierarchy still perceptible? Sections still distinct?
- **Look at the render**: when browser automation is available, open the file and screenshot it — run the squint test on the actual render, not your mental model of it.
- **Text on decoration**: scan for prose sitting directly on a striped, ruled, or dot-grid background with no surface between them. If the pattern is legible as *lines* behind a sentence, it is too strong.
- **The swap test**: would replacing your fonts and colors with a generic dark theme make this indistinguishable from a template? If yes, push the aesthetic further.
- **The slop test**: review the page against `./references/anti-patterns.md`. Two or more slop signals means regenerate with a different aesthetic direction.
- **Page voice**: every body sentence passes the Page Voice specs — under the word cap, one fact, one word per concept, no empty adjectives.
- **Checkable**: every claim about a real artifact names its source — the file:line, the command, the commit, the document. A reader who doubts a cell can find what it came from without asking you. Pages that explain a concept are exempt.
- **Steerable**: where a decision is still open, the reader has a way to act on it — options to pick between, a status to correct, an export that carries their edit back. A page that leaves them nothing to do but agree has skipped this. Where the page asks for a decision, it also meets the full "Asking the user" contract in `./references/tool-patterns.md`.
- **Both themes**: toggle your OS between light and dark. Both look intentional.
- **Information completeness**: the page conveys what the user asked for. Pretty but incomplete is a failure.
- **No overflow**: resize the browser across widths. Nothing clips or escapes its container. Every grid and flex child needs `min-width: 0`. Side-by-side panels need `overflow-wrap: break-word`. `<li>` keeps its default `display` so markers render. See Overflow Protection in `./references/css-patterns.md`.
- **Mermaid opens fully visible**: every diagram shows its *entire* graph on load, scaled down to fit. The zoom label reads `fit` (or `capped` on a small diagram). A reading above 100% on anything but a tiny diagram means the contain-fit broke in adaptation. On slides, check that nothing runs off the bottom — there is no scrolling to recover it. If a diagram is too small to read once it fits, cut nodes or split it.
- **Mermaid interaction**: on scrollable pages, every `.mermaid-wrap` carries the full engine — zoom controls, a non-clipping WebP export button, Ctrl/Cmd+scroll zoom, drag panning, and click-to-expand. Test the expanded tab and WebP output per the export-safety checklist in `./references/mermaid.md`. On slide decks, diagrams are click-to-expand only (see `./references/slide-patterns.md`).
- **No template filler**: search the page for the templates' example content — names, metrics, subject matter. Every word comes from the actual subject.
- **File opens cleanly**: no console errors, no broken font loads, no layout shifts.
- **Single self-contained file** (see File Structure): `grep -oE '(src|href)="[^"]*"' file.html` shows only `data:` URIs and `https://` URLs.

**Done when:** you ran every check above, and every check reports clean.

### 6. Deliver

**Output location:** write to `~/.agent/diagrams/` with a descriptive content-based filename: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. The directory persists across sessions.

**Stamp provenance:** end the page with a small dim footer — generation date, the git branch and short commit hash when the subject is a repository, and the key files or documents you built the page from. Explainers describe moving targets. The stamp is what makes the page auditable a week later and gives `fact-check` an anchor.

**Optional — embed fonts for offline/CSP hardening.** Only when the page must render with no network or on a strict-CSP host (for example, claude.ai Artifacts):

```bash
python3 ~/.claude/skills/html-craft/scripts/embed-fonts.py ~/.agent/diagrams/filename.html
```

It fetches the Google Fonts `<link>`s, embeds the `latin`/`latin-ext` woff2 subsets as base64 `@font-face`, and strips the external `<link>`/`preconnect` tags. Pass `--subsets latin,latin-ext,cyrillic` (or `all`) for glyphs outside those subsets (for example `№` or Greek). Mermaid and Chart.js still need the network. A fully offline page avoids them.

**Open in browser:** `open ~/.agent/diagrams/filename.html` (macOS) or `xdg-open …` (Linux).

**Tell the user the file path** so they can re-open or share it.

**Refresh the index in the background:** rebuild the launcher page per `./commands/index.md` in a background subagent, without blocking or interleaving the main task.

**Done when:** the file exists at its path, carries a provenance footer, and is open in the browser — and the path is in your reply to the user.

## Slide Deck Mode

An alternative output format: a magazine-quality slide deck instead of a scrollable page. **Opt-in only** — generate slides when the user invokes `/generate-slides`, passes `--slides` to another command (same data-gathering, same breadth of coverage, slide presentation), or explicitly asks for a deck.

**Before generating any slides**, read `./references/slide-patterns.md` — the planning process (inventory the source, map every item to slides, verify coverage: every section, decision, and data point appears in the deck), the slide engine CSS/JS, the 10 slide types, presets, imagery workflow, and compositional-variety rules all live there. Also read `./templates/slide-deck.html` (reference implementation), `./references/css-patterns.md`, and `./references/mermaid.md` if the deck contains diagrams.

## File Structure

Every page is a **single self-contained `.html` file** — one file that can be sent on its own and open correctly. The rule is about *local* assets, not the network: every generated image or asset is inlined as a `data:` URI. CDN `<link>`/`<script>` URLs (fonts, Mermaid, Chart.js, icons) are allowed — they add no sidecar files. You can also embed the fonts (Deliver step) for offline/CSP hardening.

**Degradation tiers.** CDN links are progressive enhancement: the page stays readable with every one of them blocked. Fonts fall back to the system stack (always include one). Icons vanish but their text labels remain. Mermaid failures render the diagram source via a `.catch` fallback. Charts sit beside the figures they visualize rather than replace them. **Hosting caveat:** claude.ai Artifacts and other strict-CSP hosts block all external requests, so CDN-dependent pages break there. For those targets, embed the fonts (Deliver step) and skip Mermaid/Chart.js.

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
  <!-- Optional: <script> for Mermaid or Chart.js when used -->
</body>
</html>
```

## Sharing Pages

You can deploy a page to a public Vercel URL (no account needed) via `scripts/share.sh` when a Pi-compatible `vercel-deploy` skill is installed. Usage, install paths, requirements, and caveats are in `./commands/share-page.md`. Deployments are public — anyone with the URL can view the page, so check that the content is shareable before you deploy.

