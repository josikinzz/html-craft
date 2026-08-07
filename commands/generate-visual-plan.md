---
description: Generate a visual HTML implementation plan — a living ledger of the work with a task tracker, plus state machines, code snippets, and edge cases
---
Load the html-craft skill, then generate a comprehensive visual implementation plan for `$@` as a self-contained HTML page.

The page is a **ledger** of the work, not a snapshot of an intention. It records what will be done, what is done, and what happened to everything else. The user reads it to check the work instead of trusting a summary.

Follow the html-craft skill workflow. Read the reference template, CSS patterns, and mermaid theming references before generating. Use an editorial or blueprint aesthetic, but vary fonts and palette from previous diagrams.

**Data gathering phase** — understand the context before designing. Steps 2–3 and the state/API design steps apply to code features; for a non-code plan, gather from whatever the plan's real substrate is (documents, timelines, prior decisions) instead:

1. **Parse the feature request.** Extract the core problem, the desired user-facing behavior, stated constraints, and what is explicitly out of scope.

2. **Read the relevant codebase.** Identify files needing modification, existing patterns to follow (style, architecture, naming), related functionality to integrate with, and the types, interfaces, and APIs the feature must conform to.

3. **Understand the extension points.** Look for hook points, event systems, plugin architectures, configuration flags, public APIs that may need extension, and the codebase's test patterns.

4. **Check for prior art.** Search for similar features already implemented, related issues or discussions, and code that can be reused or extended.

**Design phase** — work through the implementation before writing HTML:

1. **State design.** What new state variables are needed? What existing state is affected? Draw the state machine if behavior has multiple modes.

2. **API design.** What commands, functions, or endpoints are added? What are the signatures? What are the error cases?

3. **Integration design.** How does this feature interact with existing functionality? What hooks or events are involved?

4. **Edge cases.** Walk through unusual scenarios: concurrent operations, error conditions, boundary values, user mistakes.

5. **Task breakdown.** Split the work into tasks the user can check off. Each task gets a stable id, a one-line title, and a **completion criterion** — the observable condition that makes it done ("`parseFlags` accepts `--dry-run` and the new unit test passes"), not a label like "wire up parsing".

**Verification checkpoint** — before generating HTML, produce a structured fact sheet:
- Every state variable (new and modified) with its type and purpose
- Every function/command/API with its signature
- Every file that needs modification with the specific changes
- Every edge case with expected behavior
- Every task with its completion criterion
- Every assumption about the codebase that the plan relies on
Verify each against the code. If something cannot be verified, mark it as uncertain. This fact sheet is your source of truth during HTML generation.

Sort the uncertain items before generating. A fact you failed to verify stays marked uncertain on the page. A decision only the user can make — scope, a tradeoff, which behavior is wanted — is a **fork**: ask it now, per "Ask" in the skill's SKILL.md, because a guess baked into the plan reads as a decision.

## Page voice

The copy on the page follows the skill's page voice (full rules in SKILL.md). The essentials:

- Cap instruction sentences at about 20 words. One fact per sentence.
- Active voice, simple tenses. Prefer *can*, *will*, and *must* over *should*, *may*, and *might*.
- Condition first, command second: "When the build fails, revert the migration."
- Delete words carrying no fact — *simply*, *robust*, *seamlessly*, *just*, *powerful*.
- Reproduce code, paths, flags, and identifiers exactly.

## Diagram structure

Include a section only when the plan has real content for it; the sections below assume a code feature. A non-code plan (migration sequence, research plan, roadmap, process change) keeps the header / problem / ledger / breakdown / risks spine — header, The Problem, the task ledger, a phase-by-phase breakdown in place of the code-shaped sections, Edge Cases reframed as risks, and Implementation Notes — and drops state machines, state variables, functions, API tables, and test requirements entirely. An empty section rendered anyway is template filler.

1. **Header** — feature name, one-line description, scope summary. *Visual treatment: distinctive header with a monospace label ("Feature Plan", "Implementation Spec"), large italic title, muted subtitle. Set the tone for the page.*

2. **The Problem** — side-by-side comparison panels showing current behavior vs. desired behavior. Use concrete examples, not abstract descriptions. Show what the user experiences or what the code does, step by step. *Visual treatment: two-column grid with rose-tinted "Before" header and sage-tinted "After" header. Numbered flow steps with arrows between them.*

