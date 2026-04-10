---
session: "2026-04-10.02"
topic: "arquitectura-cloud"
status: "active"
layer: 4
---

## Contexto
- Definida estrategia cloud para toda la vida del proyecto (10+ años)
- Decisión: Neo4j Aura Free → VPS Hetzner (escalado gradual $0→$5→$10)
- Estrategia datos híbridos: metadatos en grafo, contenido en Google Drive
- Documentado en docs/decisiones_tecnicas.md (DT-007) y docs/02_capa4_espejo_neo4j.md

## Anclajes
- [decision] Neo4j Aura Free ahora, migrar a VPS en 6-12 meses (DT-007)
- [decision] Solo metadatos en grafo (~500 bytes/nota), contenido en Drive
- [codigo] Mirror pipeline debe usar variables de entorno para fácil migración
- [infraestructura] VPS Hetzner CX21 ($5.39/mes) como destino final

## Última acción (1 línea)
Documentada estrategia de infraestructura a largo plazo en docs/.

## Siguiente acción pendiente
Crear cuenta Neo4j Aura Free y configurar instancia inicial.
