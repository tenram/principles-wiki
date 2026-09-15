# Principles Wiki Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `/principles-wiki`, a skill that grows `principios-de-mi.md` into a living wiki by ingesting quotes, researching provenance honestly, and weaving each quote into the essay's voice per principle.

**Architecture:** A self-contained Claude Code skill in the target folder manages a `raw/` layer (immutable captured quotes + provenance) and a `wiki/` layer (the living essay, one prose file per principle). Operations are Ingest, Query, Lint, Export. The wiki is seeded from the current essay so it starts complete.

**Tech Stack:** Markdown only. No runtime, no test framework. "Tests" are content/structure assertions run with Grep and Read.

## Global Constraints

- Language: Spanish latino for all wiki prose, notes, index, and log. Skill instructions (SKILL.md, references) may be in English.
- Voice: first person; quotes in original language with translation when needed; provenance is a signpost in the notes, never proof in the body; calm, plainspoken, no drama, no corporate gloss.
- No dashes to separate ideas anywhere in wiki prose; use commas, colons, semicolons.
- Provenance honesty: never assert a contested attribution as fact; write "comúnmente atribuida a X." Never fabricate a source.
- Source of truth for seeding: `/Users/jorgetena/Claude-Code/conosthens/theory/principios-de-mi.md`.
- Skill invocation name: `principios-wiki` (invoked as `/principles-wiki`).
- Notes use stable slug-anchors (`[^slug]`) internally; sequential numbering happens only at Export.
- Git is currently non-functional on this machine; treat every "Commit" step as an optional checkpoint (skip if `git` errors).

## Canonical note anchor map

Every essay end-note maps to a stable slug. Use these exact anchors when converting the seed and when adding new notes:

```
[1]  -> dalio                 [12] -> jtr-puerta            [23] -> washington-demonios
[2]  -> mahler-fuego          [13] -> recuerdo-manana       [24] -> ligia-felicidad
[3]  -> jtr                   [14] -> montagu-joven         [25] -> jtr-callar
[4]  -> marco-aurelio-colmena [15] -> franklin-sabios       [26] -> refran-amo-callas
[5]  -> ford-vision           [16] -> refran-joven-viejo    [27] -> refran-carbon-lena
[6]  -> levenson-reloj        [17] -> felicidad-futuro      [28] -> refran-burra
[7]  -> gregorio-antes        [18] -> heraclito-cambio      [29] -> marco-aurelio-correcto
[8]  -> refran-actitud        [19] -> seneca-ensenar        [30] -> mamet-duda
[9]  -> welch-destino         [20] -> jtr-escuchar          [31] -> reagan-confia-verifica
[10] -> jtr-deber             [21] -> tretera-espacio       [32] -> loop-seis-pasos
[11] -> jtr-familia           [22] -> refran-juzgan         [33] -> camus-tipasa
```

## Seed source-to-file map

Copy prose verbatim from the source essay, then apply the anchor conversion. Line ranges refer to `principios-de-mi.md`:

```
00-prefacio.md                  lines 11-27  (Intro + Prefacio)
01-ejecucion-sobre-intencion.md lines 33-45
02-deber-antes-que-deseo.md     lines 47-55
03-tiempo-y-legado.md           lines 57-63
04-cambio-y-tradicion.md        lines 65-69
05-conocerse-y-reflexion.md     lines 71-79
06-como-te-perciben.md          lines 81-85
07-palabra-y-silencio.md        lines 87-91
08-el-foco.md                   lines 93-97
metodo.md                       lines 101-103 (Transición) + 107-119 (método)
                                + 121-123 (Apéndice) + 127-131 (Despedida)
notas.md                        lines 137-169 (33 notes), converted to [^slug] entries
```

## File Structure

