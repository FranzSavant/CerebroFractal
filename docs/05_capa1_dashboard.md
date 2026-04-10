---
title: "Capa 1 — El Tablero de Operaciones (Dashboard)"
layer: 1
created: "2026-04-10"
status: "Diseñado"
technologies:
  - Next.js
  - React Flow
  - Socket.io
  - react-markdown
  - Prism.js
related_files:
  - "../src/dashboard/"
---

# 🖥️ Capa 1 — El Tablero de Operaciones

## Propósito

Lobby del sistema. Interfaz visual. No toma decisiones, no procesa datos, no almacena nada permanente. Solo **muestra** y **recibe órdenes**.

## Componentes

### 1. Chat Principal
- Interfaz conversacional (texto + potencialmente voz + drag-and-drop)
- **Botón "Consolidar Conocimiento"**: Gatillo para guardar chat (Padre+Hijo+Atómicas)
- **Botón "Retomar Conversación"**: Carga Padre (visual) + Hijo (contexto LLM)

### 2. Radar de Atención (Context Mini-Map)
- Visualización miniatura del grafo Neo4j
- Nodos consultados se iluminan en tiempo real
- Sensación espacial de dónde opera la IA

### 3. Consola de Cadena de Pensamiento
- Panel estilo terminal con razonamiento interno del agente
- Transparencia total del proceso ReAct
- Permite intervención HITL si se detecta error

### 4. Selector de Personas
- Menú visual para cambiar rol del agente
- Al cambiar, esquema de colores del Dashboard cambia
- Arquitecto=azul, Creativo=naranja, Finanzas=verde, Reflexivo=púrpura

### 5. Centro de Métricas
- Costo de API (hoy/semana/mes)
- Crecimiento de la red (nodos/relaciones nuevas)
- Tiempo ahorrado estimado

### 6. Historial de Chats
- Barra lateral listando chats en `.chats_saved/`
- Costo de tokens: CERO (renderizado local de Markdown)
- Botón "Retomar" en cada chat

### 7. Interfaz de Voz (Dual Voice Hub)

#### Modo A: Push-to-Talk (Comandos)
- Audio se procesa en bloque (STT) → texto en chat
- Ideal para órdenes puntuales

#### Modo B: Streaming (Conversación fluida)
- **STT**: Fennec (~$0.16/hora)
- **TTS**: Inworld TTS (~$0.10-0.15/hora)
- **LLM**: Qwen2.5-72B o Qwen3-235B vía Baseten
- **Latencia**: 600-800ms
- **Costo total**: ~$0.25-0.35/hora

### 8. Dropzone Multimodal
- Drag-and-drop de imágenes, PDFs, audios
- LLM multimodal los analiza automáticamente

### 9. Time Travel Bar
- Slider temporal para "retroceder" en la sesión
- Grafo muestra estado de cualquier momento pasado

### 10. Galería de Artefactos
- Últimos Outputs generados por agentes
- Miniaturas visuales, click para ver en visor Markdown

## Comunicación en Tiempo Real (Socket.io)

| Evento | Significado | Visual |
|---|---|---|
| `agent:thinking` | Procesando | Nodo palpita azul |
| `agent:querying_graph` | Consultando Neo4j | Nodos del grafo se iluminan |
| `agent:responding` | Escribiendo respuesta | Texto fluye en panel |
| `agent:writing_output` | Creando archivo en Obsidian | Notificación |
| `agent:paused` | HITL activado | Panel intervención se abre |

## Pendiente

- [ ] Crear proyecto Next.js
- [ ] Implementar cada componente (ver lista arriba)
- [ ] Conectar con backend via Socket.io
- [ ] Diseñar theme system (colores por persona)
