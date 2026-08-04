---
description: Generate a throwaway single-file HTML tool — triage board, config editor, live tuner, curation table, or annotator — that round-trips its result back as text
---
Load the visual-explainer skill, then build a purpose-built interactive tool as a single self-contained HTML page for the data and job the user points at.

Follow the visual-explainer skill workflow. Read `../references/tool-patterns.md` before making any structural choice, plus `../references/css-patterns.md` (especially "Interactive Controls") and the skill's Style and Anti-Patterns sections. Follow the impeccable skill's frontend craft (accessibility, responsiveness, deliberate component quality) within this skill's aesthetic constraints.

**Ingestion** — `$1` names the data (a file, a Linear/GitHub query, a config, a transcript) and the job (reorder, edit, tune, curate, annotate, pick); ask only if neither is identifiable from arguments or conversation:

1. **Read the actual data in full** — the tool embeds it, and its constraints come from it. Note the item count; it becomes the census anchor.
2. **Pick the tool type** from the catalog in tool-patterns.md and **decide the export format first** — what text the user will paste back, and where it goes. State both to the user in one short line before building.
3. **Form your best guess** — the proposed ordering, the recommended values, the pre-set verdicts. The tool opens showing it.

**Privacy pass** — run the credential/PII scan (see tool-patterns.md → browser-patterns.md) before embedding; report any redactions in chat.

**Build** — the chosen tool shape with the skill's full aesthetic treatment: fresh font pairing and palette, both themes, no slop patterns. State as one JS object rendered to DOM, export serializing state, pre-filled with the best guess, constraints enforced inline, change counter and unexported-changes guard wired.

**Verify** — the skill's global Verify checklist plus every tool-specific check in tool-patterns.md. The round-trip check is the completion criterion: one edit of each kind performed, exported text reflects all of them and fully reconstructs the final state.

Write to `~/.agent/diagrams/` with a descriptive job-based filename (e.g. `ticket-triage-board.html`), open in the browser, and tell the user the path — and that the result comes back by pasting the export.

$@
