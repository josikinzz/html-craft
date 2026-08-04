# Interactive Tool Patterns

Reference for building a **throwaway tool** — a single self-contained HTML file, purpose-built for one piece of data and one job: reordering these tickets, editing this config, tuning this animation, annotating this transcript. Not a product, not a reusable app. The user manipulates it in the browser, then the result **round-trips** back into the agent loop as text. All the skill's global rules apply (aesthetics, anti-patterns, verify checklist, single-file delivery); this file adds only what's tool-specific.

## Round-trip is the contract

A tool is finished when its state can leave as text. Every tool ends with one or more export buttons — "copy as JSON", "copy as Markdown", "copy as prompt", "copy diff" — whose output the user pastes back into the agent conversation or commits to a file. The export defines the tool: decide what the exported text looks like *first*, then build the interface that produces it. A beautiful board whose final ordering can't leave the page has failed at its one job.

Export format follows destination:

- **Back into the agent** → Markdown or a prompt-shaped block, with a one-line rationale per decision where the user made judgment calls
- **Into a file/commit** → the file's own format (JSON, YAML, CSS custom properties), complete and valid
- **Config edits** → a diff of changed keys only, not a full re-dump

## Tool types

Pick the shape from the job. Hybrids are fine; commit to one primary interaction.

| Tool | Job | Primary interaction | Export |
|---|---|---|---|
| **Bucket board** | Reorder, triage, prioritize (tickets, test cases, feedback) | Draggable cards across labeled columns | Markdown ordering with per-bucket rationale |
| **Config editor** | Edit structured config with constraints (flags, env, JSON/YAML) | Form grouped by area; dependency warnings inline | Diff of changed keys |
| **Live-preview tuner** | Tune prompts, templates, copy | Editable source pane + sample inputs re-rendering live; char/token counter | Final text |
| **Parameter sandbox** | Dial in animation, easing, layout, algorithm values | Sliders/knobs driving a live demo | The winning parameter set (CSS/JSON) |
| **Curation table** | Approve/reject/tag rows (datasets, examples, findings) | Per-row verdict controls + bulk actions | The selection, with verdicts |
| **Annotator** | Mark up a document, transcript, or diff | Select a span → attach note/tag | Annotations with stable anchors (line/offset/quote) |
| **Value picker** | Values painful to type: colors, easing curves, crop regions, cron schedules, regexes | Direct-manipulation control with a live text readout | The value, in its usable syntax |

## Mechanics

- **Control styling** — buttons, focus rings, inputs, sliders, toggles, drag states, validation — is in "Interactive Controls" in `css-patterns.md`, on the same token contract as the rest of the page. The export button is the page's one primary button.
- **Pre-fill with your best guess.** The tool opens showing the agent's proposed answer — tickets pre-sorted, flags pre-set, sliders at recommended values — so the user corrects rather than starts from zero. An empty tool wastes the agent's judgment.
- **Embed source data** in a single `<script type="application/json">` block, parsed at load. No fetch, no sidecar files.
- **State is one JS object; the DOM renders from it.** Every interaction mutates state, then re-renders. Export serializes state directly — never scrape the DOM to find out what the user did.
- **Export mechanics**: `navigator.clipboard.writeText` with a hidden-textarea fallback (clipboard API needs a secure context; `file://` counts, but keep the fallback). Flash a visible confirmation on the button ("Copied ✓", ~1.5s). Offer a second format only when both destinations are real.
- **Unexported changes are fragile** — state lives only in the open page. Show a change count against the initial state ("4 changes"), and register a `beforeunload` guard while unexported changes exist; clear it after export.
- **Drag-and-drop** needs a keyboard path: select a card, arrow keys move it between/within columns. Pointer-events-based dragging is more reliable than HTML5 native DnD across browsers.
- **Escape everything** interpolated from data into HTML (`&<>"`), or build via `createElement`/`textContent`. Ticket titles and config values are untrusted strings.
- **Constraints live in the tool.** If a flag needs a prerequisite, warn when it's violated; if a regex field must compile, validate on input. The point of a purpose-built editor is that it knows the rules of this one dataset.
- **Privacy pass**: config, env, and ticket data attract secrets. Before embedding, run the credential/PII scan from `browser-patterns.md` ("Privacy pass") and report redactions the same way.

## Tool-specific verify checks

Run these in addition to the skill's global Verify checklist:

- **Census**: every item in the source data appears in the tool — count them.
- **Round-trip**: perform one edit of each supported kind, export, and confirm the exported text reflects every edit and fully reconstructs the final state. This is the completion criterion for any tool.
- **Pre-fill**: the tool opens populated with the best-guess state, not blank.
- **Constraint firing**: each encoded rule triggers its warning when deliberately violated.
- **Unexported-changes guard**: change counter increments on edit; `beforeunload` warns before, and not after, export.
- **Keyboard path**: the primary interaction is completable without a pointer.
- **Degenerate data**: zero-item and one-item inputs render a usable page, not a broken layout.