```
principles-wiki/
  .claude/skills/principios-wiki/
    SKILL.md
    references/
      voice-guide.md
      attribution-taxonomy.md
      principle-template.md
      raw-template.md
      index-template.md
  raw/.gitkeep
  wiki/
    00-prefacio.md … 08-el-foco.md, metodo.md, notas.md, index.md, log.md
```

---

### Task 1: Scaffold directories and skeleton files

**Files:**
- Create: `.claude/skills/principios-wiki/references/.gitkeep`
- Create: `raw/.gitkeep`
- Create: `wiki/index.md`
- Create: `wiki/log.md`

**Interfaces:**
- Produces: the directory tree all later tasks write into; `wiki/index.md` (heading `# Índice de Principios`) and `wiki/log.md` (heading `# Bitácora`) as empty-bodied files.

- [ ] **Step 1: Define the check**

Verify these paths exist after creation: `.claude/skills/principios-wiki/references/`, `raw/`, `wiki/index.md`, `wiki/log.md`.

- [ ] **Step 2: Run the check to confirm it fails**

Run: `ls wiki/index.md wiki/log.md .claude/skills/principios-wiki/references/`
Expected: errors, paths do not exist.

- [ ] **Step 3: Create the files**

Write `wiki/index.md`:
```markdown
# Índice de Principios

```
Write `wiki/log.md`:
```markdown
# Bitácora

```
Create empty `.gitkeep` in `raw/` and `.claude/skills/principios-wiki/references/`.

- [ ] **Step 4: Run the check to confirm it passes**

Run: `ls wiki/index.md wiki/log.md .claude/skills/principios-wiki/references/`
Expected: all listed, no errors.

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "chore: scaffold principles-wiki tree"
```

---

### Task 2: Write the voice guide

**Files:**
- Create: `.claude/skills/principios-wiki/references/voice-guide.md`

**Interfaces:**
- Produces: `voice-guide.md`, the rules every Ingest reads before writing prose. Referenced by SKILL.md Compile step (Task 6).

- [ ] **Step 1: Define the check**

The file must state, explicitly: first person Spanish latino; quotes in original language with translation when needed; provenance as señas in notes not proof in body ("lo que sostiene cada idea es la experiencia, no la cita"); calm/plainspoken/no drama; no dashes (use commas, colons, semicolons); and the cadence rule (lived observation → quote crystallizes it → plain gloss on why it holds).

- [ ] **Step 2: Run the check to confirm it fails**

Run: `ls .claude/skills/principios-wiki/references/voice-guide.md`
Expected: does not exist.

- [ ] **Step 3: Write the file**

Content (verbatim):
```markdown
# Voice Guide — how to write in the essay's voice

Read this before writing or editing any prose in `wiki/`. The living essay must
read as one person's voice, not as generic assistant prose.

## Non-negotiables

- First person, Spanish latino. The narrator is the author.
- Quotes appear in their original language. Add a short translation in parentheses
  only when the quote is not in Spanish and the meaning would otherwise be lost.
- Provenance is a signpost, and it lives in the notes, never in the body as proof.
  The body carries the lived idea; the note carries the source. Guiding line:
  "lo que sostiene cada idea es la experiencia, no la cita."
- Calm, direct, plainspoken. No drama, no hype, no corporate gloss.
- No dashes to separate ideas. Use commas, colons, semicolons.

## Cadence of a principle

A principle moves in three beats:
1. A lived observation, stated plainly and often at the author's own cost.
2. The quote arrives to crystallize what was just said, with its `[^slug]` note.
3. A plain gloss on why the idea holds, no moralizing.

Weave new quotes into this rhythm. Do not append a quote as a bare list item; fold
it into the flowing prose of the principle it belongs to.

## What to avoid

- Emoji, exclamation, and marketing verbs.
- Asserting a contested attribution as fact (see attribution-taxonomy.md).
- Bullet lists in the essay body. The essay is prose.
```

- [ ] **Step 4: Run the check to confirm it passes**

Run: `grep -c "señas\|no dashes\|primera\|First person" .claude/skills/principios-wiki/references/voice-guide.md` (via Grep tool)
Expected: matches present for the key rules.

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "docs: add voice guide"
```

