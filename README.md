# HTML Craft

An agent skill that writes self-contained HTML pages — one file, no sidecar assets — and opens them in your browser.

The organizing idea is that a page is a working surface, not a report. It keeps you in the loop on your own work, two ways:

- **Check.** The page leads with the conclusion and attaches what it rests on — `parser.py:88` rather than "the parser", the number rather than "significantly faster", the checklist in its real state rather than "mostly done". You take the answer and verify it only if you want to. Every page ends with a provenance footer naming the files, branch, and commit it was built from.
- **Steer.** Where a decision is still open, the page gives you a handle on it — options side by side, a task status you can correct, an export that carries your edits back into the conversation as text. A page that arrives after the work is done can only be audited; the same page at a decision point changes what happens next.

See [`SKILL.md`](./SKILL.md) for the full behavior.

## Lineage

This is a personal fork, tuned to one person's workflow. It is a mishmash of several skills and ideas, and it has diverged a long way from where it started. Credit where it belongs:

- **[nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer)** by [Nico Bailon](https://github.com/nicobailon) — the original, and most of the foundation here. MIT. This fork renames it to `html-craft`.
- **[AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish)** — packages ASD-STE100 Simplified Technical English, the aerospace controlled language. The Page Voice rules that govern copy on generated pages are distilled from it. Jargon stays; empty adjectives go.
- **[antvis/infographic](https://github.com/antvis/infographic)** — the source of the structure/item/theme taxonomy and the layout shapes (funnel, quadrant, pyramid, radial, waterfall stagger, zigzag steps, binary compare, snake path). The ideas only, none of the code — this skill hand-writes plain CSS.

The fork also restructured `SKILL.md` against the writing-great-skills principles: information hierarchy, progressive disclosure into `references/`, checkable completion criteria per step, pruned no-ops, leading words. It went from 490 lines to about 290, with the anti-patterns and per-diagram-type detail moved into reference files.

New in this fork: the plan task ledger, and a delegation rule that hands verification, tracker maintenance, and deployment to subagents while the parent agent keeps the judgment calls.

## The task ledger

`/generate-visual-plan` produces a plan page that stays true as the work proceeds. Each task row carries a stable id, a one-line title, a completion criterion, and a `data-status` of `todo`, `doing`, `done`, `blocked`, or `dropped`.

While the plan is being executed, the agent must reconcile the page with reality on every task transition: flip the row's status, update the count and the progress bar, restamp the local time, and reopen the page in your browser. The reopen is the point — it puts the real state in front of you. Dropped rows stay on the page with the reason they were dropped, so the ledger records what happened rather than what was intended.

## Commands

Prompt templates in `commands/`, invoked as slash commands namespaced by harness (`/html-craft:diff-review` in Claude Code, `/diff-review` in Pi).

| Command | What it does |
|---|---|
| `generate-web-diagram` | Generate an HTML diagram for any topic |
| `generate-visual-plan` | Generate a visual implementation plan with the task ledger |
| `generate-slides` | Generate a magazine-quality slide deck |
| `diff-review` | Visual diff review with architecture comparison and code review |
| `plan-review` | Compare a plan against the codebase with risk assessment |
| `project-recap` | Mental model snapshot for context-switching back to a project |
| `browse-docs` | Document browser for a corpus of docs with nav, search, and facets |
| `make-tool` | Throwaway single-file editor with a round-trip text export |
| `explore-options` | Exploration grid — different approaches side by side, each with its tradeoff |
| `index` | Build or refresh the launcher index for `~/.agent/diagrams` |
| `fact-check` | Verify a document against the actual code |
| `share-page` | Deploy an HTML page to Vercel and get a live URL |

The skill also fires on its own when a page beats terminal output — including when the agent is about to print a wide ASCII table.

## Layout

- `SKILL.md` — the workflow: think, structure, style, delegate, verify, deliver.
- `references/` — loaded on demand, one file per topic: `structures.md` (content→shape taxonomy and layout recipes), `css-patterns.md` (tokens, the contrast contract, connectors, overflow), `anti-patterns.md`, `mermaid.md`, `diagram-types.md`, `slide-patterns.md`, `tool-patterns.md`, `browser-patterns.md`, `libraries.md`, `imagery.md`, `responsive-nav.md`.
- `templates/` — four reference implementations to copy patterns from: `architecture.html`, `data-table.html`, `mermaid-flowchart.html`, `slide-deck.html`.
- `scripts/` — `check-contrast.py` (resolves CSS custom properties in both themes and reports every pair that misses the floors), `embed-fonts.py`, `share.sh`.

## Install

```sh
git clone https://github.com/josikinzz/html-craft.git ~/.agents/skills/html-craft
```

It works from any agent-skill directory — `~/.claude/skills/html-craft` also works. My own setup clones once at `~/.agents/skills/html-craft` and symlinks `~/.claude/skills/html-craft` at it.

## Requirements

- A browser, to view the generated files.
- `python3`, for the contrast checker and the font embedder.
- Optional: `surf-cli`, for AI-generated hero images. Without it, the skill skips images and continues.

## License

MIT — see [`LICENSE`](./LICENSE). Created by [Nico Bailon](https://github.com/nicobailon); the upstream project is [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer).
