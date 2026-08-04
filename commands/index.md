---
description: Build or refresh the launcher index for ~/.agent/diagrams — one homepage listing every generated page, grouped by repo and date, with staleness flags
---
Build (or rebuild from scratch — it is a derived artifact, never hand-maintained) the launcher page at `~/.agent/diagrams/index.html`.

**Run in the background by default.** When invoked as part of delivering another page, or when any other work is in flight, do this via a background subagent (Agent tool, `run_in_background: true`) so it never blocks or interleaves with the main task. Index maintenance is mechanical extraction and templating, so give it the smallest tier the harness offers. Only run it inline when the user invoked `/html-craft:index` directly and nothing else is going on. The subagent prompt is simply: "Follow ~/.claude/skills/html-craft/commands/index.md to rebuild the diagrams index."

**Gather** — for every `*.html` in `~/.agent/diagrams/` except `index.html` itself:

- **Title** from the `<title>` tag; fall back to the filename.
- **Kind** — infer from content (browser, plan, review, recap, slides, diagram, table) for a small type badge.
- **Repo and commit** from the provenance footer when present (pages stamp branch/commit and source files at generation time); no stamp → group under the "unfiled" section.
- **Dates**: file mtime is the freshness signal; the provenance date is shown when present.

Extract with grep/sed over each file — do not read 500 KB pages fully into context; only the `<title>` line and the footer region are needed.

**Build** — a single lightweight self-contained page (this is a launcher, not a report — one screen of ceremony, fast to scan):

1. **Grouping**: primary sections by repo (from provenance), "unfiled" last; within each section, newest first. A date heading or date column keeps the timeline visible.
2. **Each entry**: title as a `file://` link, kind badge, provenance date, and a staleness flag — fresh (≤7 days), aging (8–30), stale (>30) — conveyed by label + shape, not color alone.
3. **Header**: total page count and the index's own build timestamp.
4. A search-as-you-filter input once the list passes ~15 entries; below that, skip it.
5. Aesthetic: follow the skill's Style rules but keep it compact and quiet — the index should feel like a shelf, not a poster. Both themes, no slop patterns, distinctive but restrained type.

**Completion criterion**: every `.html` file in the folder except `index.html` appears exactly once — entry count in the header equals the file count on disk.

Overwrite `~/.agent/diagrams/index.html` in place (stable bookmark URL). When invoked directly by the user, open it in the browser and report the count; when run as a background refresh, stay silent — no browser open, no chat summary beyond the subagent's completion.