---

### Task 3: Write the attribution taxonomy

**Files:**
- Create: `.claude/skills/principios-wiki/references/attribution-taxonomy.md`

**Interfaces:**
- Produces: the classification buckets used by the Ingest provenance step (Task 6) and the Lint attribution-honesty check.

- [ ] **Step 1: Define the check**

The file must define six buckets with their footnote rendering: `[family]`, `[personal]`, `[JATR]`, `[folk]`, `[public: solid]`, `[public: paraphrase]`, `[public: contested]`, and state that contested attributions render as "comúnmente atribuida a X" and are never asserted as fact.

- [ ] **Step 2: Run the check to confirm it fails**

Run: `ls .claude/skills/principios-wiki/references/attribution-taxonomy.md`
Expected: does not exist.

- [ ] **Step 3: Write the file**

Content (verbatim):
```markdown
# Attribution Taxonomy

Classify every ingested quote into exactly one bucket. The bucket decides whether
web research runs and how the note is phrased.

| Bucket | When | Web research? | Note phrasing |
|--------|------|---------------|---------------|
| `[family]` | attributed to a family member (padre, madre, etc.) | No | name + relation, e.g. "Jorge Tena Reyes, padre del autor" |
| `[personal]` | attributed to a named private person the user flags | No | name + relation as the user gave it, e.g. "de mi hermana Debra" |
| `[JATR]` | the author's own line | No | omit source or mark as the author's own |
| `[folk]` | proverb / dicho with no fixed author | Light | "refrán popular" / "dicho de uso familiar; sin autor cierto" |
| `[public: solid]` | public figure, attribution well supported | Yes | assert plainly with brief identity |
| `[public: paraphrase]` | a summary of a public thinker, not verbatim | Yes | "(paráfrasis de su pensamiento)" |
| `[public: contested]` | commonly attributed but not reliably sourced | Yes | "comúnmente atribuida a X" (never asserted as fact) |

Rules:
- Never fabricate a source. If research is inconclusive, say so and pick `[folk]`
  or `[public: contested]` accordingly.
- If the user flags a private source at ingest time, use `[family]` or `[personal]`
  and skip web research entirely.
```

- [ ] **Step 4: Run the check to confirm it passes**

Run (Grep): pattern `comúnmente atribuida` in the file.
Expected: present.

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "docs: add attribution taxonomy"
```

---

### Task 4: Write the three templates

**Files:**
- Create: `.claude/skills/principios-wiki/references/raw-template.md`
- Create: `.claude/skills/principios-wiki/references/principle-template.md`
- Create: `.claude/skills/principios-wiki/references/index-template.md`

**Interfaces:**
- Produces: exact formats consumed by SKILL.md (Task 6) for capturing raw quotes, structuring principle files, and rendering the index.

- [ ] **Step 1: Define the check**

Three files exist; `raw-template.md` has fields Source/Collected/Bucket/Original/Translation; `principle-template.md` shows a title + flowing prose + a "Notas de esta sección" list of `[^slug]` refs; `index-template.md` shows a table with columns Principio / Resumen / Actualizado.

- [ ] **Step 2: Run the check to confirm it fails**

Run: `ls .claude/skills/principios-wiki/references/{raw,principle,index}-template.md`
Expected: none exist.

- [ ] **Step 3: Write the files**

`raw-template.md`:
```markdown
# {Cita corta o slug}

> Fuente: {URL, o descripción de origen, o "de mi hermana Debra"}
> Recogida: {YYYY-MM-DD}
> Bucket: {family | personal | JATR | folk | public: solid | public: paraphrase | public: contested}
> Ancla de nota: [^{slug}]

## Original
{La cita en su lengua original.}

## Traducción
{Solo si hace falta.}

