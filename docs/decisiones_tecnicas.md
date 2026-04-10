---
title: "Log de Decisiones Técnicas"
created: "2026-04-10"
last_updated: "2026-04-10"
---

## DT-007: Neo4j Aura Free → VPS (Estrategia de Vida)

- **Fecha:** 2026-04-10
- **Decisión:** Empezar con Neo4j Aura Free (200k nodos, $0). Migrar a VPS propio con Neo4j Community Edition cuando se acerque el límite.
- **Razonamiento:** Aura Free tiene salto brusco de $0 a $65/mes. Un VPS (Hetzner CX21: $5.39/mes) con Neo4j CE es ilimitado en nodos, solo limitado por RAM. A 10 años ahorra $2,670+.
- **Plan de Migración:**
  - **Fase 1 (ahora):** Aura Free. Solo metadatos en grafo (títulos, tags, relaciones), contenido completo en Google Drive.
  - **Fase 2 (150k nodos):** Comprar VPS Hetzner CX21 ($5.39/mes), instalar Neo4j CE, migrar dump.
  - **Fase 3 (escalado):** Subir de VPS ($5→$9→$14→$20) según necesidad de RAM.
- **Estrategia de Datos Híbridos:**
  - **Neo4j (grafo):** Solo metadatos (~500 bytes/nota). 200k notas = 100MB.
  - **Google Drive (archivos):** Contenido Markdown completo, imágenes, adjuntos.
- **Consecuencia:** El código debe usar abstracción de conexión (URI/credentials externos) para permitir migración sin cambios en lógica de negocio.

# 📝 Log de Decisiones Técnicas

Cada decisión importante del proyecto se registra aquí con su contexto y razonamiento.

---

## DT-001: Pimono sobre LangGraph

- **Fecha:** 2026-04-10
- **Decisión:** Usar Pimono (Pi, Mario Zechner) como motor de agentes en lugar de LangGraph
- **Razonamiento:** Pimono maneja internamente ciclos ReAct. LangGraph orquestaría externamente lo mismo → redundancia. Dos directores para un volante.
- **Consecuencia:** LangChain se usa solo como "caja de herramientas" (Document Loaders, Parsers, etc.), no como framework principal.

---

## DT-002: Neo4j como espejo, no como almacenamiento primario

- **Fecha:** 2026-04-10
- **Decisión:** Neo4j refleja Obsidian, nunca al revés. Obsidian es Source of Truth.
- **Razonamiento:** Si Neo4j muere, se reconstruye desde los .md. Los archivos Markdown son legibles sin software especial. Evita dependencia de base de datos propietaria.
- **Consecuencia:** Se necesita mirror_pipeline robusto. Sincronización es unidireccional (Obsidian → Neo4j).

---

## DT-003: Guardado manual de chats (no automático)

- **Fecha:** 2026-04-10
- **Decisión:** Solo se guardan chats cuando el usuario presiona "Consolidar Conocimiento"
- **Razonamiento:** Evita que el sistema se llene de conversaciones triviales/de prueba. El usuario decide qué es valioso.
- **Consecuencia:** Se necesita botón claro en Dashboard. El usuario debe formar el hábito de consolidar.

---

## DT-004: Micro_chats NO se espejean en Neo4j

- **Fecha:** 2026-04-10
- **Decisión:** Los archivos hijo (micro_chats) son puramente operativos, no se reflejan en el grafo.
- **Razonamiento:** Son resúmenes de bootstrap para retomar conversaciones. El conocimiento "real" está en las Notas Atómicas (que sí se espejean).
- **Consecuencia:** El grafo se mantiene limpio. Los micro_chats son efímeros/operativos.

---

## DT-005: LiteLLM como router de modelos

- **Fecha:** 2026-04-10
- **Decisión:** Usar LiteLLM para abstraer todos los providers de LLM bajo interfaz unificada.
- **Razonamiento:** Elimina vendor lock-in. Cambiar de Gemini a GPT a Claude requiere cambiar un string de configuración, no reescribir código.
- **Consecuencia:** Toda llamada a LLM pasa por LiteLLM. Se puede implementar routing inteligente por tipo de tarea.

---

## DT-006: Implementación bottom-up (Capa 5 → Capa 1)

- **Fecha:** 2026-04-10
- **Decisión:** Construir desde la base (estructura de archivos) hacia arriba (dashboard).
- **Razonamiento:** Cada capa depende de la anterior. No puedes visualizar un grafo que no existe. No puedes orquestar agentes sin LLMs configurados.
- **Consecuencia:** Las primeras sesiones serán menos "visuales" pero construyen cimientos sólidos.
