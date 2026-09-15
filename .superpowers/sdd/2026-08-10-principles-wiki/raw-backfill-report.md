# Raw backfill report

## Status
Complete. 33 raw source files created under `raw/`, one per note anchor in `wiki/notas.md`, each following the template at `.claude/skills/principios-wiki/references/raw-template.md` with all fields present (Fuente, Recogida, Bucket, Ancla de nota, Original, Traducción, Procedencia).

## Files created per theme
- raw/prefacio/: 4 (dalio, mahler-fuego, jtr, marco-aurelio-colmena)
- raw/ejecucion-sobre-intencion/: 5 (ford-vision, levenson-reloj, gregorio-antes, refran-actitud, welch-destino)
- raw/deber-antes-que-deseo/: 3 (jtr-deber, jtr-familia, jtr-puerta)
- raw/tiempo-y-legado/: 5 (recuerdo-manana, montagu-joven, franklin-sabios, refran-joven-viejo, felicidad-futuro)
- raw/cambio-y-tradicion/: 1 (heraclito-cambio)
- raw/conocerse-y-reflexion/: 3 (seneca-ensenar, jtr-escuchar, tretera-espacio)
- raw/como-te-perciben/: 3 (refran-juzgan, washington-demonios, ligia-felicidad)
- raw/palabra-y-silencio/: 2 (jtr-callar, refran-amo-callas)
- raw/el-foco/: 2 (refran-carbon-lena, refran-burra)
- raw/metodo/: 5 (marco-aurelio-correcto, mamet-duda, reagan-confia-verifica, loop-seis-pasos, camus-tipasa)

Total: 33 files.

## Verification summary
`find raw -type f -name "*.md" | wc -l` returns 33; a per-file grep confirmed every file contains all seven required fields (Fuente, Recogida, Bucket, Ancla de nota, ## Original, ## Traducción, ## Procedencia) with no gaps.

## Notes on non-trivial calls
- `dalio`: the essay only references the book title (no verbatim Dalio quote), so Original is set to "Principles" (the work cited as trigger, not a quote to endorse).
- `jtr` (prefacio): the anchor covers a biographical mention of the father, not a discrete aphorism, so Original holds the descriptive sentence from the essay rather than a maxim.
- `mahler-fuego` and `camus-tipasa`: both quoted in Spanish in the essay itself (French/German originals not given in-text), so per instructions Traducción is "—" and the Spanish text stands as Original.
- `reagan-confia-verifica`: Original is the Russian "Доверяй, но проверяй"; Traducción is "Confía, pero verifica," per instructions.
- `loop-seis-pasos`: bucket JATR; Original uses the author's own six-step labels (SENSE/FRAME/HYPOTHESIZE/BUILD/TEST/DELIVER) referenced in note 32, since the essay doesn't render a single quotable sentence for this anchor.

## Concerns
None. All 33 anchors in `wiki/notas.md` have a matching raw file, all buckets match the assignment given, and Recogida is 2026-08-10 throughout. No commits were made (git untouched per instructions).
