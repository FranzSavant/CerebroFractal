---
title: "Capa 4 — El Espejo de Inteligencia (Contextual Engine)"
layer: 4
created: "2026-04-10"
status: "Diseñado, código base creado"
technologies:
  - Neo4j
  - Python (watchdog, neo4j-driver)
  - LlamaIndex Property Graph Index
related_files:
  - "../src/mirror_pipeline/"
  - "../config/neo4j/"
---

# 🪞 Capa 4 — El Espejo de Inteligencia

## Propósito

Mundo de la máquina. Copia espejo refinada de la Capa 5, optimizada para navegación por agentes. Los agentes **leen** de aquí, **nunca** escriben aquí directamente.

**Neo4j NO es almacenamiento primario.** Si se corrompe, se reconstruye desde Obsidian.

## Neo4j — Estructura de Nodos

```cypher
(:Persona {nombre, rol, ...})
(:Lugar {nombre, ...})
(:Evento {nombre, fecha, ...})
(:Idea {nombre, estado, ...})
(:Chat {id, fecha, ...})
(:NotaAtomica {nombre, tipo, ...})
(:Nota {nombre, carpeta, tags, ...})
```

## Relaciones de ejemplo

```cypher
(Wilmer)-[:IMPARTE]->(ClaseBaile)
(ClaseBaile)-[:OCURRE_EN]->(GymMillennium)
(CerebroFractal)-[:NACIO_EN]->(Chat_001)
(Chat_001)-[:GENERO]->(NotaAtomica_Pimono)
(Nota_A)-[:MENCIONA]->(Nota_B)
```

## Mirror Pipeline — El puente automático

### Tecnologías
- **watchdog**: Monitorea cambios en sistema de archivos
- **mistune/markdown-it**: Parsea Markdown → estructura de datos
- **neo4j (Python driver)**: Escribe en Neo4j vía Cypher

### Flujo
1. `watchdog` detecta cambio en archivo .md
2. Parser extrae: título, tags, wikilinks, frontmatter
3. Driver ejecuta MERGE en Neo4j (nodos + relaciones)
4. Grafo actualizado

### Reglas de Espejeo

| Tipo de Archivo | ¿Se espejea? | Razón |
|---|---|---|
| Notas regulares `*.md` | ✅ SÍ | Conocimiento base |
| Outputs de Agentes | ✅ SÍ | Entregables que enriquecen grafo |
| Chats Padre | ✅ SÍ | Eventos de conocimiento |
| Chats Hijo (micro_chats) | ❌ NO | Solo operativos para bootstrap |
| Notas Atómicas | ✅ SÍ | Átomos de conocimiento puro |
| Config/SKILL.md | ❌ NO | Instrucciones, no conocimiento |

## LlamaIndex Property Graph Index

Capa de abstracción entre agentes y Neo4j. Traduce preguntas en lenguaje natural a consultas Cypher optimizadas.

## Infraestructura y Escalado

### Fase 1: Prototipado (Neo4j Aura Free)
- **Costo:** $0
- **Límite:** 200k nodos
- **Uso:** Metadatos únicamente (títulos, tags, relaciones, fechas)
- **Tiempo estimado:** 6-12 meses para alcanzar límite (si es solo metadata)

### Fase 2: Migración (VPS Hetzner)
- **Trigger:** 150k nodos (alerta automática)
- **VPS:** Hetzner CX21 ($5.39/mes, 4GB RAM)
- **Neo4j:** Community Edition (ilimitado nodos)
- **Migración:** Dump de Aura → Import a VPS (1 fin de semana)

### Fase 3: Escalado (Años siguientes)
- VPS crece: $5 → $9 → $14 → $20/mes según RAM
- Neo4j CE sigue siendo gratis
- Backups automáticos a Google Drive

## Estrategia de Datos Híbridos

**Error común:** Meter TODO el contenido en el grafo.
**Solución:** Separar concerns.

| Dato | Almacenamiento | Razón |
|------|----------------|-------|
| Título de nota | Neo4j | Navegación rápida |
| Tags | Neo4j | Filtrado y búsqueda |
| Relaciones `[[link]]` | Neo4j | Grafo navegable |
| Fechas | Neo4j | Timeline y queries temporales |
| Contenido Markdown | Google Drive | Ya tienes 2TB, versionado nativo |
| Imágenes/Adjuntos | Google Drive | No meter binarios en grafo |

**Ejemplo práctico:**
- Nodo en Neo4j: `(n:Nota {titulo: "Reunión Juan", tags: ["work"], drive_id: "abc123"})`
- Contenido completo: Archivo en Drive accesible vía `drive_id`

**Cálculo:** 200k notas × 500 bytes metadata = 100MB. Cabe en cualquier instancia.

## Código fuente

Ver: `src/mirror_pipeline/`

**Nota migración:** El código usa variables de entorno para URI/credentials. Cambiar de Aura a VPS = cambiar `.env`, sin tocar código.
