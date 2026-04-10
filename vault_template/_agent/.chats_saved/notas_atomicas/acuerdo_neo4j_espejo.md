---
id: "na_acuerdo_neo4j_espejo"
type: "nota_atomica"
category: "acuerdo"
extracted_from: "chat_2026_04_10_001"
tags:
  - arquitectura-ai
  - neo4j
  - decision-tecnica
date_extracted: "2026-04-10"
confidence: "alta"
---

# Acuerdo: Neo4j como Espejo, no como Almacenamiento Primario

Se acordó que [[Neo4j]] funciona como **espejo de lectura** de la bóveda [[Obsidian]], nunca como almacenamiento primario.

**Principio:** Si Neo4j muere, se reconstruye desde los archivos `.md`. La bóveda es la Source of Truth.

**Implicaciones:**
- La sincronización es **unidireccional**: Obsidian → Neo4j
- Los agentes **leen** del grafo pero **escriben** en Obsidian
- Se necesita un mirror_pipeline robusto (watchdog + parser + neo4j driver)

---
*Nota atómica extraída automáticamente de [[chat_2026_04_10_001]]*
