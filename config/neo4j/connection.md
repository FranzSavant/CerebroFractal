---
type: "config"
layer: 4
service: "neo4j"
status: "active"
---

# Configuración de Conexión Neo4j Aura

## Estado Actual
✅ Instancia Aura Free creada y configurada
✅ Credenciales almacenadas en `.env` (ignorado por Git)
✅ Archivo de ejemplo `.env.example` disponible

## Variables de Entorno

Las credenciales se leen desde archivo `.env` en raíz:

```bash
NEO4J_URI=neo4j+s://d01e9743.databases.neo4j.io
NEO4J_USERNAME=d01e9743
NEO4J_PASSWORD=[ver archivo .env local]
NEO4J_DATABASE=neo4j
```

## Seguridad

- ⚠️ **`.env` está en `.gitignore`** — nunca se sube a GitHub
- ⚠️ **Las credenciales reales solo existen en tu máquina local**
- ✅ **Backup:** Si pierdes `.env`, puedes regenerar credenciales desde https://console.neo4j.io

## Conexión desde Python

```python
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)
```

## Límites de Aura Free

- **Nodos:** 200,000
- **Relaciones:** Ilimitadas (dentro del límite de RAM)
- **Almacenamiento:** 1GB
- **Costo:** $0

## Próximos Pasos

1. Instalar dependencias: `pip install neo4j python-dotenv`
2. Probar conexión con script de verificación
3. Implementar mirror_pipeline para sincronizar Obsidian → Neo4j