## Procedencia
{Lo que se encontró al investigar: quién, cuándo, y con qué grado de certeza.
Honesto: "comúnmente atribuida a X" cuando aplique.}
```

`principle-template.md`:
```markdown
# {Número}. {Título del principio}

{Prosa en la voz del ensayo. Observación vivida, luego la cita que la cristaliza
con su [^slug], luego el porqué se sostiene. Sin viñetas, sin guiones separadores.}

## Notas de esta sección
- [^{slug}]
```

`index-template.md`:
```markdown
# Índice de Principios

| Principio | Resumen | Actualizado |
|-----------|---------|-------------|
| [{Título}]({archivo}.md) | {una línea} | {YYYY-MM-DD} |
```

- [ ] **Step 4: Run the check to confirm it passes**

Run (Grep): `Ancla de nota` in raw-template; `Notas de esta sección` in principle-template; `Actualizado` in index-template.
Expected: all present.

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "docs: add raw/principle/index templates"
```

---

### Task 5: Seed the wiki prose (prefacio, 8 principles, método)

**Files:**
- Create: `wiki/00-prefacio.md`, `wiki/01-ejecucion-sobre-intencion.md`, `wiki/02-deber-antes-que-deseo.md`, `wiki/03-tiempo-y-legado.md`, `wiki/04-cambio-y-tradicion.md`, `wiki/05-conocerse-y-reflexion.md`, `wiki/06-como-te-perciben.md`, `wiki/07-palabra-y-silencio.md`, `wiki/08-el-foco.md`, `wiki/metodo.md`
- Read: `/Users/jorgetena/Claude-Code/conosthens/theory/principios-de-mi.md`

**Interfaces:**
- Consumes: the source-to-file map and the anchor map (top of this plan).
- Produces: ten prose files whose bodies match the source essay, with every in-text `[N]` replaced by its `[^slug]` anchor, and each file ending with a `## Notas de esta sección` listing the slugs it uses.

- [ ] **Step 1: Define the check**

For each file: its prose matches the mapped source lines; no bare `[N]` numeric refs remain (all converted to `[^slug]`); a `## Notas de esta sección` section lists exactly the anchors used in that file.

- [ ] **Step 2: Run the check to confirm it fails**

Run: `ls wiki/01-ejecucion-sobre-intencion.md`
Expected: does not exist.

- [ ] **Step 3: Write the files (worked example for Task, apply same pattern to all)**

Read the source, copy each file's mapped lines verbatim, then convert refs. Worked example for `wiki/01-ejecucion-sobre-intencion.md` (source lines 33-45), showing the conversion of `[5]`,`[6]`,`[7]`,`[8]`,`[9]` to anchors:

