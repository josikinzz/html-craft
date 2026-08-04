# Interactive Tool Patterns

Reference for building a **throwaway tool** — a single self-contained HTML file, purpose-built for one piece of data and one job: reordering these tickets, editing this config, tuning this animation, annotating this transcript. Not a product, not a reusable app. The user manipulates it in the browser, then the result **round-trips** back into the agent loop as text. All the skill's global rules apply (aesthetics, anti-patterns, verify checklist, single-file delivery); this file adds only what's tool-specific.

## Round-trip is the contract

A tool is finished when its state can leave as text. Every tool ends with one or more export buttons — "copy as JSON", "copy as Markdown", "copy as prompt", "copy diff" — whose output the user pastes back into the agent conversation or commits to a file. The export defines the tool: decide what the exported text looks like *first*, then build the interface that produces it. A beautiful board whose final ordering can't leave the page has failed at its one job.

Export format follows destination:

- **Back into the agent** → Markdown or a prompt-shaped block, with a one-line rationale per decision where the user made judgment calls
- **Into a file/commit** → the file's own format (JSON, YAML, CSS custom properties), complete and valid
- **Config edits** → a diff of changed keys only, not a full re-dump

The export carries the **notes** and the **answered / unanswered / overridden** state alongside the structured values (see "Asking the user"). Structured values alone export the agent's own proposal back at it.

## Asking the user

This section binds **any page that asks the user to approve, pick, rank, or sign off** — an exploration grid, a plan ledger, a review, a curation table, not only tools. The risk it removes: when the only inputs are the agent's predefined options, the user can pick among the agent's ideas and nothing else. Free text is the one channel that can say *the question itself is wrong*.

**Free text at two scopes, always present, never required.**

- A **page-level notes** field, once per page — this catches "you framed this wrong".
- A **per-item note** on the repeating unit, whatever it is: each option in an exploration grid, each row in a curation table, each task in a plan ledger — this catches "option 2, but not the caching part".

**Nothing blocks the export.** No required fields, no validation gate on the way out. The export button works with every field blank. A page that can refuse to let the user leave is a form, not a working surface.

**Structured choices are accelerants, not gates.** Offer radios, chips, and rankings for the reason they work: one click is cheaper than a paragraph, so the user answers instead of skipping. Every question can be left unanswered, and every choice set carries an explicit escape — a "none of these" / "other" option with an inline text field — so the user can reject the framing instead of picking the least-wrong answer.

**Every open question carries a recommendation with its reason.** Where a question has no predetermined answer, commit to one — a page that dumps N options and makes the user do all the thinking is its own failure. Mark it visibly as the agent's recommendation and give it a one-line reason. The reason is the point: a bare recommendation invites a rubber stamp, a reasoned one can be argued with.

**Blank is not agreement.** This rule is what makes the recommendation safe. Implement it as **provenance per field**: every answerable field holds a value *and* a source, `agent` or `user`. Any interaction with the field flips its source to `user`. The export then tells three states apart honestly — confirmed, overridden, never touched — and exports an untouched question as explicitly unanswered instead of dropping it, so the agent reads "no input given" rather than treating silence as consent.

A field whose source is still `agent` was never touched, whatever value sits in it. That case reads as *not confirmed* — never as agreement. Confirming is an action: the user clicks the already-selected option, which flips the source like any other interaction.

```js
// State is one object (see Mechanics); provenance is two extra keys per field.
state.answers = {
  cacheLayer: { value: "redis", source: "agent", reason: "Already in the stack." },
  retries:    { value: 3,       source: "user",  reason: "Agent recommended 3." },
  rolloutPct: { value: 10,      source: "user",  reason: "Agent recommended 50." },
  authFlow:   { value: null,    source: "agent", reason: "No default fits." }
};
state.notes = { page: "", byItem: { opt1: "", opt2: "" } };
```

```markdown
- Cache layer: **redis** — agent recommendation, NOT confirmed (untouched)
- Retries: **3** — confirmed by the user (matches the recommendation)
- Rollout %: **10** — set by the user (agent recommended 50)
- Auth flow: **unanswered** — no recommendation offered, no input given
- Notes on option 2: "yes, but not the caching part"
- Page notes: (none)
```

Read the first line back as the agent: it says the value is yours, not theirs, and still needs a decision. That is the whole point of the rule.

Style the recommendation marker and the notes fields on the existing token contract — an inline `.status`-style pill in `--accent` on `--accent-dim` for "Recommended", `--text-dim` for the one-line reason, `1px solid var(--border)` on the `<textarea>`. Full tinted borders, no left accent stripes, no emoji.

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
- **Pre-fill with your best guess, and record that it was yours.** The tool opens showing the agent's proposed answer — tickets pre-sorted, flags pre-set, sliders at recommended values — so the user corrects rather than starts from zero. An empty tool wastes the agent's judgment. Every pre-filled field opens at `source: "agent"` (see "Asking the user"); the provenance is what keeps an untouched pre-fill from exporting as the user's endorsement. The two rules are one system: pre-fill supplies the starting point, provenance keeps the export honest about who chose it.
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
- **Empty export**: export with no input at all. The exported text states that nothing was answered, and names the agent's values as the agent's. This check fails often, because the tool opens pre-filled — the untouched defaults leave as if the user had picked them.
- **Free text**: the page-level notes field and one per-item note both reach the export, and the export button works with every field blank.
- **Constraint firing**: each encoded rule triggers its warning when deliberately violated.
- **Unexported-changes guard**: change counter increments on edit; `beforeunload` warns before, and not after, export.
- **Keyboard path**: the primary interaction is completable without a pointer.
- **Degenerate data**: zero-item and one-item inputs render a usable page, not a broken layout.
