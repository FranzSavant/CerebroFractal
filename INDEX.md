---
project: "CerebroFractal"
type: "navigation-index"
last_updated: "2026-04-10"
---

# Índice de Navegación

**AI del futuro:** Leer `.PI_PROTOCOL` primero antes de cualquier otra cosa.

## Archivos de entrada (cargar según necesidad)

| Archivo | Cuándo cargar | Prioridad |
|---------|---------------|-----------|
| `.PI_PROTOCOL` | **SIEMPRE PRIMERO** — Reglas de interacción | 🔴 Crítica |
| `SESION_ACTUAL.md` | Después de .PI_PROTOCOL — Estado actual | 🟢 Diaria |
| `README.md` | Cuando necesites entender estructura general | 🟡 Referencia |
| `INDEX.md` | Cuando busques algo entre sesiones históricas | 🟡 Referencia |

## Historial de sesiones

| Sesión | Tema | Estado | Layer | Notas rápidas |
|--------|------|--------|-------|---------------|
| 2026-04-10.02 | setup-completo | done | 4 | GitHub, Neo4j Aura, protocolo AI |
| 2026-04-10.01 | setup-inicial | done | 5 | Estructura base + docs |

## Búsqueda por anclajes

### Decisiones importantes
- Usar Pimono en vez de LangGraph → `sesion_2026_04_10_01.md` [decision]
- Neo4j como ESPEJO, Obsidian como fuente → `sesion_2026_04_10_01.md` [decision]
- Estructura metadatos YAML para navegación → `sesion_2026_04_10_02.md` [decision]
- AI documenta automáticamente sin pedir permiso → `sesion_2026_04_10_02.md` [decision]
- Neo4j Aura Free → VPS cuando 150k nodos → `docs/decisiones_tecnicas.md` DT-007

### Código implementado
- mirror_pipeline.py → `sesion_2026_04_10_01.md` [codigo]
- Estructura vault_template/ → `sesion_2026_04_10_01.md` [codigo]

### Infraestructura
- GitHub configurado → `sesion_2026_04_10_02.md` [infraestructura]
- Neo4j Aura Free → `sesion_2026_04_10_02.md` [infraestructura]
- Credenciales persistentes → `sesion_2026_04_10_02.md` [config]

## Documentación de arquitectura (docs/)

| Archivo | Contenido |
|---------|-----------|
| 00_vision_general.md | Arquitectura completa 5 capas |
| 01_capa5_boveda_humana.md | Especificación Capa 5 (Obsidian) |
| 02_capa4_espejo_neo4j.md | Especificación Capa 4 (Neo4j) + estrategia migración |
| 03_capa3_multi_llm_hub.md | Especificación Capa 3 (LiteLLM) |
| 04_capa2_orquestacion.md | Especificación Capa 2 (Agentes) |
| 05_capa1_dashboard.md | Especificación Capa 1 (Next.js) |
| decisiones_tecnicas.md | Log de decisiones técnicas (DT-001 a DT-007) |

## Configuración importante

| Archivo | Propósito |
|---------|-----------|
| .PI_PROTOCOL | Reglas de interacción AI-usuario |
| .GIT_CONFIG | Configuración credenciales persistentes |
| .env | Credenciales locales (NUNCA subir a GitHub) |
| .env.example | Template de credenciales (sí subir) |