```markdown
# 1. La ejecución por encima de la intención

Aprendí temprano, y a mi costa, que la intención no cuenta. Lo que no se ejecuta no existe, por más noble que sea el plan que quedó en la cabeza. *"Una visión sin ejecución no es más que una alucinación"* (H. Ford)[^ford-vision]. Tiene razón el dicho, aunque no sea del todo suyo: soñar no basta, y confundir la intención con el logro es la trampa más cómoda que hay. Una idea que no se aterriza no cambia nada; solo consuela. El valor nunca estuvo en imaginarla, sino en la disciplina, muchas veces ingrata, de hacerla ocurrir.

De ahí que el tiempo no se mire, se use. *"No te detengas a mirar el reloj; haz lo que él hace y sigue avanzando"* (S. Levenson)[^levenson-reloj] es de las cosas que me repito cuando la ansiedad quiere disfrazarse de trabajo. Mirar el reloj no apura nada. Avanzar, sí: sin pausa y sin ruido. La constancia callada rinde más que la urgencia nerviosa, y llega más lejos que quien solo cuenta las horas que le faltan.

Hay una lección que viene de casa, de Gregorio Ramírez, el chófer de toda la vida de mi padre: *"mejor antes y no después"* (G. Ramírez)[^gregorio-antes]. Suena simple; es de las más difíciles. Casi todo lo importante se vuelve más barato y más fácil cuando se hace a tiempo, y más caro y más torpe cuando se posterga. La prisa de última hora es, casi siempre, la factura de una calma mal usada. Adelantarse es una forma de respeto, empezando por uno mismo.

Y cuando el resultado tarda, conviene recordar dónde está de verdad la diferencia. No suele faltar talento ni información; sobra, más bien. *"La diferencia entre una persona exitosa y el resto no es falta de fuerza o conocimiento, sino de actitud y voluntad"*[^refran-actitud]. Lo que separa a quien logra de quien no es la actitud con que empieza y la voluntad con que sostiene cuando ya dejó de ser novedad. El músculo que decide no es el del arranque, es el de la insistencia.

Sostener también es hacerse cargo. *"Controla tu propio destino, o alguien más lo hará"* (J. Welch)[^welch-destino] no es una frase de superación barata; es una advertencia. Si uno no dirige su vida, alguien la dirige, y rara vez a favor de uno. Tomar el timón no es un privilegio, es una obligación incómoda: obliga a elegir, a equivocarse y a responder. Ceder el mando se siente ligero un tiempo, hasta que uno ve adónde lo llevaron.

Cierro este primer punto con algo mío, de tanto pelearme con el arranque: *"cierto es que en esta vida puedes hacer de todo; incierto es si lo quieres hacer o no; y la duda yace en cómo hacerlo."* Casi todo es posible. Lo dudoso es si de verdad lo quiero. Y la duda honesta, la que de verdad frena, casi nunca está en el *si*; está en el *cómo*. Separar esas tres cosas, lo posible, lo deseado y el método, aclara más decisiones que cualquier arranque de fuerza de voluntad.

## Notas de esta sección
- [^ford-vision]
- [^levenson-reloj]
- [^gregorio-antes]
- [^refran-actitud]
- [^welch-destino]
```

Apply the identical pattern to the other nine files using the source-to-file and anchor maps. `00-prefacio.md` uses anchors `dalio, mahler-fuego, jtr, marco-aurelio-colmena`. `metodo.md` uses `marco-aurelio-correcto, mamet-duda, reagan-confia-verifica, loop-seis-pasos, camus-tipasa`. Preserve the `# Intro` / `## Prefacio`, `## Transición`, `# Parte 2 — El método`, `### Apéndice`, `## Despedida` headings inside their files.

- [ ] **Step 4: Run the check to confirm it passes**

Run (Grep, across `wiki/*.md` excluding notas.md): pattern `\[[0-9]+\]` (bare numeric refs).
Expected: zero matches (all converted to `[^slug]`).
Run (Grep): `## Notas de esta sección` count == 10.

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "feat: seed wiki prose from essay"
```

---

### Task 6: Seed notas.md

**Files:**
- Create: `wiki/notas.md`
- Read: `principios-de-mi.md` lines 137-169

**Interfaces:**
- Consumes: the anchor map; the `[^slug]` refs produced in Task 5.
- Produces: `wiki/notas.md` with one `[^slug]: text` entry per note, text taken from the source's Notas section.

- [ ] **Step 1: Define the check**

`notas.md` contains exactly 33 `[^slug]:` definitions, one per anchor in the map, and every anchor referenced in Task 5 files has a matching definition here.

- [ ] **Step 2: Run the check to confirm it fails**

Run: `ls wiki/notas.md`
Expected: does not exist.

- [ ] **Step 3: Write the file**

Header `# Notas`, then one definition per anchor. Copy each note's text from source lines 137-169. Example first three:
```markdown
# Notas

[^dalio]: Ray Dalio, *Principles* (2017), fundador del fondo Bridgewater Associates. Citado como el disparador de este texto, no como respaldo de sus ideas.
[^mahler-fuego]: Comúnmente atribuida a Gustav Mahler, compositor y director austríaco tardorromántico; circula también en la forma del francés Jean Jaurès, líder socialista e historiador. De atribución discutida.
[^jtr]: Jorge Tena Reyes, padre del autor; figura conocida en la vida política y cultural dominicana. Falleció en 2025.
```
Continue for all 33 using the anchor map order.

