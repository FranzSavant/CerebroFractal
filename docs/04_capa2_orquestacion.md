---
title: "Capa 2 — El Director (Orquestación de Agentes)"
layer: 2
created: "2026-04-10"
status: "Diseñado"
technologies:
  - "Pimono (Pi, Mario Zechner)"
  - FastAPI
  - LangChain (herramientas selectas)
  - LangSmith
related_files:
  - "../src/backend/"
---

# 🎭 Capa 2 — El Director

## Propósito

Carácter y voluntad del sistema. No sabe la respuesta, pero sabe **cómo llegar a la respuesta**. Director de orquesta que decide qué agente, qué datos, qué LLM.

## Pimono — Motor de Agentes

Framework de Mario Zechner. Paradigma **Pensamiento → Acción → Observación** (ReAct).

### Flujo de Pimono
1. Recibe instrucción del usuario (Capa 1)
2. Consulta grafo (Capa 4) para contexto
3. Decide herramientas a invocar
4. Envía petición al LLM (Capa 3)
5. Valida respuesta
6. Escribe resultado en Obsidian (Capa 5)

### ¿Por qué Pimono y no LangGraph?

Pimono maneja internamente los ciclos de razonamiento. Usar LangGraph sería redundante — dos directores para un mismo volante.

## Herramientas de LangChain (selectas)

| Herramienta | Finalidad |
|---|---|
| Document Loaders | Cargar PDFs, Google Docs, CSVs |
| Text Splitters | Dividir documentos largos en chunks |
| Tool Integrations | Gmail, Google Calendar, APIs |
| Output Parsers | Respuestas → JSON/YAML limpio |

## Sistema de Personas (Roles de Agente)

| Persona | Enfoque | Color Dashboard |
|---|---|---|
| 🏗️ Arquitecto | Procesos, diseño de sistemas | Azul |
| 🎨 Content Creator | Visual, copy, redes sociales | Naranja |
| 💰 Socio Financiero | Inversiones, presupuestos | Verde |
| 🧠 Reflexivo | Introspección, análisis emocional | Púrpura |

## HITL — Human-in-the-Loop

Protocolo que pausa al agente cuando:
- Baja confianza en siguiente paso
- Decisión irreversible
- Tarea sensible

Notifica al usuario en Capa 1 para aprobación.

## LangSmith — Observabilidad

Registra cada paso del razonamiento:
- Prompt enviado al LLM
- Respuesta recibida
- Tokens consumidos
- Estado del ciclo de razonamiento
- Errores o bucles infinitos

## Backend — FastAPI

Servidor Python que expone endpoints para la Capa 1:
- `POST /chat` — Enviar mensaje
- `POST /consolidate` — Consolidar conocimiento
- `GET /graph/context` — Obtener contexto del grafo
- `GET /agents/status` — Estado de agentes
- `WS /ws` — WebSocket para tiempo real

## Pendiente

- [ ] Configurar Pi como motor de agentes
- [ ] Crear primer agente funcional
- [ ] Implementar Agent Personas
- [ ] Implementar HITL
- [ ] Integrar LangSmith
- [ ] Crear backend FastAPI
