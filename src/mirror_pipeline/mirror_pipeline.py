"""
Mirror Pipeline - Obsidian Vault to Neo4j Graph
Sesion: 2026-04-10.03
Convierte archivos Markdown en nodos y relaciones de grafo.
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class MarkdownParser:
    """Parsea archivos Markdown extrayendo frontmatter, wikilinks y tags."""
    
    @staticmethod
    def parse_file(filepath: str) -> Optional[Dict]:
        """Parsea un archivo Markdown y retorna dict con metadatos."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return MarkdownParser.parse_content(content, filepath)
        except Exception as e:
            print(f"[ERROR] No se pudo parsear {filepath}: {e}")
            return None
    
    @staticmethod
    def parse_content(content: str, filepath: str) -> Dict:
        """Parsea contenido Markdown."""
        # Extraer frontmatter
        frontmatter = {}
        body = content
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except yaml.YAMLError:
                    body = content
        
        # Extraer wikilinks [[...]]
        wikilink_pattern = r'\[\[([^\]]+)\]\]'
        wikilinks = re.findall(wikilink_pattern, body)
        
        # Extraer hashtags #tag (excluyendo headers markdown)
        hashtag_pattern = r'(?:^|\s)#([a-zA-Z0-9_\-\/]+)'
        hashtags = re.findall(hashtag_pattern, body)
        
        # Combinar tags del frontmatter y del body
        frontmatter_tags = frontmatter.get('tags', []) or []
        if isinstance(frontmatter_tags, str):
            frontmatter_tags = [frontmatter_tags]
        all_tags = list(set(frontmatter_tags + hashtags))
        
        # Extraer titulo
        title = frontmatter.get('title', '')
        if not title:
            # Buscar primer H1
            h1_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1).strip()
            else:
                # Usar nombre de archivo
                title = Path(filepath).stem
        
        # Determinar tipo de nota
        note_type = frontmatter.get('type', 'nota')
        if 'nota_atomica' in str(filepath).lower() or note_type == 'nota_atomica':
            note_type = 'NotaAtomica'
        elif 'chat' in str(filepath).lower():
            note_type = 'Chat'
        elif 'micro_chat' in str(filepath).lower():
            note_type = 'MicroChat'
        else:
            note_type = 'Nota'
        
        return {
            'filepath': filepath,
            'filename': Path(filepath).name,
            'title': title,
            'type': note_type,
            'tags': all_tags,
            'wikilinks': wikilinks,
            'frontmatter': frontmatter,
            'body_preview': body[:500] if body else '',
            'date_created': frontmatter.get('date_captured', frontmatter.get('date_extracted', datetime.now().isoformat()))
        }


