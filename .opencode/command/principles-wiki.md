---
description: Ingesta una cita nueva al wiki de principios de mí.
---

Carga el skill `principios-wiki` y ejecuta su flujo de **Ingest (primary)** con la siguiente cita y pista de atribución:

$ARGUMENTS

Sigue el procedimiento del skill paso a paso: parsea la cita, clasifica la procedencia, captura a `raw/<tema>/`, propón el principio de mejor encaje y espera mi decisión antes de escribir en `wiki/`. Al compilar, sigue `references/voice-guide.md`. Al terminar, actualiza `wiki/index.md` y anota en `wiki/log.md`.