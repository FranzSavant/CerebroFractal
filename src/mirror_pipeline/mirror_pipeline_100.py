"""
Mirror Pipeline - 100 notas de prueba
Validacion con subset del vault real
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

LIMIT = 100  # Solo primeras 100 notas

class MarkdownParser:
    @staticmethod
    def parse_file(filepath: str) -> Optional[Dict]:
        try:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin-1') as f:
                    content = f.read()
            return MarkdownParser.parse_content(content, filepath)
        except Exception as e:
            print(f"[ERROR] {filepath}: {e}")
            return None
    
    @staticmethod
    def parse_content(content: str, filepath: str) -> Dict:
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
        
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', body)
        hashtags = re.findall(r'(?:^|\s)#([a-zA-Z0-9_\-\/]+)', body)
        
        frontmatter_tags = frontmatter.get('tags', []) or []
        if isinstance(frontmatter_tags, str):
            frontmatter_tags = [frontmatter_tags]
        all_tags = list(set(frontmatter_tags + hashtags))
        
        title = frontmatter.get('title', '')
        if not title:
            h1_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
            title = h1_match.group(1).strip() if h1_match else Path(filepath).stem
        
        note_type = 'Nota'
        if 'nota_atomica' in str(filepath).lower():
            note_type = 'NotaAtomica'
        elif 'chat' in str(filepath).lower():
            note_type = 'Chat'
        
        return {
            'filepath': filepath,
            'filename': Path(filepath).name,
            'title': title or '',
            'type': note_type,
            'tags': [t for t in all_tags if t] or [],
            'wikilinks': wikilinks or [],
            'date_created': frontmatter.get('date_captured', datetime.now().isoformat()) or datetime.now().isoformat(),
            'body_preview': body[:200] if body else ''
        }


def main():
    print("=" * 60)
    print(f"CEREBRO FRACTAL - Mirror Pipeline ({LIMIT} notas)")
    print("=" * 60)
    
    VAULT_PATH = os.getenv("VAULT_PATH")
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USERNAME")
    NEO4J_PASS = os.getenv("NEO4J_PASSWORD")
    
    # 1. Escanear (solo primeras LIMIT)
    print(f"\n[1/3] Escaneando vault (limite: {LIMIT})...")
    md_files = list(Path(VAULT_PATH).rglob("*.md"))[:LIMIT]
    print(f"[INFO] {len(md_files)} archivos seleccionados")
    
    # 2. Parsear
    print("\n[2/3] Parseando...")
    parser = MarkdownParser()
    notes = [parser.parse_file(str(f)) for f in md_files if '.git' not in str(f)]
    notes = [n for n in notes if n]
    print(f"[INFO] {len(notes)} notas validas")
    
    # 3. Sincronizar
    print("\n[3/3] Sincronizando con Neo4j...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        print("[INFO] BD limpiada")
        
        # Crear notas
        for note in notes:
            session.run("""
                CREATE (n:Nota {
                    filepath: $filepath, title: $title, filename: $filename,
                    type: $type, tags: $tags, date_created: $date_created,
                    body_preview: $body_preview
                })
            """, **note)
        print(f"[INFO] {len(notes)} notas creadas")
        
        # Crear tags
        all_tags = set()
        for note in notes:
            all_tags.update(note['tags'])
        
        for tag in all_tags:
            if tag:
                session.run("MERGE (t:Tag {name: $name})", name=tag)
        print(f"[INFO] {len(all_tags)} tags creados")
        
        # Relaciones
        for note in notes:
            for tag in note['tags']:
                if tag:
                    session.run("""
                        MATCH (n:Nota {filepath: $fp}), (t:Tag {name: $tag})
                        MERGE (n)-[:HAS_TAG]->(t)
                    """, fp=note['filepath'], tag=tag)
        
        # Stats
        result = session.run("MATCH (n) RETURN labels(n)[0] as l, count(n) as c")
        stats = {r["l"]: r["c"] for r in result}
        
        print("\n" + "=" * 60)
        print("RESUMEN:")
        for label, count in stats.items():
            print(f"  {label}: {count}")
        print("=" * 60)
    
    driver.close()
    print("\n[EXITO] Validacion completada!")
    print(f"Ver grafo en: https://console.neo4j.io")

if __name__ == "__main__":
    main()
