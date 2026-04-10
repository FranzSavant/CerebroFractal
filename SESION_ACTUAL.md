---
session: "2026-04-10.02"
topic: "infraestructura-neo4j"
status: "active"
layer: 4
recovery_protocol: "github_auto"
github_remote: "https://github.com/FranzSavant/CerebroFractal.git"
last_checkpoint: "58826fa"
auto_verify: true
credential_persistence: "enabled"
---

## 🚨 PROTOCOLO DE ARRANQUE (ejecutar automáticamente al cargar)

### 1. Sincronizar con GitHub (automático, no pide credenciales)
git fetch origin
git log --oneline --graph --all -5

### 2. Verificar último checkpoint
# Debe coincidir con last_checkpoint arriba: [actualizar con último commit]

### Nota
Git está configurado con credential helper persistente (Windows Credential Manager).
Sobrevive reinicios. Ver archivo `.GIT_CONFIG` para detalles.

## Contexto de sesión
- ✅ Neo4j Aura Free creado y configurado
- ✅ Credenciales seguras en `.env` (ignorado por Git)
- ✅ GitHub conectado con credenciales persistentes
- Estrategia cloud: Aura Free (200k nodos) → VPS propio en el futuro

## Anclajes
- [decision] Neo4j Aura Free ahora, migrar a VPS cuando lleguemos a 150k nodos (DT-007)
- [infraestructura] Instancia Neo4j: d01e9743.databases.neo4j.io
- [infraestructura] Seguridad: `.env` en `.gitignore`, credenciales locales únicamente
- [config] Variables: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE
- [pendiente] Probar conexión con mirror_pipeline

## Última acción
Configurada instancia Neo4j Aura Free con credenciales seguras en `.env`.

## Siguiente acción pendiente
Probar conexión Neo4j desde Python e implementar mirror_pipeline.

---

## Nota de recuperación de emergencia
Si Git está roto: Ver archivo `.SESSION_STATE` (YAML legible).
Si todo está roto: Los archivos docs/ contienen las decisiones permanentes.
Credenciales Neo4j: Si se pierde `.env`, regenerar desde https://console.neo4j.io
