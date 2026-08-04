# Document Browser Patterns

Reference for building a **corpus browser** — a single self-contained HTML file that lets the user peruse a collection of documents (trip reports, research notes, meeting minutes, incident writeups, articles) with navigation, search, and filtering. The documents are the content; the browser is the container. All the skill's global rules apply (aesthetics, anti-patterns, verify checklist, single-file delivery); this file adds only what's browser-specific.

## The corpus decides the shape

Inspect the corpus before choosing anything: how many documents, what metadata they share, how long the narratives run. Every structural choice below derives from that inspection. A corpus of 5 untagged markdown essays and a corpus of 60 richly-tagged reports produce different browsers — both correct.

**Derive, don't invent.** Facets, groupings, and within-doc sections come *from* the corpus's actual metadata and structure. A field earns a facet when it exists on most documents and has 2–15 distinct values. A narrative renders as flowing prose under the skill's typography rules; sectioning appears in the reader only when the source documents have sections (headings, timestamps, labeled entries). When metadata is thin, the browser is a doc list plus full-text search plus a reader — that is a complete output, not a degraded one.

## Three layouts

Classify the corpus, pick one:

| Layout | When | Shape |
|---|---|---|
| **Reader-first** | ~3–8 docs, little shared metadata | Tab bar or compact top nav; one big reading column; search optional |
| **Corpus-first** | ~9+ docs, shared metadata worth filtering | Master–detail: sticky sidebar (grouped doc list, search, facet pills) + reader pane |
| **Table-first** | Metadata matters more than narrative (logs, structured records) | Filterable/sortable table as the main view; row click opens a detail drawer or reader |

Hybrids are fine (a table-first browser can still have a full reader pane) — but commit to one primary view.

## Master–detail skeleton (corpus-first)

The canonical structure, top to bottom:

1. **Brand block** — corpus title, one-line context, and header stats: total doc count plus per-facet counts. The doc count is a verification anchor — it must equal the number of source documents.
2. **Controls** — search input (matches metadata *and* narrative text) and facet filter pills. Live filtering, no Apply button. Show an active-filter note with a clear affordance whenever any filter is on.
3. **Nav** — the doc list, grouped by the most meaningful facet, each item showing a stable ID plus 1–2 scannable metadata values. Selected state visually distinct. Filtered-out items hide; group counts update.
4. **Reader pane** — the selected document: title, metadata badges, a metadata card (definition list) for the full record, then the narrative. Cap the reading column at ~65–75ch.
5. **Cross-filtering** (when the corpus has tags): clicking a tag inside the reader filters the nav to documents sharing it — the highest-leverage interaction a browser can offer.

Sidebar collapses to a toggleable drawer or top bar under ~800px; the reader is the mobile-first surface.

## Mechanics

- **Embed the corpus as data.** All documents go into a single `<script type="application/json">` block, parsed at load; rendering, search, and filtering are pure client-side JS. No fetch, no sidecar files.
- **State** is one small JS object (query, active facets, selected doc). Optionally mirror selection in the URL hash so a specific doc can be bookmarked.
- **Escape everything** interpolated from data into HTML (`&<>"`), or build via `createElement`/`textContent`. Document narratives are untrusted strings.
- **Markdown narratives**: convert to HTML at generation time (you, not a client-side library) so the file needs no markdown runtime.
- **Scale**: render the nav list fully up to ~500 docs; beyond that, paginate or render only matching items. Warn the user when the embedded corpus pushes the file past ~5 MB.
- **Keyboard**: ↑/↓ or j/k moves between docs, `/` focuses search. Cheap to add, transforms perusal.

## Privacy pass

The file embeds the **entire corpus** — filters hide documents from view, not from the source, and the file is built to be shared. Before embedding, scan the corpus for credential-shaped values (API keys, tokens, `Authorization`/`Cookie` headers, private-key blocks, credentials in URLs) and personal identifiers the user may not intend to ship (emails, phone numbers, full names in sensitive contexts). Replace hits with stable placeholders (`[REDACTED:key#1]`), tell the user in chat what was redacted and how many, and treat verbatim embedding of a flagged value as an explicit opt-in. After writing the file, grep it for the same patterns — no hits is the pass condition.

## Browser-specific verify checks

Run these in addition to the skill's global Verify checklist:

- **Census**: header doc count = nav item count (unfiltered) = source document count. Every document is reachable and its full narrative renders.
- **Field accounting**: every metadata field is surfaced as a facet, shown in the metadata card, or deliberately dropped — and you can say which for each.
- **Search reaches narratives**: a phrase that appears only inside one document's body text finds that document.
- **Filter round-trip**: apply each facet, confirm counts; clear all, confirm the full corpus returns.
- **Empty state**: a filter combination matching nothing shows a "no documents match" state with a clear-filters affordance, not a blank pane.
