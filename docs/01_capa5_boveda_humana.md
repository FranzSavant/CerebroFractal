---
title: "Capa 5 — La Bóveda Humana (Source of Truth)"
layer: 5
created: "2026-04-10"
status: "Implementado (template)"
technologies:
  - Obsidian
  - Markdown
  - YAML frontmatter
related_files:
  - "../vault_template/_agent/"
---

# 📂 Capa 5 — La Bóveda Humana

## Propósito

Suelo sagrado del sistema. Todo el conocimiento vive en formato Markdown (.md), legible por humanos, editable a mano, propiedad absoluta del usuario. Es la **Única Fuente de Verdad**.

- Los agentes **escriben** sus resultados aquí (carpetas `Outputs`)
- Los agentes **NO leen** directamente de aquí para operar (usan Capa 4)
- Si todo el sistema muere, los archivos .md siguen legibles

## Estructura Fractal

```
_agent/
├── Atlas/               # Hub transversal
│   ├── Agentes/
│   ├── Herramientas/
│   └── Ideas/
├── Career/              # Dominio profesional
│   ├── Activos/
│   ├── Agentes/
│   │   └── PublicadorVisualAcelerado/
│   │       └── FineTuning/
│   │           └── GymMillennium/
│   │               └── Outputs/
│   └── Recursos/
├── FinancialLife/
├── Parenting/
├── LoveRelationship/
├── Character/
├── LifeVision/
└── IntellectualLife/
```

## Sistema Padre-Hijo de Chats

### `.chats_saved/` — Estructura

```
.chats_saved/
├── chat_XXXX.md              # PADRE: Conversación completa (lectura humana)
├── micro_chats/
│   └── micro_XXXX.md         # HIJO: Resumen ultracomprimido (bootstrap IA)
└── notas_atomicas/
    └── *.md                   # Átomos de conocimiento extraídos
```

### Reglas clave

| Archivo | ¿Lo lee la IA? | ¿Se espejea en Neo4j? | Tokens |
|---------|----------------|----------------------|--------|
| Padre (chat_*.md) | NO | SÍ | 0 |
| Hijo (micro_*.md) | SÍ (solo bootstrap) | NO | 100-300 |
| Notas Atómicas | Indirectamente (vía Neo4j) | SÍ | N/A |

### Proceso de Guardado ("Consolidar Conocimiento")

1. Dump del Padre → `.chats_saved/chat_XXXX.md`
2. LLM genera Hijo → `.chats_saved/micro_chats/micro_XXXX.md`
3. LLM extrae Notas Atómicas → `.chats_saved/notas_atomicas/`
4. Script espejo actualiza Neo4j (Padre + Notas Atómicas, NO Hijo)

## Implementación

Template creado en: `vault_template/_agent/`

Ver archivos de ejemplo en esa carpeta.