- [ ] **Step 4: Run the check to confirm it passes**

Run (Grep, count): `^\[\^[a-z-]+\]:` in `wiki/notas.md`.
Expected: 33.
Cross-check: every `[^slug]` used in `wiki/*.md` appears as a definition in notas.md (compare the union of Task 5 anchors against notas.md keys).

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "feat: seed notas.md with slug anchors"
```

---

### Task 7: Build index.md and log the seed

**Files:**
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`

**Interfaces:**
- Consumes: the ten prose files from Task 5.
- Produces: an index table with one row per principle file (plus prefacio and método), and a seed entry in the log.

- [ ] **Step 1: Define the check**

`index.md` has a row per file in `wiki/` (excluding index.md, log.md, notas.md), each with a one-line Spanish resumen and today's date. `log.md` has a `## [2026-08-10] seed` entry.

- [ ] **Step 2: Run the check to confirm it fails**

Run (Grep): `01-ejecucion-sobre-intencion.md` in `wiki/index.md`.
Expected: no match.

- [ ] **Step 3: Write the content**

`index.md`:
```markdown
# Índice de Principios

| Principio | Resumen | Actualizado |
|-----------|---------|-------------|
| [Prefacio](00-prefacio.md) | Por qué escribo esto: pasar el fuego. | 2026-08-10 |
| [1. La ejecución por encima de la intención](01-ejecucion-sobre-intencion.md) | Lo que no se ejecuta no existe. | 2026-08-10 |
| [2. El deber antes que el deseo](02-deber-antes-que-deseo.md) | Primero lo que se debe, después lo que se quiere. | 2026-08-10 |
| [3. El tiempo y el legado](03-tiempo-y-legado.md) | Sé hoy por lo que quieres que te recuerden. | 2026-08-10 |
| [4. El cambio y la tradición](04-cambio-y-tradicion.md) | Preservar el fuego, no adorar las cenizas. | 2026-08-10 |
| [5. El conocerse y la reflexión](05-conocerse-y-reflexion.md) | La inteligencia empieza en admitir que no se sabe. | 2026-08-10 |
| [6. Cómo te perciben los demás](06-como-te-perciben.md) | Te juzgan por cómo son ellos, no por lo que eres. | 2026-08-10 |
| [7. La palabra y el silencio](07-palabra-y-silencio.md) | Amo de lo que callas, esclavo de lo que dices. | 2026-08-10 |
| [8. El foco](08-el-foco.md) | No se puede ser carbón y leña a la vez. | 2026-08-10 |
| [El método](metodo.md) | Darse cuenta, reconocer, resolver, decidir. | 2026-08-10 |
```

Append to `log.md`:
```markdown
## [2026-08-10] seed | ensayo importado
- 10 secciones sembradas desde principios-de-mi.md
- 33 notas con anclas estables en notas.md
```

- [ ] **Step 4: Run the check to confirm it passes**

