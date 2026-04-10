---
project: "CerebroFractal"
type: "project-master"
created: "2026-04-10"
last_updated: "2026-04-10"
---

# 🧠 Cerebro Fractal

**Arquitectura de IA Personal con Memoria Grafada**

## 🚨 INSTRUCCIONES PARA LA AI (LEER PRIMERO)

**Antes de cualquier otra cosa, lee:**
1. `.PI_PROTOCOL` - Protocolo de interacción con el usuario
2. `SESION_ACTUAL.md` - Estado actual del proyecto
3. Ejecutar automáticamente: `git fetch origin && git log --oneline -5`

**Reglas fundamentales:**
- El usuario NO guarda nada manualmente
- El usuario NO ejecuta comandos git
- TÚ documentas, actualizas, y persistes automáticamente
- Ver `.PI_PROTOCOL` para checklist completo

---

## 🚀 Cómo retomar el trabajo (IMPORTANTE)

**Mañana cuando abras pi:**

1. **Carga ÚNICAMENTE este archivo:** `SESION_ACTUAL.md`
2. Lee el YAML frontmatter (3 líneas) + Contexto (4 bullets máx)
3. Ahí está todo lo que necesitas para continuar sin pérdida de contexto
4. **NO** preguntes "¿qué hacemos?" - Lee "Siguiente acción pendiente" y procede

**Si necesitas buscar algo específico de sesiones pasadas:**
- Abre `INDEX.md` — tabla de sesiones con temas y anclajes

---

## 📁 Estructura del proyecto

```
CerebroFractal/
├── README.md                 # Este archivo
├── .PI_PROTOCOL              # ← AI: LEER ESTO PRIMERO SIEMPRE
├── SESION_ACTUAL.md          # ← CARGAR ESTO AL INICIAR (working memory)
├── INDEX.md                  # Índice de sesiones históricas
├── .env                      # Credenciales locales (IGNORADO POR GIT)
├── .env.example              # Template de credenciales
├── .gitignore                # Asegura que .env no suba a GitHub
├── .GIT_CONFIG               # Configuración de credenciales persistentes
├── docs/                     # Documentación de arquitectura
│   ├── 00_vision_general.md
│   ├── 01_capa5_boveda_humana.md
│   ├── 02_capa4_espejo_neo4j.md
│   ├── 03_capa3_multi_llm_hub.md
│   ├── 04_capa2_orquestacion.md
│   ├── 05_capa1_dashboard.md
│   └── decisiones_tecnicas.md
├── sesiones/                 # Historial de sesiones
│   ├── _TEMPLATE.md          # Template para nuevas sesiones
│   └── sesion_YYYY_MM_DD.md  # Archivos de sesiones pasadas
├── src/                      # Código fuente
├── vault_template/           # Template Obsidian (Capa 5)
└── config/                   # Configuraciones
```

## 🏗️ Orden de implementación

1. **Capa 5** → Estructura de carpetas Obsidian (`vault_template/`)
2. **Capa 4** → Neo4j + Script espejo (`src/mirror_pipeline/`)
3. **Capa 3** → LiteLLM Hub (`config/litellm/`)
4. **Capa 2** → Motor de agentes (`src/backend/`)
5. **Capa 1** → Dashboard Next.js (`src/dashboard/`)

---

## Convenciones de metadatos

Todos los archivos `.md` usan YAML frontmatter mínimo:

```yaml
---
session: "YYYY-MM-DD.NN"    # ID único
topic: "nombre-tema"         # Para búsqueda rápida
status: "active"             # active | paused | done
layer: 0                     # 1-5 o null
---
```

**Anclajes dentro del contenido:**
- `[decision]` — Decisiones técnicas importantes
- `[codigo]` — Implementaciones o cambios de código
- `[bug]` — Problemas conocidos o blockers
- `[pendiente]` — Acciones futuras

**Secciones estándar:**
- `## Contexto` — Máximo 4 bullets, estado actual
- `## Anclajes` — Puntos de búsqueda rápida
- `## Última acción` — 1 línea, qué acabamos de hacer
- `## Siguiente acción pendiente` — Qué toca hacer

---

## Estado del proyecto

Ver `SESION_ACTUAL.md` para estado en tiempo real.
Resumen histórico en `INDEX.md`.

---

## Nota de seguridad

- **`.env`** contiene credenciales reales. NUNCA subir a GitHub.
- **`.env.example`** es el template seguro (se sube a GitHub).
- Si se pierde `.env`, regenerar credenciales desde el proveedor correspondiente.
