---
project: "CerebroFractal"
type: "navigation-index"
---

# Índice de Navegación

## Archivos de entrada (cargar según necesidad)

| Archivo | Cuándo cargar |
|---------|---------------|
| `SESION_ACTUAL.md` | **SIEMPRE** — al iniciar cada día, carga este único archivo |
| `README.md` | Cuando necesites entender estructura general del proyecto |
| `INDEX.md` | Cuando necesites buscar algo específico entre sesiones |

## Historial de sesiones

| Sesión | Tema | Estado | Layer | Notas rápidas |
|--------|------|--------|-------|---------------|
| 2026-04-10.02 | metadatos-navegacion | active | — | Definiendo sistema de metadatos |
| 2026-04-10.01 | setup-inicial | done | 5 | Estructura base + docs creados |

## Búsqueda por anclajes

### Decisiones importantes
- Usar Pimono en vez de LangGraph → `sesion_2026_04_10.md` [decision]
- Neo4j como ESPEJO, Obsidian como fuente → `sesion_2026_04_10.md` [decision]
- Metadatos YAML para navegación → `SESION_ACTUAL.md` [decision]

### Código implementado
- mirror_pipeline.py → `sesion_2026_04_10.md` [codigo]
- Estructura vault_template/ → `sesion_2026_04_10.md` [codigo]

## Documentación de arquitectura (docs/)

| Archivo | Contenido |
|---------|-----------|
| 00_vision_general.md | Arquitectura completa 5 capas |
| 01_capa5_boveda_humana.md | Especificación Capa 5 (Obsidian) |
| 02_capa4_espejo_neo4j.md | Especificación Capa 4 (Neo4j) |
| 03_capa3_multi_llm_hub.md | Especificación Capa 3 (LiteLLM) |
| 04_capa2_orquestacion.md | Especificación Capa 2 (Agentes) |
| 05_capa1_dashboard.md | Especificación Capa 1 (Next.js) |
| decisiones_tecnicas.md | Log de decisiones técnicas |