3. **Task ledger** — the tracker, placed directly after The Problem so it is visible on load. It carries:
   - A progress line: a count ("4 of 9 done") and a bar whose width is that fraction.
   - A **last updated** stamp, in local time, next to the count.
   - One row per task: checkbox mark, id, title, its completion criterion, and a status pill reading Todo, Doing, Done, or Blocked.
   - Blocked rows state the blocker in one sentence. Dropped rows state why they were dropped.
   - A per-task notes field, plus one page-level notes field under the ledger — a task the user disagrees with needs somewhere to say so. Both optional. See "Asking the user" in `../references/tool-patterns.md`.
   *Visual treatment: elevated depth, monospace ids, `.status` pills from css-patterns.md. Full 1px tinted borders — no left-border accent stripes, no emoji; the checkmark is an inline SVG or a styled span.*

4. **State Machine** — Mermaid flowchart or stateDiagram showing states and transitions. Label edges with the triggers (commands, events, conditions). *Wrap in `.mermaid-wrap` with zoom controls (+/−/reset/expand) and click-to-expand. Use `flowchart TD` instead of `stateDiagram-v2` if labels need colons or parentheses. Add an explanatory caption below the diagram.*

5. **State Variables** — card grid showing new state and modified existing state. Use code blocks with `white-space: pre-wrap`. *Visual treatment: two cards side-by-side, elevated depth, monospace labels.*

6. **Modified Functions** — per function: name and file path, a 10–20 line snippet showing the pattern, and what changed and why. *Visual treatment: file path as monospace dim text above the code block, code in a recessed card with accent-dim background.*

7. **Commands / API** — table of name, parameters, and behavior. Use `<code>` for technical names. *Visual treatment: bordered table with sticky header, alternating row backgrounds.*

8. **Edge Cases** — table of scenarios and expected behaviors. Cover error conditions, concurrent operations, and boundary values. *Visual treatment: same table style as Commands.*

9. **Test Requirements** — table or card grid of test categories and specific tests, grouped into unit, integration, and edge case. *Visual treatment: compact table with file references.*

10. **File References** — table mapping files to the changes needed. *Visual treatment: compact reference table; use `<details>` if many files.*

11. **Implementation Notes** — callout boxes for backward compatibility (gold border), critical warnings (rose border), and performance (amber border). *Visual treatment: callout boxes with full tinted borders and background washes (see css-patterns.md Callout Boxes), strong labels.*

## Ledger markup

Each task row carries a stable `id` and a `data-status` of `todo`, `doing`, `done`, `blocked`, or `dropped`. CSS keys off that attribute, so an update flips one attribute and the rendering follows. Ids stay fixed for the life of the page.

```html
<div class="ledger" id="ledger">
  <div class="ledger-head">
    <span class="ledger-count" id="ledger-count">4 of 9 done</span>
    <span class="ledger-stamp" id="ledger-stamp">Updated 14:32, 4 Aug 2026</span>
  </div>
  <div class="ledger-bar"><span id="ledger-fill" style="width: 44%"></span></div>

  <div class="task" id="task-3" data-status="done">
    <span class="task-mark" aria-hidden="true"></span>
    <div class="task-body">
      <p class="task-title"><span class="task-id">T3</span> Add <code>--dry-run</code> to the CLI parser</p>
      <p class="task-criterion">Done when <code>parseFlags</code> accepts <code>--dry-run</code> and <code>flags.test.ts</code> passes.</p>
    </div>
    <span class="status status--match">Done</span>
  </div>
</div>
```

