"""
Test de conexión a Neo4j Aura
Sesión: 2026-04-10.03
"""

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Cargar variables de entorno
load_dotenv()

# Configuración
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

def test_connection():
    print(f"[CONECTAR] Intentando conectar a: {URI}")
    print(f"[USUARIO] Usuario: {USERNAME}")
    
    try:
        # Crear driver
        driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        
        # Verificar conectividad
        driver.verify_connectivity()
        print("[OK] Conexion exitosa!")
        
        # Obtener información del servidor
        with driver.session() as session:
            result = session.run("CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition")
            record = result.single()
            print(f"[INFO] Servidor: {record['name']}")
            print(f"[INFO] Version: {record['versions'][0]}")
            print(f"[INFO] Edicion: {record['edition']}")
            
            # Contar nodos existentes
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()["count"]
            print(f"[INFO] Nodos en base de datos: {count}")
            
            # Crear nodo de prueba
            result = session.run("""
                CREATE (c:Config {name: 'CerebroFractal', created: datetime()})
                RETURN c
            """)
            print("[OK] Nodo de prueba creado")
            
            # Verificar creación
            result = session.run("MATCH (c:Config {name: 'CerebroFractal'}) RETURN c.created as created")
            record = result.single()
            print(f"[OK] Nodo verificado - Creado: {record['created']}")
            
        driver.close()
        print("\n[EXITO] Todas las pruebas pasaron correctamente")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error de conexion: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    exit(0 if success else 1)
