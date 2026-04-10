---
session: "2026-04-10.02"
topic: "arquitectura-cloud"
status: "active"
layer: 4
recovery_protocol: "github_auto"
github_remote: "https://github.com/FranzSavant/CerebroFractal.git"
last_checkpoint: "425ae44"
auto_verify: true
credential_persistence: "enabled"
---

## 🚨 PROTOCOLO DE ARRANQUE (ejecutar automáticamente al cargar)

### 1. Sincronizar con GitHub (automático, no pide credenciales)
git fetch origin
git log --oneline --graph --all -5

### 2. Verificar último checkpoint
# Debe coincidir con last_checkpoint arriba: 425ae44 (o más reciente)

### Nota
Git está configurado con credential helper persistente (Windows Credential Manager).
Sobrevive reinicios. Ver archivo `.GIT_CONFIG` para detalles.

## Contexto de sesión
- Estrategia cloud definida (Aura Free → VPS)
- Sistema robusto: Git + GitHub + .SESSION_STATE
- ✅ GitHub configurado: https://github.com/FranzSavant/CerebroFractal
- ✅ Credenciales persistentes (sobrevive reinicios)
- Persistencia permanente activada

## Anclajes
- [decision] Neo4j Aura Free ahora, migrar a VPS en 6-12 meses (DT-007)
- [infraestructura] GitHub conectado con credenciales persistentes
- [sistema] Protocolo auto-verificación implementado
- [config] Ver .GIT_CONFIG para configuración de credenciales

## Última acción
Configuradas credenciales Git persistentes que sobreviven reinicios.

## Siguiente acción pendiente
Crear cuenta Neo4j Aura Free.

---

## Nota de recuperación de emergencia
Si Git está roto: Ver archivo `.SESSION_STATE` (YAML legible).
Si todo está roto: Los archivos docs/ contienen las decisiones permanentes.
