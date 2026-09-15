---
name: principios-wiki
description: "Use to grow the living wiki version of principios-de-mi.md. Triggers: 'ingest this quote', 'ingesta esta cita', '/principles-wiki', add a quote/aphorism to the principles wiki, query what I say about a theme, lint the principles wiki, or export the full essay."
---

# Principios Wiki

Grow and maintain the living wiki version of the essay `principios-de-mi.md`. You
manage `raw/` (immutable captured quotes + provenance) and `wiki/` (the living
essay, one prose file per principle). The wiki compounds over time.

Before writing ANY prose into `wiki/`, read `references/voice-guide.md`. Before
classifying provenance, read `references/attribution-taxonomy.md`.

## Layout

- `raw/<theme>/YYYY-MM-DD-slug.md` — captured quote + provenance. Immutable once written.
- `wiki/00-prefacio.md … 08-el-foco.md`, `metodo.md` — the living essay, prose.
- `wiki/notas.md` — `[^slug]: text` note definitions. Slugs are stable.
- `wiki/index.md` — one row per section. `wiki/log.md` — append-only operation log.

## Ingest (primary)

Invoked as `/principles-wiki` with a quote and an optional attribution hint,
e.g. `ingesta esta cita: "..." — de mi hermana Debra`.

1. Parse the quote text and any attribution hint.
2. Classify provenance using attribution-taxonomy.md:
   - Personal/family/own → trust it, no web search.
   - Otherwise → web research, then tag honestly. Contested → "comúnmente atribuida a X".
     Never fabricate. If inconclusive, say so.
3. Capture to `raw/<theme>/YYYY-MM-DD-slug.md` using references/raw-template.md.
   Assign a stable `[^slug]` note anchor now.
4. Route: propose the best-fit existing principle OR propose a new principle,
   explain the reasoning, and WAIT for the user's decision before writing to wiki/.
5. Compile: following voice-guide.md, weave the quote into the chosen principle's
   prose, with quoted wording in bold and parenthetical author in italics. Keep raw
   capture unchanged. Add the note definition to notas.md. Add the slug plus a short
   cue or provenance hint to that section's "Notas de esta sección", using `- [^slug]
   — breve pista`.
   If the parenthetical already contains italic text, use outer underscores so the
   inner title keeps its markdown form.
6. Cascade: check other principles and metodo.md for ripple effects; update any
   affected file. Update index.md (refresh the row's Actualizado date) and append
   to log.md:
   `## [YYYY-MM-DD] ingest | <cita corta> -> <principio>`

## Query

Answer questions about the credo ("¿qué digo sobre el silencio?"). Read index.md,
read the relevant principle files, synthesize in Spanish, cite with relative links.
Do not write files unless the user asks to archive; if so, write a new page and
prefix its index Resumen with `[Archivo]`.

## Lint

Deterministic (auto-fix): index vs wiki file consistency; every `[^slug]` used in a
wiki file has a definition in notas.md and vice versa; orphan detection (quotes in
`raw/` whose slug is not woven into any wiki file).
Attribution-honesty (report): flag any note asserting a contested attribution as
fact instead of "comúnmente atribuida".
Heuristic (report): voice drift, redundant quotes, unbalanced principles.
Append to log.md: `## [YYYY-MM-DD] lint | <N> issues, <M> auto-fixed`.

## Export

Stitch `00-prefacio` + `01…08` + `metodo` into one document. Collect every `[^slug]`
in order of first appearance, assign sequential numbers `[1]…[N]`, replace anchors
with those numbers in the exported text, and render a final `## Notas` list in that
numeric order. Write to `wiki/export/principios-de-mi-YYYY-MM-DD.md`. Do not modify
the source `wiki/` files.

## Conventions

- Spanish latino for all wiki content. No dashes as separators; commas/colons/semicolons.
- Today's date for Collected, log, and Actualizado dates.
- One level of theme subdirectories in raw/ only.
