---
id: "na_decision_usar_pimono"
type: "nota_atomica"
category: "decision"
extracted_from: "chat_2026_04_10_001"
tags:
  - arquitectura-ai
  - pimono
  - decision-tecnica
date_extracted: "2026-04-10"
confidence: "alta"
---

# Decisión: Usar Pimono como Motor de Agentes

Se decidió usar [[Pimono]] (de Mario Zechner) en lugar de [[LangGraph]] como motor de agentes del [[Cerebro Fractal]].

**Razón:** Pimono maneja internamente los ciclos ReAct. LangGraph orquestaría externamente lo mismo, generando redundancia.

**Consecuencia:** [[LangChain]] se usa solo como caja de herramientas (Document Loaders, Parsers), no como framework principal.

---
*Nota atómica extraída automáticamente de [[chat_2026_04_10_001]]*