class Neo4jMirror:
    """Maneja la sincronizacion con Neo4j."""
    
    def __init__(self, uri: str, username: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.session = None
    
    def __enter__(self):
        self.session = self.driver.session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
        self.driver.close()
    
    def clear_database(self):
        """Limpia la base de datos (cuidado!)."""
        self.session.run("MATCH (n) DETACH DELETE n")
        print("[INFO] Base de datos limpiada")
    
    def create_note(self, note_data: Dict):
        """Crea un nodo Nota en Neo4j."""
        query = """
        MERGE (n:Nota {filepath: $filepath})
        SET n.title = $title,
            n.filename = $filename,
            n.type = $type,
            n.tags = $tags,
            n.date_created = $date_created,
            n.body_preview = $body_preview,
            n.last_synced = datetime()
        RETURN n
        """
        
        # Limpiar valores que podrian ser None o contener nulls
        tags = note_data['tags'] if note_data['tags'] else []
        tags = [t for t in tags if t is not None]  # Filtrar None
        
        self.session.run(query, 
            filepath=note_data['filepath'],
            title=note_data['title'] or '',
            filename=note_data['filename'] or '',
            type=note_data['type'] or 'Nota',
            tags=tags,
            date_created=note_data['date_created'] or '',
            body_preview=note_data['body_preview'] or ''
        )
    
    def create_tag(self, tag_name: str):
        """Crea un nodo Tag."""
        query = """
        MERGE (t:Tag {name: $name})
        RETURN t
        """
        self.session.run(query, name=tag_name)
    
    def link_note_to_tag(self, filepath: str, tag_name: str):
        """Crea relacion entre Nota y Tag."""
        query = """
        MATCH (n:Nota {filepath: $filepath})
        MATCH (t:Tag {name: $tag_name})
        MERGE (n)-[:HAS_TAG]->(t)
        """
        self.session.run(query, filepath=filepath, tag_name=tag_name)
    
    def link_notes(self, from_filepath: str, to_title: str):
        """Crea relacion entre dos Notas via wikilink."""
        # Buscar la nota destino por titulo o filename
        query = """
        MATCH (from:Nota {filepath: $from_filepath})
        MATCH (to:Nota)
        WHERE to.title = $to_title OR to.filename = $to_title + '.md'
        MERGE (from)-[:LINKS_TO {type: 'wikilink'}]->(to)
        """
        self.session.run(query, from_filepath=from_filepath, to_title=to_title)
    
    def get_stats(self) -> Dict:
        """Retorna estadisticas del grafo."""
        result = self.session.run("""
            MATCH (n) 
            RETURN labels(n)[0] as label, count(n) as count
            ORDER BY count DESC
        """)
        return {record["label"]: record["count"] for record in result}


class MirrorPipeline:
    """Pipeline completo: Vault -> Neo4j."""
    
    def __init__(self, vault_path: str, neo4j_uri: str, neo4j_user: str, neo4j_pass: str):
        self.vault_path = Path(vault_path)
        self.parser = MarkdownParser()
        self.neo4j = Neo4jMirror(neo4j_uri, neo4j_user, neo4j_pass)
    
    def scan_vault(self) -> List[Dict]:
        """Escanea todos los archivos .md en el vault."""
        notes = []
        md_files = list(self.vault_path.rglob("*.md"))
        
        print(f"[INFO] Encontrados {len(md_files)} archivos Markdown")
        
        for md_file in md_files:
            # Ignorar archivos de plantilla o sistema si es necesario
            if '.git' in str(md_file):
                continue
                
            note_data = self.parser.parse_file(str(md_file))
            if note_data:
                notes.append(note_data)
        
        return notes
    
    def sync(self, clear_db: bool = False):
        """Sincroniza el vault completo con Neo4j."""
        with self.neo4j as db:
            if clear_db:
                db.clear_database()
            
            # 1. Escanear vault
            notes = self.scan_vault()
            print(f"[INFO] Parseadas {len(notes)} notas")
            
            # 2. Crear nodos Nota
            for note in notes:
                db.create_note(note)
            print(f"[INFO] Creados {len(notes)} nodos Nota")
            
            # 3. Crear Tags y relaciones
            all_tags = set()
            for note in notes:
                for tag in note['tags']:
                    all_tags.add(tag)
                    db.create_tag(tag)
                    db.link_note_to_tag(note['filepath'], tag)
            print(f"[INFO] Creados {len(all_tags)} nodos Tag")
            
            # 4. Crear relaciones entre notas (wikilinks)
            link_count = 0
            for note in notes:
                for link in note['wikilinks']:
                    # Limpiar alias si existe [[Nota|Alias]]
                    clean_link = link.split('|')[0].strip()
                    db.link_notes(note['filepath'], clean_link)
                    link_count += 1
            print(f"[INFO] Creadas {link_count} relaciones LINKS_TO")
            
            # 5. Estadisticas
            stats = db.get_stats()
            print(f"\n[RESUMEN] Estadisticas del grafo:")
            for label, count in stats.items():
                print(f"  - {label}: {count}")


def main():
    """Funcion principal."""
    print("=" * 60)
    print("CEREBRO FRACTAL - Mirror Pipeline")
    print("Obsidian Vault -> Neo4j Graph")
    print("=" * 60)
    
    # Configuracion
    VAULT_PATH = os.getenv("VAULT_PATH", r"C:\Users\Fran\Desktop\CerebroFractal\vault_template")
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USERNAME")
    NEO4J_PASS = os.getenv("NEO4J_PASSWORD")
    
    if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASS]):
        print("[ERROR] Faltan variables de entorno NEO4J_* en archivo .env")
        return
    
    print(f"[CONFIG] Vault: {VAULT_PATH}")
    print(f"[CONFIG] Neo4j: {NEO4J_URI}")
    
    # Ejecutar sync
    pipeline = MirrorPipeline(VAULT_PATH, NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    pipeline.sync(clear_db=True)  # clear_db=True limpia primero
    
    print("\n[EXITO] Sincronizacion completada!")


if __name__ == "__main__":
    main()
