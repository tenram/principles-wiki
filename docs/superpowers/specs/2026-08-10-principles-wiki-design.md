# Principles Wiki — Design Spec

Date: 2026-08-10
Status: Approved (design), pending implementation plan

## Purpose

Turn the essay `principios-de-mi.md` into a living, evolving wiki. The user invokes
`/principles-wiki` and says "ingest this quote." The tool researches the quote's
provenance (honestly), then weaves the quote into the essay in the essay's own voice.
Over time the wiki becomes an up-to-date, growing version of the essay.

This adapts the operational model of `llm-wiki` (raw/ immutable sources + wiki/ compiled
articles, with Ingest / Query / Lint operations) to a different content type: personal
aphorisms and quotes compiled into a single-author Spanish-language credo, rather than web
articles compiled into a neutral knowledge base.

## Two source dimensions studied

- **Voice dimension** — `/Users/jorgetena/Claude-Code/conosthens/theory/principios-de-mi.md`
  and `principles-corpus.md`. First-person Spanish latino, calm and plainspoken. Quotes
  appear in their original language with translation when needed; provenance lives in
  end-notes as *señas* (signposts), never as proof, because "lo que sostiene cada idea es la
  experiencia, no la cita." Organized as prefacio + 8 themed principles + a 4-step decision
  method (darse cuenta, reconocer, resolver, decidir) + 33 end-notes.
- **Mechanics dimension** — `/Users/jorgetena/Claude-Code/llm-wiki`, the `karpathy-llm-wiki`
  skill: `raw/` (immutable) + `wiki/` (compiled), `index.md` + `log.md`, Ingest (fetch then
  compile, merge-on-same-thesis), Query, Lint (deterministic auto-fix + heuristic report),
  and reference templates.

## Approved design decisions

1. **Entry model: one entry per principle; quotes merge in.** Each of the 8 principles (plus
   prefacio and método) is a single evolving prose file. Ingesting a quote weaves it into the
   relevant file's prose. The wiki IS the living essay, section by section.
2. **Provenance: web research + honest taxonomy.** The tool searches the web for public
   quotes and classifies them with the corpus taxonomy. It never asserts a contested
   attribution as fact ("comúnmente atribuida a X"). Personal/family/own quotes are flagged by
   the user at ingest time and are trusted without web search.
3. **New themes: propose, then ask.** When a quote fits no existing principle well, the tool
   proposes the best-fit principle OR a new principle, explains its reasoning, and waits for
   the user's decision before writing. The user stays editor of the essay's structure.
4. **Seed & language: seed from the essay, all Spanish.** The wiki is bootstrapped by
   importing the current 8 principles, prefacio, método, and 33 notes from
   `principios-de-mi.md`. Entries, prose, and scaffolding (index/log) are all Spanish latino.
5. **Notes keyed by stable slug, numbered only on export.** Notes carry stable slug-anchors
   internally so ingests never trigger global renumbering. Sequential `[1]…[N]` numbering is
   generated only at Export.
6. **Export step included.** A compile operation stitches prefacio + principles + método +
   renumbered notes into a single up-to-date `principios-de-mi.md`-style document.
7. **Packaged as a skill** named `principios-wiki`, invoked as `/principles-wiki`, self-
   contained in the target folder for portability.

## Directory layout

```
principles-wiki/
  .claude/skills/principios-wiki/
    SKILL.md
    references/
      voice-guide.md            distilled essay voice + rules
      attribution-taxonomy.md   family / JATR / folk / public:solid|paraphrase|contested
      principle-template.md
      raw-template.md
      index-template.md
  raw/<theme>/YYYY-MM-DD-slug.md
  wiki/
    00-prefacio.md
    01-ejecucion-sobre-intencion.md
    02-deber-antes-que-deseo.md
    03-tiempo-y-legado.md
    04-cambio-y-tradicion.md
    05-conocerse-y-reflexion.md
    06-como-te-perciben.md
    07-palabra-y-silencio.md
    08-el-foco.md
    metodo.md
    notas.md
    index.md
    log.md
```

## Operations

### Ingest (primary)

Invocation: `/principles-wiki ingest "<quote>"` with an optional attribution hint
(e.g. `"...", de mi hermana Debra`, or `Marco Aurelio`, or nothing).

1. **Parse** the quote text and any attribution hint.
2. **Classify provenance:**
   - Personal/family source flagged by user → `[family]`/`[personal]`, no web search.
   - Author's own → `[JATR]`, no web search.
   - Otherwise → web research, then classify `[folk]`, `[public: solid]`,
     `[public: paraphrase]`, or `[public: contested]`. Contested attributions are written as
     "comúnmente atribuida a X." Never fabricate a source. If research is inconclusive, say so.
3. **Capture to raw/**: original language + translation if needed + provenance notes +
   confidence tag, at `raw/<theme>/YYYY-MM-DD-slug.md` (immutable).
4. **Route**: propose best-fit existing principle OR propose a new principle, explain the
   reasoning, and WAIT for the user's decision before writing to wiki/.
5. **Compile**: weave the quote into the chosen principle's prose in the essay voice
   (per voice-guide). Add its note to `notas.md` with a stable slug-anchor.
6. **Cascade + bookkeeping**: check other principles and método for ripple effects; update
   `index.md` (row per principle) and append to `log.md`.

### Query

Search the wiki and answer questions ("¿qué digo sobre el silencio?"). Read `index.md`,
read relevant principle files, synthesize, cite with relative links. Optionally archive the
answer as a new page when the user asks.

### Lint

- **Deterministic (auto-fix):** index vs wiki file consistency; note-reference resolution
  (every in-text note anchor resolves to a `notas.md` entry and vice versa); orphan detection
  (quotes captured in `raw/` not yet woven into any wiki file).
- **Attribution-honesty check (report):** flag any note that asserts a contested attribution
  as fact rather than "comúnmente atribuida."
- **Heuristic (report):** voice drift, redundant quotes, principles growing unbalanced.

### Export

Stitch `00-prefacio` + principles `01–08` + `metodo` + a renumbered notes section into one
document mirroring the current `principios-de-mi.md` structure. Sequential note numbers are
assigned here from the stable slug-anchors.

## The voice guide (linchpin)

`references/voice-guide.md` distills the rules every ingest must follow:

- First person, Spanish latino.
- Quotes in original language, with translation when needed.
- Provenance is a signpost in the notes, never proof in the body. Experience carries the
  idea, not the citation.
- Calm, direct, plainspoken, no drama, no corporate gloss.
- No dashes to separate ideas; use commas, colons, semicolons.
- Preserve the essay's cadence: a principle opens with a lived observation, then the quote
  arrives to crystallize it, then a plain gloss on why it holds.

## Out of scope

- No web UI or rendering layer; markdown files only.
- No automated attribution beyond honest web research; the user adjudicates disputes.
- No multi-author support; single-author credo by design.

## Success criteria

- Seeded wiki reproduces the current essay's content across the section files.
- Ingesting a public quote produces an honest provenance note and a voice-consistent
  weave, after user confirms routing.
- Ingesting a personal quote skips web search and tags it correctly.
- Export regenerates a coherent, correctly-numbered full essay from the section files.
```
