---
description: Generate an exploration grid — several distinctly different approaches to one problem, side by side, each labeled with the tradeoff it makes
---
Load the html-craft skill, then build an exploration grid as a single self-contained HTML page: multiple genuinely different answers to one design or implementation question, laid out for side-by-side comparison so the user can pick one.

Follow the html-craft skill workflow. Read `../references/css-patterns.md`, the skill's Style step, and `../references/anti-patterns.md` before generating.

**Framing** — `$1` is the problem to explore (an onboarding screen, an API shape, a caching strategy, a page layout); ask only if no problem is identifiable from arguments or conversation. Read whatever real context exists — the current code, the current design, prior plans — so every option is grounded in the actual constraints, then decide the option count from the problem's real spread (4–6 is the usual range; state it in one line before building).

**The options must differ structurally, not cosmetically.** Vary the axes that matter for this problem — layout, tone, density, data flow, dependency choice, failure behavior — such that no two options could be described as the same approach with different styling. Before building, write one sentence per option naming what it bets on; if two sentences match, replace one option.

**Each option's panel carries:**

1. A short name and number the user can pick it by
2. The rendering that shows the approach — a live mockup for UI options (each visually committed to its own direction), a diagram or annotated snippet for code/architecture options
3. **The tradeoff it makes** — one labeled line stating what this option buys and what it gives up. An option without a stated cost is advertising, not exploration.
4. **A notes field** the user can type into about this option ("option 2, but not the caching part").

Exactly one option carries a **Recommended** marker with a one-line reason for it. The grid also carries a page-level notes field and an explicit escape from the framing — a "none of these" panel with a text field — so the user can say the question is wrong instead of picking the least-wrong option. Every field stays optional. Full contract: "Asking the user" in `../references/tool-patterns.md`; copy the markup, styling, and export bar from "Question Blocks (Asking the User)" in `../references/css-patterns.md`.

**The choice round-trips.** Each panel carries a radio in one named group, so picking costs one click. A **Copy selection** button under the grid exports the state as a markdown block: the chosen option, every per-option note, the page notes, and the escape text if it was used. The block names the provenance of the pick — confirmed when the user clicked the recommended option, overridden when they picked another, untouched when they clicked nothing. An untouched grid exports as *unanswered*, never as agreement with the recommendation. Confirming fires no `change` event, so capture the click; see the wiring note in the Question Blocks recipe. The button works with every field blank.

Picking by number in chat stays the lightweight path — one word beats a round trip when the user has nothing to add. The export is for the answer that carries notes with it.

The page itself uses one coherent aesthetic (fresh font pairing and palette, both themes, no slop patterns) as neutral chrome around the panels — for UI explorations, the variation belongs inside the mockups, not in the page frame.

**Verify** — the skill's global Verify checklist, plus: every option has a distinct structural bet and a stated tradeoff, and the grid supports direct comparison at a glance (equal panel prominence — the page recommends by argument, not by visual weight). Then run the round trip: type one per-option note, click the recommended option, export, and confirm the block names the pick as confirmed and carries the note. Export again with nothing touched and confirm it reads unanswered.

Write to `~/.agent/diagrams/` with a descriptive filename (e.g. `onboarding-explorations.html`), open in the browser, and tell the user the path. Invite them to pick an option by number in chat, or to hit **Copy selection** and paste the block back when they have notes to send with it. Either way the natural next step is expanding the winner with `/html-craft:generate-visual-plan`, keeping this page as reference context for the implementing session.

$@
