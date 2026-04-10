"""
Mirror Pipeline v2 - Obsidian Vault to Neo4j Graph
Batch processing + Error handling + Encoding fix
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class MarkdownParser:
    """Parsea archivos Markdown extrayendo frontmatter, wikilinks y tags."""
    
    @staticmethod
    def parse_file(filepath: str) -> Optional[Dict]:
        """Parsea un archivo Markdown y retorna dict con metadatos."""
        try:
            # Intentar UTF-8 primero
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Si falla, intentar Latin-1 (ISO-8859-1)
                with open(filepath, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            return MarkdownParser.parse_content(content, filepath)
        except Exception as e:
            print(f"[ERROR] No se pudo parsear {filepath}: {e}")
            return None
    
    @staticmethod
    def parse_content(content: str, filepath: str) -> Dict:
        """Parsea contenido Markdown."""
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
        
        # Extraer hashtags
        hashtag_pattern = r'(?:^|\s)#([a-zA-Z0-9_\-\/]+)'
        hashtags = re.findall(hashtag_pattern, body)
        
        # Combinar tags
        frontmatter_tags = frontmatter.get('tags', []) or []
        if isinstance(frontmatter_tags, str):
            frontmatter_tags = [frontmatter_tags]
        all_tags = list(set(frontmatter_tags + hashtags))
        
        # Extraer titulo
        title = frontmatter.get('title', '')
        if not title:
            h1_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1).strip()
            else:
                title = Path(filepath).stem
        
        # Determinar tipo
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
            'title': title or '',
            'type': note_type or 'Nota',
            'tags': [t for t in all_tags if t] or [],
            'wikilinks': wikilinks or [],
            'frontmatter': frontmatter or {},
            'body_preview': body[:500] if body else '',
            'date_created': frontmatter.get('date_captured', frontmatter.get('date_extracted', datetime.now().isoformat())) or datetime.now().isoformat()
        }


def main():
    """Funcion principal con batch processing."""
    print("=" * 60)
    print("CEREBRO FRACTAL - Mirror Pipeline v2")
    print("Obsidian Vault -> Neo4j Graph (Batch Mode)")
    print("=" * 60)
    
    VAULT_PATH = os.getenv("VAULT_PATH", r"C:\Users\Fran\Desktop\CerebroFractal\vault_template")
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USERNAME")
    NEO4J_PASS = os.getenv("NEO4J_PASSWORD")
    
    if not all([NEO4J_URI, NEO4J_USER, NEO4J_PASS]):
        print("[ERROR] Faltan variables de entorno NEO4J_*")
        return
    
    print(f"[CONFIG] Vault: {VAULT_PATH}")
    print(f"[CONFIG] Neo4j: {NEO4J_URI}")
    
    # 1. Escanear vault
    print("\n[1/4] Escaneando vault...")
    vault_path = Path(VAULT_PATH)
    md_files = list(vault_path.rglob("*.md"))
    print(f"[INFO] {len(md_files)} archivos encontrados")
    
    # 2. Parsear notas
    print("\n[2/4] Parseando notas...")
    parser = MarkdownParser()
    notes = []
    errors = 0
    for i, md_file in enumerate(md_files, 1):
        if '.git' in str(md_file):
            continue
        note = parser.parse_file(str(md_file))
        if note:
            notes.append(note)
        else:
            errors += 1
        if i % 100 == 0:
            print(f"  Procesados {i}/{len(md_files)}...")
    
    print(f"[INFO] {len(notes)} notas parseadas ({errors} errores)")
    
    # 3. Conectar a Neo4j y sincronizar en batch
    print("\n[3/4] Conectando a Neo4j...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    
    with driver.session() as session:
        # Limpiar
        print("[INFO] Limpiando base de datos...")
        session.run("MATCH (n) DETACH DELETE n")
        
        # Crear notas en batch
        print(f"[INFO] Creando {len(notes)} nodos...")
        for i, note in enumerate(notes, 1):
            try:
                session.run("""
                    CREATE (n:Nota {
                        filepath: $filepath,
                        title: $title,
                        filename: $filename,
                        type: $type,
                        tags: $tags,
                        date_created: $date_created,
                        body_preview: $body_preview
                    })
                """, 
                    filepath=note['filepath'],
                    title=note['title'],
                    filename=note['filename'],
                    type=note['type'],
                    tags=note['tags'],
                    date_created=note['date_created'],
                    body_preview=note['body_preview'][:200]  # Limitar tamaño
                )
                if i % 100 == 0:
                    print(f"  Creados {i}/{len(notes)} nodos...")
            except Exception as e:
                print(f"[ERROR] No se pudo crear nodo para {note['filepath']}: {e}")
        
        print(f"[INFO] {len(notes)} nodos creados")
        
        # 4. Crear tags
        print("\n[4/4] Creando tags y relaciones...")
        all_tags = set()
        for note in notes:
            for tag in note['tags']:
                if tag:
                    all_tags.add(tag)
        
        for tag in all_tags:
            try:
                session.run("MERGE (t:Tag {name: $name})", name=tag)
            except Exception as e:
                print(f"[ERROR] Tag {tag}: {e}")
        
        print(f"[INFO] {len(all_tags)} tags creados")
        
        # Relacionar notas con tags
        link_count = 0
        for note in notes:
            for tag in note['tags']:
                if tag:
                    try:
                        session.run("""
                            MATCH (n:Nota {filepath: $filepath})
                            MATCH (t:Tag {name: $tag})
                            MERGE (n)-[:HAS_TAG]->(t)
                        """, filepath=note['filepath'], tag=tag)
                        link_count += 1
                    except:
                        pass
        
        print(f"[INFO] {link_count} relaciones nota-tag creadas")
        
        # Estadisticas
        result = session.run("MATCH (n) RETURN labels(n)[0] as label, count(n) as count")
        stats = {r["label"]: r["count"] for r in result}
        
        print("\n" + "=" * 60)
        print("RESUMEN:")
        for label, count in stats.items():
            print(f"  {label}: {count}")
        print("=" * 60)
    
    driver.close()
    print("\n[EXITO] Sincronizacion completada!")


if __name__ == "__main__":
    main()
