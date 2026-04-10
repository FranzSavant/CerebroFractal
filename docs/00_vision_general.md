---
title: "Cerebro Fractal — Visión General"
layer: "all"
created: "2026-04-10"
status: "Definido"
---

# 🧠 Cerebro Fractal — Visión General

## Filosofía Central

> **El humano posee los archivos, la máquina navega el grafo, y ambos mundos se sincronizan automáticamente.**

## Las 5 Capas

| Capa | Nombre | Responsabilidad | Tech Principal |
|------|--------|-----------------|----------------|
| 5 | Bóveda Humana | Almacenamiento en Markdown (Source of Truth) | Obsidian |
| 4 | Espejo de Inteligencia | Grafo de conocimiento navegable por agentes | Neo4j |
| 3 | El Intelecto | Modelos de lenguaje intercambiables | LiteLLM |
| 2 | El Director | Orquestación de agentes autónomos | Pimono (Pi) |
| 1 | Tablero de Operaciones | Interfaz visual del usuario | Next.js + React Flow |

## Flujo de datos

```
Usuario → [Capa 1: Dashboard] → [Capa 2: Pimono] → [Capa 4: Neo4j] → contexto
                                                   → [Capa 3: LLM] → respuesta
                                                   → [Capa 5: Obsidian] → persistencia
                                                   → [Capa 4: Neo4j] → espejeo automático
```

## Problemas que resuelve

1. **Amnesia de LLMs** → Memoria eterna vía grafo
2. **Desperdicio de tokens** → micro_chats + GraphRAG (-90% tokens)
3. **Asistentes genéricos** → Perfil profundo fractalizado
4. **Vendor lock-in** → Modelos intercambiables vía LiteLLM
5. **Opacidad del razonamiento** → Dashboard con visualización en tiempo real

## Orden de implementación

Capa 5 → Capa 4 → Capa 3 → Capa 2 → Capa 1

Ver cada documento de capa para detalle completo.
