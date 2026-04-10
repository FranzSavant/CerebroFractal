"""
Mirror Pipeline — Cerebro Fractal
==================================
Sincronización unidireccional: Obsidian (.md) → Neo4j (grafo)

Monitorea la bóveda de Obsidian y espejea los cambios en Neo4j.
Extrae: título, tags, wikilinks, frontmatter → nodos y relaciones.

Uso:
    python mirror_pipeline.py          # Modo watch (monitoreo continuo)
    python mirror_pipeline.py --sync   # Sincronización completa una vez
"""

import re
import sys
import time
import yaml
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent
from neo4j import GraphDatabase

from config import (
    VAULT_ROOT, AGENT_ROOT, CHATS_SAVED, MICRO_CHATS,
    NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE,
    MIRROR_EXCLUDE_PATTERNS, WATCHED_EXTENSIONS,
    LOG_LEVEL, LOG_FILE,
)

# ============================================
# LOGGING
# ============================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("mirror_pipeline")


# ============================================
# DATA MODELS
# ============================================

@dataclass
class ParsedNote:
    """Resultado del parsing de un archivo .md"""
    filepath: Path
    title: str = ""
    frontmatter: dict = field(default_factory=dict)
    tags: list = field(default_factory=list)
    wikilinks: list = field(default_factory=list)
    node_type: str = "Nota"  # Nota, Chat, NotaAtomica, etc.
    content_preview: str = ""
    relative_path: str = ""


# ============================================
# MARKDOWN PARSER
# ============================================

class MarkdownParser:
    """Extrae metadatos estructurados de archivos Markdown de Obsidian."""

    # Regex para extraer frontmatter YAML (entre ---)
    FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)

    # Regex para extraer [[Wikilinks]] (con o sin alias)
    WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

    # Regex para extraer #tags inline
    INLINE_TAG_RE = re.compile(r"(?:^|\s)#([\w\-/]+)")

    # Regex para extraer título del primer heading
    HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)

    def parse(self, filepath: Path) -> Optional[ParsedNote]:
        """Parsea un archivo .md y retorna un ParsedNote o None si debe ignorarse."""
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Error leyendo {filepath}: {e}")
            return None

        # Verificar si debe excluirse
        if self._should_exclude(filepath):
            logger.debug(f"Excluido por reglas: {filepath}")
            return None

        note = ParsedNote(filepath=filepath)
        note.relative_path = str(filepath.relative_to(VAULT_ROOT))

        # Extraer frontmatter YAML
        fm_match = self.FRONTMATTER_RE.match(content)
        if fm_match:
            try:
                note.frontmatter = yaml.safe_load(fm_match.group(1)) or {}
            except yaml.YAMLError as e:
                logger.warning(f"Error parseando YAML en {filepath}: {e}")
                note.frontmatter = {}
            # Quitar frontmatter del contenido para el resto del parsing
            content_body = content[fm_match.end():]
        else:
            content_body = content

        # Extraer título (frontmatter > heading > filename)
        note.title = (
            note.frontmatter.get("title")
            or self._extract_heading(content_body)
            or filepath.stem
        )

        # Extraer tags (frontmatter + inline)
        fm_tags = note.frontmatter.get("tags", [])
        if isinstance(fm_tags, str):
            fm_tags = [fm_tags]
        inline_tags = self.INLINE_TAG_RE.findall(content_body)
        note.tags = list(set(fm_tags + inline_tags))

        # Extraer wikilinks
        note.wikilinks = list(set(self.WIKILINK_RE.findall(content)))

        # Determinar tipo de nodo
        note.node_type = self._determine_node_type(filepath, note.frontmatter)

        # Preview del contenido (primeros 200 chars sin frontmatter)
        note.content_preview = content_body.strip()[:200]

        return note

    def _extract_heading(self, content: str) -> Optional[str]:
        """Extrae el primer heading H1 del contenido."""
        match = self.HEADING_RE.search(content)
        return match.group(1).strip() if match else None

    def _determine_node_type(self, filepath: Path, frontmatter: dict) -> str:
        """Determina el tipo de nodo Neo4j basándose en la ruta y frontmatter."""
        fm_type = frontmatter.get("type", "")

        if fm_type == "chat_parent":
            return "Chat"
        elif fm_type == "chat_child":
            return "MicroChat"  # No debería llegar aquí por exclusión
        elif fm_type == "nota_atomica":
            return "NotaAtomica"

        # Por ruta
        rel = str(filepath.relative_to(VAULT_ROOT))
        if "notas_atomicas" in rel:
            return "NotaAtomica"
        elif ".chats_saved" in rel and "micro_chats" not in rel:
            return "Chat"
        elif "Outputs" in rel:
            return "Output"
        elif "Agentes" in rel:
            return "Agente"
        elif "Ideas" in rel:
            return "Idea"

        return "Nota"

    def _should_exclude(self, filepath: Path) -> bool:
        """Verifica si el archivo debe excluirse del espejeo."""
        rel = str(filepath.relative_to(VAULT_ROOT))

        # Excluir micro_chats
        if "micro_chats" in rel:
            return True

        # Excluir archivos SKILL.md
        if filepath.name == "SKILL.md":
            return True

        # Excluir carpeta .obsidian
        if ".obsidian" in rel:
            return True

        # Excluir templates
        if "_templates" in rel:
            return True

        return False


# ============================================
# NEO4J WRITER
# ============================================

