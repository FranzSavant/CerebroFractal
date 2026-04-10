"""
Configuración del Mirror Pipeline — Cerebro Fractal
Sincronización unidireccional: Obsidian → Neo4j
"""

from pathlib import Path

# ============================================
# RUTAS DE LA BÓVEDA
# ============================================

# Ruta raíz de la bóveda de Obsidian (ajustar a tu ruta real)
VAULT_ROOT = Path(r"C:\Users\Fran\Desktop\CerebroFractal\vault_template")

# Carpeta base del agente dentro de la bóveda
AGENT_ROOT = VAULT_ROOT / "_agent"

# Carpeta de chats guardados
CHATS_SAVED = AGENT_ROOT / ".chats_saved"
MICRO_CHATS = CHATS_SAVED / "micro_chats"
NOTAS_ATOMICAS = CHATS_SAVED / "notas_atomicas"

# ============================================
# NEO4J
# ============================================

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "cerebrofractal"  # Cambiar en producción
NEO4J_DATABASE = "neo4j"

# ============================================
# REGLAS DE ESPEJEO
# ============================================

# Patrones de archivos que SÍ se espejean en Neo4j
MIRROR_INCLUDE_PATTERNS = [
    "**/*.md",  # Todas las notas Markdown
]

# Patrones de archivos que NO se espejean
MIRROR_EXCLUDE_PATTERNS = [
    "**/micro_chats/**",      # Hijos de chats (solo operativos)
    "**/SKILL.md",            # Instrucciones para agentes
    "**/_templates/**",       # Templates
    "**/.obsidian/**",        # Config de Obsidian
]

# Extensiones a monitorear
WATCHED_EXTENSIONS = {".md"}

# ============================================
# LOGGING
# ============================================

LOG_LEVEL = "INFO"
LOG_FILE = Path(__file__).parent / "mirror_pipeline.log"