```css
.ledger-bar { height: 6px; border-radius: 3px; background: var(--border); overflow: hidden; }
.ledger-bar span { display: block; height: 100%; background: var(--accent); transition: width .3s ease; }
.ledger-stamp { font-family: var(--font-mono); font-size: 11px; color: var(--text-dim); }

.task {
  display: grid; grid-template-columns: 20px 1fr auto; gap: 12px; align-items: start;
  padding: 12px 14px; border: 1px solid var(--border); border-radius: 8px;
  background: var(--surface); min-width: 0;
}
.task + .task { margin-top: 8px; }
.task-body { min-width: 0; overflow-wrap: break-word; }
.task-id { font-family: var(--font-mono); font-size: 11px; color: var(--text-dim); margin-right: 8px; }
.task-criterion { font-size: 12px; color: var(--text-dim); margin: 4px 0 0; }

/* The mark is a styled span — a drawn checkbox, never an emoji. */
.task-mark {
  width: 16px; height: 16px; margin-top: 2px; border-radius: 4px;
  border: 1px solid var(--border-bright); display: block; position: relative;
}

.task[data-status="done"] { background: color-mix(in srgb, var(--green, #15803d) 6%, var(--surface)); }
.task[data-status="done"] .task-mark { background: var(--green, #15803d); border-color: var(--green, #15803d); }
/* SVG-shaped tick: two borders rotated into a checkmark. */
.task[data-status="done"] .task-mark::after {
  content: ""; position: absolute; left: 5px; top: 1px; width: 4px; height: 9px;
  border: solid var(--surface); border-width: 0 2px 2px 0; transform: rotate(45deg);
}
.task[data-status="done"] .task-title { color: var(--text-dim); }

.task[data-status="doing"] { border-color: color-mix(in srgb, var(--accent) 45%, var(--border)); }
.task[data-status="doing"] .task-mark { border-color: var(--accent); background: var(--accent-dim); }

.task[data-status="blocked"] { background: color-mix(in srgb, var(--red, #b91c1c) 6%, var(--surface)); }
.task[data-status="blocked"] .task-mark { border-color: var(--red, #b91c1c); }

.task[data-status="dropped"] { opacity: .65; }
.task[data-status="dropped"] .task-title { text-decoration: line-through; }
```

Pair each status with its `.status` pill: `--match` for Done, `--info` for Doing, `--warn` for Blocked, `--gap` for Dropped, plain for Todo.

## The update contract

This contract binds while the plan is being executed. A plan generated purely for discussion carries the ledger but needs no updates.

While a plan page exists for the current work, **the page reflects the true state of the work**. On every task transition:

1. Flip that row's `data-status` to `done`, `doing`, `blocked`, or `dropped`, and swap its `.status` pill text and class.
2. Update `#ledger-count` and the `width` on `#ledger-fill`.
3. Update `#ledger-stamp` to the current local time.
4. Reopen the page in the user's browser — `open <path>` on macOS, `xdg-open <path>` on Linux. The reopen is the point: it puts the real state in front of the user so they can check it.

Blocked tasks get `data-status="blocked"` and a one-sentence blocker. A dropped task gets `data-status="dropped"` and the reason it was dropped — the ledger records what happened, so dropped rows stay on the page.

Make each update a small targeted edit to the existing file. The stable ids make every edit unambiguous; regenerating the page throws away the history the ledger exists to hold.

**Completion criterion:** the turn ends with the plan page showing the same state as the work. Read the page's current `data-status` values before you finish, and reconcile any that differ.

**Delegate the maintenance.** Tracker upkeep is mechanical and needs no judgment about content. When the harness offers subagents, hand each update to one: give it the file path, the task ids and their new statuses, the new count, and the instruction to update the stamp and reopen the page. The parent agent stays on the actual work. Without subagents, do the update inline. Any model can run this — pick whatever the harness makes available.

## Rendering rules

**Visual hierarchy:**
- Sections 1–4 dominate the viewport on load (hero depth for header, elevated for the problem comparison, the ledger, and the state machine)
- Sections 5–7 are core implementation detail (elevated cards, readable code blocks)
- Sections 8–11 are reference material (flat or recessed depth, compact layout)

**Typography and color:** pick a distinctive font pairing (not Inter/Roboto). Use semantic accents — gold for primary, sage for "after"/success, rose for "before"/warning. Both light and dark themes must work.

**Code blocks:** always `white-space: pre-wrap` and `word-break: break-word`. Include file path headers where relevant. Keep snippets focused on the pattern rather than the full implementation.

**Overflow prevention:** `min-width: 0` on all grid/flex children, `overflow-wrap: break-word` on text containers, absolute positioning for list markers, and tables checked against wide content.

**Optional hero image** — if `surf` CLI is available (`which surf`), consider a conceptual illustration that captures the feature's essence. Use it for abstract concepts that benefit from visual metaphor; skip it for purely structural changes. Embed as a base64 data URI using the `.hero-img-wrap` pattern from css-patterns.md.

Write to `~/.agent/diagrams/` with a descriptive filename (e.g., `feature-name-plan.html`). Open the result in the browser. Tell the user the file path, and keep that path for the update contract.

Ultrathink.
