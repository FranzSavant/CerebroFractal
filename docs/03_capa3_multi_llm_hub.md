---
title: "Capa 3 — El Intelecto (Multi-LLM Hub)"
layer: 3
created: "2026-04-10"
status: "Diseñado"
technologies:
  - LiteLLM
  - APIs de LLMs (Gemini, GPT, Claude, Llama, Mistral)
related_files:
  - "../config/litellm/"
---

# 🧠 Capa 3 — El Intelecto

## Propósito

El "IQ" del sistema. Capa completamente **agnóstica al modelo**. Hoy Gemini, mañana GPT-5, pasado un modelo local. El sistema no depende de ningún proveedor.

## LiteLLM (Router de Modelos)

Librería open source que unifica APIs de +100 modelos bajo interfaz OpenAI-compatible.

```python
from litellm import completion

# Pimono hace UNA llamada, LiteLLM enruta al modelo configurado
response = completion(
    model="gemini/gemini-2.5-pro",  # o "gpt-4o", "claude-3-opus", etc.
    messages=[{"role": "user", "content": "..."}]
)
```

## Modelos y casos de uso

| Modelo | Fortaleza | Caso de uso |
|---|---|---|
| Gemini | Multimodal, contexto masivo | Audios, imágenes del Gym |
| GPT | Razonamiento, código | Orquestación, análisis financiero |
| Claude | Escritura de calidad | Redacción, análisis con matices |
| Llama | Gratis, local, privado | Datos sensibles, experimentación |
| Mistral | Eficiente, barato | Tareas simples frecuentes |

## Gestión de costos

- **Tracking**: Cada llamada registra modelo, tokens in/out, costo, timestamp
- **Visualización**: Widget en Dashboard (Capa 1)
- **Optimización**: micro_chats + GraphRAG = -90% tokens vs historiales brutos

## Reglas de enrutamiento (ejemplo)

```yaml
routing_rules:
  creative_tasks: "claude-3-opus"
  data_analysis: "gemini-2.5-pro"
  simple_queries: "mistral-small"
  sensitive_data: "llama-3-local"
  default: "gemini-2.5-flash"
```

## Pendiente

- [ ] Instalar LiteLLM
- [ ] Configurar al menos 2 providers
- [ ] Implementar logging de tokens/costos
- [ ] Crear reglas de enrutamiento
