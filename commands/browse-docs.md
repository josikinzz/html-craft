---
description: Generate a self-contained HTML document browser — peruse a collection of docs/reports with navigation, search, and facet filtering
---
Load the html-craft skill, then build a document browser as a single self-contained HTML page for the corpus the user points at.

Follow the html-craft skill workflow. Read `../references/browser-patterns.md` before making any structural choice, plus `../references/css-patterns.md`, the skill's Style step, and `../references/anti-patterns.md`. Follow the impeccable skill's frontend craft (accessibility, responsiveness, deliberate component quality) within this skill's aesthetic constraints.

**Corpus ingestion** — `$1` is a folder, glob, or description of the documents; ask only if no corpus is identifiable from arguments or conversation:

1. **Read every document.** List the corpus and read each document in full — sampling is not ingestion. Note the count; it becomes the census anchor.
2. **Extract the shared schema.** For each document, pull title, date, and every metadata field present (frontmatter, headers, filename conventions, structured prefixes). Record per-field coverage and cardinality across the corpus.
3. **Classify the corpus** per browser-patterns.md: reader-first, corpus-first, or table-first. Derive facets only from fields that earn them (present on most docs, 2–15 values). State your choice and derived facets to the user in one short line before building.

**Privacy pass** — run the browser-patterns.md privacy scan over the corpus before embedding; report any redactions in chat.

**Build** — the chosen layout from browser-patterns.md, with the skill's full aesthetic treatment: pick a fresh font pairing and palette, both themes, no slop patterns. Narratives render as flowing prose under the skill's typography rules; section them in the reader only where the source documents have sections. Embed the full corpus as JSON, all interaction client-side.

**Verify** — the skill's global Verify checklist plus every browser-specific check in browser-patterns.md. The census check is the completion criterion: header count = nav count = source count, every narrative reachable and rendered.

Write to `~/.agent/diagrams/` with a descriptive corpus-based filename, open in the browser, and tell the user the path.

$@
