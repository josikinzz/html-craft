# Anti-Patterns (AI Slop)

The single home for everything forbidden. These patterns signal "AI-generated template". Review every generated page against this list — that is the slop test in the Verify step of `../SKILL.md`.

## Typography

**Forbidden fonts as primary `--font-body`:**
- Inter — the single most overused AI default
- Roboto, Arial, Helvetica — generic system fallbacks promoted to primary
- system-ui, sans-serif alone — no character, no intent

**Monoculture fonts — avoid as reflex picks.** These are training-data defaults that make every AI-generated page look related: Instrument Serif, Instrument Sans, DM Sans, DM Serif Display/Text, IBM Plex (Sans/Serif/Mono), Plus Jakarta Sans, Space Grotesk, Space Mono, Outfit, Fraunces, Playfair Display, Crimson Pro/Text, Cormorant, Newsreader, Lora, Syne. They aren't broken fonts — but if one of these is your first instinct, that's the trained reflex talking.

**Instead:** pick from the font pairings in `./libraries.md`. Every generation uses a different pairing from the last.

## Color Palette

**Forbidden accent colors:**
- Indigo-500/violet-500 (`#8b5cf6`, `#7c3aed`, `#a78bfa`) — Tailwind's default purple range
- Fuchsia (`#d946ef`) and the cyan + magenta + pink neon gradient combination (`#06b6d4` → `#d946ef` → `#f472b6`)
- Any palette that could be described as "Tailwind defaults with purple/pink/cyan accents"

**Forbidden color effects:**
- Gradient text on headings (`background: linear-gradient(...); background-clip: text;`)
- Multiple overlapping radial glows in accent colors creating a "neon haze"
- Pure `#000` backgrounds or pure `#fff` text/backgrounds — always tint toward the palette's hue
- Gray text sitting on a colored background — it reads washed out; use a shade of the background hue

**Instead:** build palettes from the accent palettes in the Style step, or derive from a real IDE theme (Dracula, Nord, Solarized, Gruvbox, Catppuccin).

## Contrast & Legibility

Unreadable is worse than ugly. A page that looks striking in a screenshot and can't be read is a failed page.

**Forbidden:**
- **White or near-white text on a mid-tone or bright fill** — white on pale green, mint, amber, sky, coral, or lime. This is the most common readability failure in generated pages; the bright accents that look great as *text on dark* land at 1.4–2.7:1 as *fills under white*. Bright fill takes dark ink.
- `color: #fff` (or `var(--bg)`) hardcoded on top of `background: var(--accent)` without checking which tone the accent actually is. It passes in one theme and fails in the other.
- Accent-colored text at 10–12px on a tint of that same accent (status badges, tags, code chips, callout titles). Deep-enough-to-read on light backgrounds means deep — `#059669`, `#d97706`, and `#0891b2` all sit at 3.1–3.7:1 and fail.
- Body copy, bullets, or table cells set in `--text-dim`.
- Free-floating text over a striped, hatched, ruled, or dot-grid background — including text over a repeating-gradient "dead time" bar or a patterned progress segment.
- Background line patterns drawn in `--border`, or above ~0.06 alpha, or at a repeat spacing tight enough (under ~20px) to read as stripes rather than texture.
- Decorative watermark numerals or quote marks behind text at an opacity high enough to compete with it (keep ≤0.08).
- Text over a background image or bold gradient with no scrim between them.

**Instead:** two-tone accents (ink + fill), the contrast contract in the Style step, decoration behind surfaces rather than behind prose, and a scrim under any text over imagery. Verify with `scripts/check-contrast.py` rather than by eye — the failures are systematic, not obvious.

## Motion

**Forbidden:**
- Entrance animations of any kind — staggered fade-ins, reveals, draw-ins, count-ups
- Animated glowing box-shadows (`@keyframes glow { box-shadow: 0 0 20px... }`)
- Pulsing/breathing effects and continuous animations that run after page load
- Decorative hover effects on non-interactive elements (card lift, scale-on-hover)

**Instead:** the page renders complete and at rest, like print. A transition appears only as feedback on a genuinely interactive control (button, row, input, `<details>`), and stays under 0.2s.

## Section Headers

**Forbidden:**
- Emoji icons in section headers (🏗️, ⚙️, 📁, 💻, 📅, 🔗, ⚡, 🔧, 📦, 🚀)
- Section headers that all use the same icon-in-rounded-box pattern

**Instead:** vary the labeling voice between generations — numbered mono tabs, small-caps headers, serif italic labels, asymmetric section dividers (the templates each demonstrate a different one). If an icon is genuinely needed, use a Lucide icon via the Iconify web component (see "Icons" in `./libraries.md`) or a palette-matched inline SVG.

## Accent Side-Stripes

**Forbidden:** `border-left` (or `border-right`) wider than 1px used as a colored accent stripe on cards, callouts, alerts, list items, or pull quotes — hard-coded colors and CSS variables alike (`border-left: 3px solid var(--accent)` is just as banned as `border-left: 4px solid red`). This is the single most recognizable AI "design touch" in dashboards and docs.

**Instead:** rewrite the element with a different structure — a full 1px border tinted toward the accent, an accent-tinted background (`color-mix(in srgb, var(--accent) 8%, transparent)`), a leading label/number/dot in the accent color, or no indicator at all. An inset box-shadow standing in for the stripe is the same pattern and fails the same way. (A 2px active-state indicator in a nav/TOC is a functional affordance, not a decorative stripe — that's fine.)

## Layout & Hierarchy

**Forbidden:**
- Perfectly centered everything with uniform padding
- All cards styled identically with the same border-radius, shadow, and spacing
- Every section getting equal visual treatment — no hero/primary vs. secondary distinction
- Symmetric layouts where left and right halves mirror each other

**Instead:** vary visual weight. Hero sections dominate (larger type, more padding, accent-tinted background). Reference sections feel compact. Use the depth tiers (hero → elevated → default → recessed). Asymmetric layouts create interest.

## Template Patterns

**Forbidden:**
- Three-dot window chrome (red/yellow/green dots) on code blocks
- KPI cards where every metric has identical gradient text treatment
- "Neon Dashboard" as an aesthetic choice (cyan + magenta + purple on dark)
- Gradient meshes with pink/purple/cyan blobs in the background

**Instead:** code blocks use a simple header with filename or language label. KPI cards vary by importance — hero numbers for the primary metric, subdued treatment for supporting metrics. Pick aesthetics with natural constraints (Blueprint, Editorial, Paper/ink).

## The Slop Test

**Would a developer looking at this page immediately think "AI generated this"?** The telltale signs:

1. Inter or Roboto font with purple/violet gradient accents
2. Every heading has `background-clip: text` gradient
3. Emoji icons leading every section
4. Glowing cards with animated shadows
5. Cyan-magenta-pink color scheme on dark background
6. Perfectly uniform card grid with no visual hierarchy
7. Three-dot code block chrome
8. Colored accent stripes (`border-left: 3px+`) on cards and callouts
9. The same two or three "safe" fonts (Instrument Serif, DM Sans, IBM Plex) as every generation before

Two or more present means the page is slop. Regenerate with a different aesthetic direction — Editorial, Blueprint, Paper/ink, or a specific IDE theme. These constrained aesthetics are harder to mess up because their specific visual requirements block the generic defaults.
