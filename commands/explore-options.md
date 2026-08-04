---
description: Generate an exploration grid — several distinctly different approaches to one problem, side by side, each labeled with the tradeoff it makes
---
Load the visual-explainer skill, then build an exploration grid as a single self-contained HTML page: multiple genuinely different answers to one design or implementation question, laid out for side-by-side comparison so the user can pick one.

Follow the visual-explainer skill workflow. Read `../references/css-patterns.md` and the skill's Style and Anti-Patterns sections before generating.

**Framing** — `$1` is the problem to explore (an onboarding screen, an API shape, a caching strategy, a page layout); ask only if no problem is identifiable from arguments or conversation. Read whatever real context exists — the current code, the current design, prior plans — so every option is grounded in the actual constraints, then decide the option count from the problem's real spread (4–6 is the usual range; state it in one line before building).

**The options must differ structurally, not cosmetically.** Vary the axes that matter for this problem — layout, tone, density, data flow, dependency choice, failure behavior — such that no two options could be described as the same approach with different styling. Before building, write one sentence per option naming what it bets on; if two sentences match, replace one option.

**Each option's panel carries:**

1. A short name and number the user can pick it by
2. The rendering that shows the approach — a live mockup for UI options (each visually committed to its own direction), a diagram or annotated snippet for code/architecture options
3. **The tradeoff it makes** — one labeled line stating what this option buys and what it gives up. An option without a stated cost is advertising, not exploration.

The page itself uses one coherent aesthetic (fresh font pairing and palette, both themes, no slop patterns) as neutral chrome around the panels — for UI explorations, the variation belongs inside the mockups, not in the page frame.

**Verify** — the skill's global Verify checklist, plus: every option has a distinct structural bet and a stated tradeoff, and the grid supports direct comparison at a glance (equal panel prominence — the page recommends by argument, not by visual weight).

Write to `~/.agent/diagrams/` with a descriptive filename (e.g. `onboarding-explorations.html`), open in the browser, and tell the user the path. Invite them to pick an option by number — the natural next step is expanding the winner with `/visual-explainer:generate-visual-plan`, keeping this page as reference context for the implementing session.

$@