class Neo4jWriter:
    """Escribe nodos y relaciones en Neo4j a partir de ParsedNotes."""

    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database
        logger.info(f"Conectado a Neo4j en {uri}")

    def close(self):
        self.driver.close()
        logger.info("Conexión Neo4j cerrada")

    def upsert_note(self, note: ParsedNote):
        """Crea o actualiza un nodo en Neo4j y sus relaciones."""
        with self.driver.session(database=self.database) as session:
            # 1. MERGE del nodo principal
            session.execute_write(self._merge_node, note)

            # 2. Crear relaciones por cada wikilink
            for link_target in note.wikilinks:
                session.execute_write(self._merge_link, note.title, link_target)

            # 3. Crear/vincular tags como nodos
            for tag in note.tags:
                session.execute_write(self._merge_tag, note.title, tag)

        logger.info(
            f"✅ Espejeado: [{note.node_type}] {note.title} "
            f"({len(note.wikilinks)} links, {len(note.tags)} tags)"
        )

    def delete_note(self, filepath: Path):
        """Elimina un nodo del grafo cuando se borra el archivo fuente."""
        title = filepath.stem
        with self.driver.session(database=self.database) as session:
            session.execute_write(self._delete_node, title)
        logger.info(f"🗑️ Eliminado del grafo: {title}")

    @staticmethod
    def _merge_node(tx, note: ParsedNote):
        """MERGE de un nodo con sus propiedades."""
        query = """
        MERGE (n {nombre: $title})
        SET n:$node_type,
            n.ruta = $path,
            n.tags = $tags,
            n.tipo_frontmatter = $fm_type,
            n.preview = $preview,
            n.ultima_sync = datetime()
        """
        # Neo4j no permite labels dinámicos en MERGE directamente,
        # así que usamos APOC o un enfoque de dos pasos
        query = f"""
        MERGE (n {{nombre: $title}})
        SET n:{note.node_type},
            n.ruta = $path,
            n.tags = $tags,
            n.tipo_frontmatter = $fm_type,
            n.preview = $preview,
            n.ultima_sync = datetime()
        """
        tx.run(
            query,
            title=note.title,
            path=note.relative_path,
            tags=note.tags,
            fm_type=note.frontmatter.get("type", ""),
            preview=note.content_preview,
        )

    @staticmethod
    def _merge_link(tx, source_title: str, target_title: str):
        """MERGE de una relación MENCIONA entre dos nodos."""
        query = """
        MERGE (s {nombre: $source})
        MERGE (t {nombre: $target})
        MERGE (s)-[:MENCIONA]->(t)
        """
        tx.run(query, source=source_title, target=target_title)

    @staticmethod
    def _merge_tag(tx, note_title: str, tag: str):
        """MERGE de un nodo Tag y relación TAGGED."""
        query = """
        MERGE (n {nombre: $title})
        MERGE (t:Tag {nombre: $tag})
        MERGE (n)-[:TAGGED]->(t)
        """
        tx.run(query, title=note_title, tag=tag)

    @staticmethod
    def _delete_node(tx, title: str):
        """Elimina un nodo y todas sus relaciones."""
        query = """
        MATCH (n {nombre: $title})
        DETACH DELETE n
        """
        tx.run(query, title=title)


# ============================================
# FILE SYSTEM WATCHER
# ============================================

class VaultEventHandler(FileSystemEventHandler):
    """Maneja eventos del sistema de archivos de la bóveda."""

    def __init__(self, parser: MarkdownParser, writer: Neo4jWriter):
        self.parser = parser
        self.writer = writer

    def on_created(self, event):
        if not event.is_directory:
            self._process_file(Path(event.src_path))

    def on_modified(self, event):
        if not event.is_directory:
            self._process_file(Path(event.src_path))

    def on_deleted(self, event):
        if not event.is_directory:
            filepath = Path(event.src_path)
            if filepath.suffix in WATCHED_EXTENSIONS:
                self.writer.delete_note(filepath)

    def _process_file(self, filepath: Path):
        """Procesa un archivo creado o modificado."""
        if filepath.suffix not in WATCHED_EXTENSIONS:
            return

        note = self.parser.parse(filepath)
        if note:
            self.writer.upsert_note(note)


# ============================================
# SYNC COMPLETO (una vez)
# ============================================

def full_sync(parser: MarkdownParser, writer: Neo4jWriter):
    """Escanea toda la bóveda y sincroniza todo con Neo4j."""
    logger.info("=" * 60)
    logger.info("SINCRONIZACIÓN COMPLETA INICIADA")
    logger.info(f"Escaneando: {AGENT_ROOT}")
    logger.info("=" * 60)

    count = 0
    for md_file in AGENT_ROOT.rglob("*.md"):
        note = parser.parse(md_file)
        if note:
            writer.upsert_note(note)
            count += 1

    logger.info(f"Sincronización completa: {count} notas espejeadas")


# ============================================
# MAIN
# ============================================

def main():
    parser = MarkdownParser()

    # Verificar conexión a Neo4j
    try:
        writer = Neo4jWriter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE)
    except Exception as e:
        logger.error(f"No se pudo conectar a Neo4j: {e}")
        logger.error("Asegúrate de que Neo4j esté corriendo.")
        sys.exit(1)

    try:
        # ¿Sincronización completa o modo watch?
        if "--sync" in sys.argv:
            full_sync(parser, writer)
        else:
            # Primero: sync completo
            full_sync(parser, writer)

            # Luego: monitoreo continuo
            logger.info("=" * 60)
            logger.info("MODO WATCH ACTIVADO — Monitoreando cambios...")
            logger.info(f"Carpeta: {AGENT_ROOT}")
            logger.info("Presiona Ctrl+C para detener")
            logger.info("=" * 60)

            handler = VaultEventHandler(parser, writer)
            observer = Observer()
            observer.schedule(handler, str(AGENT_ROOT), recursive=True)
            observer.start()

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                logger.info("Watch detenido por el usuario")

            observer.join()

    finally:
        writer.close()


if __name__ == "__main__":
    main()