Run (Grep): count rows containing `.md)` in index.md == 10; `seed` present in log.md.

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "feat: build index and log seed"
```

---

### Task 8: Write SKILL.md (operations)

**Files:**
- Create: `.claude/skills/principios-wiki/SKILL.md`

**Interfaces:**
- Consumes: voice-guide.md, attribution-taxonomy.md, the three templates, and the seeded wiki.
- Produces: the operational contract for Ingest, Query, Lint, Export, invokable as `/principles-wiki`.

- [ ] **Step 1: Define the check**

SKILL.md has YAML frontmatter with `name: principios-wiki` and a description that triggers on "ingest this quote", "ingesta esta cita", "/principles-wiki". It documents four operations (Ingest, Query, Lint, Export) matching the spec, and the Ingest section enforces: parse hint → classify via taxonomy → capture raw → propose routing and WAIT → compile per voice-guide → cascade + update index/log.

- [ ] **Step 2: Run the check to confirm it fails**

Run: `ls .claude/skills/principios-wiki/SKILL.md`
Expected: does not exist.

- [ ] **Step 3: Write the file**

Content (verbatim):
```markdown
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
   prose (observation → quote with its `[^slug]` → plain gloss). Add the note
   definition to notas.md. Add the slug to that section's "Notas de esta sección".
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
```

- [ ] **Step 4: Run the check to confirm it passes**

Run (Grep): `name: principios-wiki` present; `## Ingest`, `## Query`, `## Lint`, `## Export` all present; `WAIT for the user` present in Ingest.

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "feat: add principios-wiki SKILL.md"
```

---

### Task 9: End-to-end verification (dry ingest + export sanity)

**Files:**
- Read: all of `wiki/` and `.claude/skills/principios-wiki/`

**Interfaces:**
- Consumes: everything built. Produces: confirmation the skill is coherent and the seed is faithful.

- [ ] **Step 1: Define the checks**

  1. Anchor integrity: the set of `[^slug]` used across `wiki/*.md` (excluding notas.md) equals the set of definitions in notas.md (33 each, no orphans, no undefined).
  2. No bare numeric refs remain in any wiki prose file.
  3. Seed fidelity: spot-check that `01`, `05`, and `metodo` prose matches the source essay's mapped lines (same sentences, only refs converted).
  4. Skill discoverability: SKILL.md frontmatter name is `principios-wiki`.

- [ ] **Step 2: Run the checks**

Run (Grep) across `wiki/`:
- `\[[0-9]+\]` in `wiki/*.md` except notas.md → expect 0.
- collect `\[\^[a-z0-9-]+\]` uses vs `^\[\^[a-z0-9-]+\]:` defs → expect equal sets.
Read `wiki/05-conocerse-y-reflexion.md` and compare against source lines 71-79.

- [ ] **Step 3: Fix any mismatch**

If a slug is used but undefined, add its definition to notas.md from the source note. If a numeric ref remains, convert it. If prose diverged from source, correct it.

- [ ] **Step 4: Confirm all checks pass**

Re-run the Grep checks; expect 0 orphans, 0 numeric refs, equal anchor sets.

- [ ] **Step 5: Commit (optional checkpoint)**

```bash
git add -A && git commit -m "test: verify seed integrity and skill coherence"
```

---

## Self-Review

**Spec coverage:**
- Entry model (one file per principle, quotes merge in) → Tasks 5, 8 (Compile).
- Provenance web research + honest taxonomy, personal quotes flagged → Task 3, Task 8 Ingest step 2.
- Propose-then-ask routing → Task 8 Ingest step 4 ("WAIT for the user").
- Seed from essay, all Spanish → Tasks 5, 6, 7.
- Notes by stable slug, numbered only on export → anchor map, Tasks 5/6, Task 8 Export.
- Export step → Task 8 Export, verified conceptually in Task 9.
- Packaged as skill `principios-wiki` → Task 8.
- Voice guide → Task 2, referenced by Task 8 Compile.
- Query and Lint operations → Task 8.

**Placeholder scan:** No TBD/TODO. Seed prose gives one fully-worked example (Task 5) plus explicit maps for the rest; this is intentional since the source file is the verbatim origin and reproducing all 24KB inline would be error-prone. All templates and SKILL.md content are given verbatim.

**Type consistency:** Anchor slugs are defined once in the anchor map and reused verbatim in Tasks 5, 6, 9. Operation names (Ingest/Query/Lint/Export) and file paths are consistent across Tasks 8 and the spec.
```
