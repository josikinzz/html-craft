# HTML Craft

HTML Craft is an agent skill. It writes self-contained HTML pages and opens them in your browser. Each page is one file that holds its own styles, data, and scripts.

A page is a working surface, not a report. It keeps you in the loop on your own work in two ways.

## Check

The page states the conclusion first. Then it attaches the evidence for that conclusion.

- It names `parser.py:88` instead of "the parser".
- It gives the number instead of "significantly faster".
- It shows the real checklist state instead of "mostly done".

You read the answer. You check it only if you want to. Every page ends with a provenance footer that names the source files, the branch, and the commit.

## Steer

The page gives you a handle on each open decision:

- Options side by side, with one marked as the recommendation.
- A task status that you can correct.
- An export that returns your edits to the conversation as text.

Timing controls the value of this. A page that arrives after the work can only be checked. The same page at a decision point changes the result.

Any page that asks you to approve or pick must let you reject the framing. Free-text notes are always present. Every choice set carries an escape. An untouched field exports as unanswered, never as agreement.

## Lineage

This repository is a personal fork, tuned to one person's workflow. It is a mishmash of several skills and ideas, and it diverged far from its origin. Credit belongs to the sources below.

- **[nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer)** by [Nico Bailon](https://github.com/nicobailon) — the original, and most of the foundation here. MIT. This fork renamed it to `html-craft`.
- **[AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish)** — packages ASD-STE100 Simplified Technical English, the aerospace controlled language. The Page Voice rules come from it. Jargon stays. Empty adjectives go.
- **[antvis/infographic](https://github.com/antvis/infographic)** — the source of the structure, item, and theme taxonomy, and of the layout shapes. This fork took the ideas only. It writes plain CSS by hand.

This fork also restructured `SKILL.md` against the writing-great-skills principles: information hierarchy, progressive disclosure into `references/`, one checkable criterion per step, and pruned no-ops. The file went from 490 lines to 298 lines.

Two behaviors are new in this fork. The first is the plan task ledger. The second is a delegation rule that hands the checks, ledger maintenance, and deployment to subagents, and keeps the judgment calls with the parent agent.

## The task ledger

The `generate-visual-plan` command writes a plan page that stays true during the work. Each task row carries a stable id, a title, a completion criterion, and a status. The status is `todo`, `doing`, `done`, `blocked`, or `dropped`.

While the plan runs, the agent must reconcile the page with reality at every task transition:

1. Flip the status of the row.
2. Update the count and the progress bar.
3. Restamp the time.
4. Reopen the page in your browser.

The reopen is the point. It puts the real state in front of you. Dropped rows stay on the page with the reason for the drop. The ledger records what happened, not what someone intended.

## Commands

The `commands/` directory holds the prompt templates. Each harness namespaces them as slash commands. Claude Code uses `/html-craft:diff-review`. Pi uses `/diff-review`.

| Command | What it does |
|---|---|
| `generate-web-diagram` | Generate an HTML diagram for any topic |
| `generate-visual-plan` | Generate an implementation plan with the task ledger |
| `generate-slides` | Generate a magazine-quality slide deck |
| `diff-review` | Visual diff review with architecture comparison and code review |
| `plan-review` | Compare a plan against the codebase with risk assessment |
| `project-recap` | Mental model snapshot for a return to an old project |
| `browse-docs` | Document browser with nav, search, and facets |
| `make-tool` | Throwaway single-file editor with a round-trip text export |
| `explore-options` | Exploration grid of different approaches, each with its tradeoff |
| `index` | Build or refresh the launcher index for `~/.agent/diagrams` |
| `fact-check` | Check a document against the actual code |
| `share-page` | Deploy a page to Vercel and return a live URL |

The skill also fires on its own when a page beats terminal output. One trigger is a wide ASCII table.

## Layout

- `SKILL.md` — the workflow: think, structure, style, delegate, verify, deliver.
- `references/` — one file per topic, loaded on demand. `structures.md` holds the content-to-shape taxonomy and the layout recipes. `css-patterns.md` holds the tokens, the contrast contract, the connectors, and the overflow rules. `tool-patterns.md` holds the round-trip contract and the rules for a page that asks you a question. The others are `anti-patterns.md`, `diagram-types.md`, `mermaid.md`, `slide-patterns.md`, `browser-patterns.md`, `libraries.md`, `imagery.md`, and `responsive-nav.md`.
- `templates/` — four reference implementations: `architecture.html`, `data-table.html`, `mermaid-flowchart.html`, and `slide-deck.html`.
- `scripts/` — `check-contrast.py` resolves the CSS custom properties in both themes and reports every pair that misses the contrast floor. `embed-fonts.py` inlines the fonts. `share.sh` deploys a page.

## Install

Clone this repository into your agent skills directory:

```sh
git clone https://github.com/josikinzz/html-craft.git ~/.agents/skills/html-craft
```

The skill runs from any agent skills directory, such as `~/.claude/skills/html-craft`. To serve two harnesses from one copy, clone the repository once and create a symlink to it.

## Requirements

- A browser, to view the generated files.
- `python3`, for the contrast checker and the font embedder.
- `surf-cli` is optional. It generates hero images. Without it, the skill skips the images and continues.

## License

MIT. See [`LICENSE`](./LICENSE). Nico Bailon created the original. The upstream project is [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer).
