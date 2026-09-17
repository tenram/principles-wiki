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
