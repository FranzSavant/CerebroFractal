---
title: "Guía de Setup de Neo4j"
layer: 4
created: "2026-04-10"
---

# 🔧 Setup de Neo4j para Cerebro Fractal

## Opción A: Neo4j Desktop (Recomendado para desarrollo)

1. Descargar de https://neo4j.com/download/
2. Instalar y crear un nuevo proyecto
3. Crear una base de datos local
4. Configurar credenciales:
   - Usuario: `neo4j`
   - Password: `cerebrofractal`
5. Puerto por defecto: `bolt://localhost:7687`

## Opción B: Neo4j Aura Free (Cloud)

1. Ir a https://neo4j.com/cloud/aura-free/
2. Crear cuenta gratuita
3. Crear una instancia Free Tier
4. Anotar URI, usuario y password
5. Actualizar `src/mirror_pipeline/config.py` con las credenciales

## Opción C: Docker (Para los que ya tienen Docker)

```bash
docker run \
  --name cerebro-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/cerebrofractal \
  -v $HOME/neo4j/data:/data \
  neo4j:community
```

## Verificar conexión

Acceder a: http://localhost:7474
- Ingresar con neo4j / cerebrofractal
- Ejecutar: `RETURN 1` para verificar

## Después del setup

1. Actualizar credenciales en `src/mirror_pipeline/config.py`
2. Ejecutar: `cd src/mirror_pipeline && pip install -r requirements.txt`
3. Ejecutar: `python mirror_pipeline.py --sync` (primera sincronización)
4. Ejecutar: `python mirror_pipeline.py` (modo watch continuo)

## Índices recomendados (ejecutar en Neo4j Browser)

```cypher
CREATE INDEX idx_nombre IF NOT EXISTS FOR (n:Nota) ON (n.nombre);
CREATE INDEX idx_chat_id IF NOT EXISTS FOR (n:Chat) ON (n.nombre);
CREATE INDEX idx_tag_nombre IF NOT EXISTS FOR (n:Tag) ON (n.nombre);
CREATE INDEX idx_nota_atomica IF NOT EXISTS FOR (n:NotaAtomica) ON (n.nombre);
```
