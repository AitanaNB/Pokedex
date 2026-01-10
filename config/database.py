# -*- coding: utf-8 -*-
"""
SQLite database configuration.
Provides database connection and context management.
"""
import sqlite3
from contextlib import contextmanager
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'pokemon.db')


def get_connection():
    """
    Gets a connection to SQLite database.
    
    Returns:
        sqlite3.Connection: Database connection
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


@contextmanager
def get_db_context():
    """
    Context manager for managing database connections.
    Ensures connections close correctly.
    
    Yields:
        sqlite3.Connection: Database connection
        
    Example:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario")
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """
    Initializes database creating all necessary tables.
    """
    with get_db_context() as conn:
        cursor = conn.cursor()
        
        # USUARIO table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                username TEXT PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                contrasena TEXT NOT NULL,
                foto TEXT,
                esAdmin INTEGER DEFAULT 0,
                aprobado INTEGER DEFAULT 0,
                cuentaTelegram TEXT
            )
        """)
        
        # TIPO table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tipo (
                nombreTipo TEXT PRIMARY KEY
            )
        """)
        
        # ESPECIE table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS especie (
                nombreEspecie TEXT PRIMARY KEY,
                ataque INTEGER NOT NULL,
                ataqueEsp INTEGER NOT NULL,
                def INTEGER NOT NULL,
                defEsp INTEGER NOT NULL,
                vida INTEGER NOT NULL,
                velocidad INTEGER NOT NULL,
                foto TEXT,
                esLegendario INTEGER DEFAULT 0,
                shiny INTEGER DEFAULT 0
            )
        """)
        
        # ATAQUE table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ataque (
                nombreAtaque TEXT PRIMARY KEY,
                damage INTEGER NOT NULL,
                descripcion TEXT,
                nombreTipo TEXT,
                FOREIGN KEY (nombreTipo) REFERENCES tipo(nombreTipo)
            )
        """)
        
        # EQUIPO table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipo (
                idEquipo INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fechaCreacion TEXT NOT NULL,
                username TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES usuario(username) ON DELETE CASCADE
            )
        """)
        
        # POKEMON table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemon (
                idPokemon INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                ataque INTEGER NOT NULL,
                ataqueEsp INTEGER NOT NULL,
                def INTEGER NOT NULL,
                defEsp INTEGER NOT NULL,
                vel INTEGER NOT NULL,
                vida INTEGER NOT NULL,
                nombreEspecie TEXT NOT NULL,
                FOREIGN KEY (nombreEspecie) REFERENCES especie(nombreEspecie)
            )
        """)
        
        # NOTIFICACIONES table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notificaciones (
                username TEXT NOT NULL,
                fecha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                texto TEXT,
                PRIMARY KEY (username, fecha),
                FOREIGN KEY (username) REFERENCES usuario(username) ON DELETE CASCADE
            )
        """)
        
        # SEGUIDORES table (N:M relationship)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seguidores (
                seguidor TEXT NOT NULL,
                seguido TEXT NOT NULL,
                PRIMARY KEY (seguidor, seguido),
                FOREIGN KEY (seguidor) REFERENCES usuario(username) ON DELETE CASCADE,
                FOREIGN KEY (seguido) REFERENCES usuario(username) ON DELETE CASCADE
            )
        """)
        
        # ESPECIE_TIPO table (N:M relationship)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS especie_tipo (
                nombreEspecie TEXT NOT NULL,
                nombreTipo TEXT NOT NULL,
                PRIMARY KEY (nombreEspecie, nombreTipo),
                FOREIGN KEY (nombreEspecie) REFERENCES especie(nombreEspecie) ON DELETE CASCADE,
                FOREIGN KEY (nombreTipo) REFERENCES tipo(nombreTipo) ON DELETE CASCADE
            )
        """)
        
        # ESPECIE_ATAQUE table (N:M relationship)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS especie_ataque (
                nombreEspecie TEXT NOT NULL,
                nombreAtaque TEXT NOT NULL,
                PRIMARY KEY (nombreEspecie, nombreAtaque),
                FOREIGN KEY (nombreEspecie) REFERENCES especie(nombreEspecie) ON DELETE CASCADE,
                FOREIGN KEY (nombreAtaque) REFERENCES ataque(nombreAtaque) ON DELETE CASCADE
            )
        """)
        
        # EQUIPO_POKEMON table (N:M relationship)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipo_pokemon (
                idPokemon INTEGER NOT NULL,
                idEquipo INTEGER NOT NULL,
                PRIMARY KEY (idPokemon, idEquipo),
                FOREIGN KEY (idPokemon) REFERENCES pokemon(idPokemon) ON DELETE CASCADE,
                FOREIGN KEY (idEquipo) REFERENCES equipo(idEquipo) ON DELETE CASCADE
            )
        """)
        
        # POKEMON_ATAQUE table (N:M relationship)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pokemon_ataque (
                idPokemon INTEGER NOT NULL,
                nombreAtaque TEXT NOT NULL,
                PRIMARY KEY (idPokemon, nombreAtaque),
                FOREIGN KEY (idPokemon) REFERENCES pokemon(idPokemon) ON DELETE CASCADE,
                FOREIGN KEY (nombreAtaque) REFERENCES ataque(nombreAtaque) ON DELETE CASCADE
            )
        """)
        
        # AFECTADO table (type effectiveness)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS afectado (
                afectaTipo TEXT NOT NULL,
                afectadoTipo TEXT NOT NULL,
                multiplo REAL NOT NULL,
                PRIMARY KEY (afectaTipo, afectadoTipo),
                FOREIGN KEY (afectaTipo) REFERENCES tipo(nombreTipo) ON DELETE CASCADE,
                FOREIGN KEY (afectadoTipo) REFERENCES tipo(nombreTipo) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        print("[+] Database initialized successfully")
        
        # Cargar datos de tipos y AFECTADO si no existen
        try:
            _load_type_data()
            _load_species_data()
        except Exception as e:
            print(f"[!] Error cargando datos: {str(e)}")


if __name__ == "__main__":
    # Create data directory if not exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_database()


def _load_type_data():
    """
    Carga datos de tipos y efectividad desde PokeAPI si la tabla está vacía.
    """
    import requests
    import time
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si la tabla de tipos está vacía
        cursor.execute("SELECT COUNT(*) FROM tipo")
        type_count = cursor.fetchone()[0]
        
        if type_count > 0:
            return  # Ya tiene datos
        
        # Lista de tipos de Gen 1
        types_list = ['normal', 'fire', 'water', 'grass', 'electric', 'ice',
                     'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
                     'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
        
        print("[*] Cargando tipos desde PokeAPI...")
        
        # Insertar tipos
        for type_name in types_list:
            cursor.execute("INSERT OR IGNORE INTO tipo (nombreTipo) VALUES (?)", (type_name,))
        
        conn.commit()
        
        # Verificar si la tabla AFECTADO está vacía
        cursor.execute("SELECT COUNT(*) FROM afectado")
        if cursor.fetchone()[0] > 0:
            return  # Ya tiene datos
        
        print("[*] Cargando efectividad de tipos desde PokeAPI...")
        
        # Cargar efectividad de tipos
        for type_name in types_list:
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/type/{type_name}", timeout=10)
                response.raise_for_status()
                type_data = response.json()
                
                # Obtener tipos que son dañados por este tipo (double damage)
                for relation in type_data['damage_relations']['double_damage_to']:
                    affected_type = relation['name']
                    multiplo = 2.0  # Daño efectivo = 2x
                    
                    cursor.execute("""
                        INSERT OR IGNORE INTO afectado (afectaTipo, afectadoTipo, multiplo)
                        VALUES (?, ?, ?)
                    """, (type_name, affected_type, multiplo))
                
                # Obtener tipos que son resistidos por este tipo (half damage)
                for relation in type_data['damage_relations']['half_damage_to']:
                    affected_type = relation['name']
                    multiplo = 0.5  # Daño reducido = 0.5x
                    
                    cursor.execute("""
                        INSERT OR IGNORE INTO afectado (afectaTipo, afectadoTipo, multiplo)
                        VALUES (?, ?, ?)
                    """, (type_name, affected_type, multiplo))
                
                print(f"[+] Tipo {type_name} cargado")
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                print(f"[!] Error cargando tipo {type_name}: {str(e)}")
        
        conn.commit()
        print("[+] Datos de efectividad cargados")
        
    except Exception as e:
        print(f"[!] Error cargando datos de tipos: {str(e)}")
    finally:
        conn.close()


def _load_species_data():
    """
    Carga especies de Pokémon Gen 1 desde PokeAPI si la tabla está vacía.
    """
    import requests
    import time
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar si la tabla especie tiene datos
        cursor.execute("SELECT COUNT(*) FROM especie")
        if cursor.fetchone()[0] > 0:
            return  # Ya tiene datos
        
        print("[*] Cargando Pokémon Gen 1 desde PokeAPI (esto puede tardar)...")
        
        # Cargar los 151 Pokémon de Gen 1
        for pokemon_id in range(1, 152):
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}", timeout=10)
                response.raise_for_status()
                poke_data = response.json()
                
                # Extraer nombre y stats
                nombre = poke_data['name'].capitalize()
                stats = {s['stat']['name']: s['base_stat'] for s in poke_data['stats']}
                
                # Insertar especie
                cursor.execute("""
                    INSERT OR IGNORE INTO especie (
                        nombreEspecie, ataque, ataqueEsp, def, defEsp, vida, velocidad, foto, esLegendario, shiny
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
                """, (
                    nombre,
                    stats.get('attack', 0),
                    stats.get('special-attack', 0),
                    stats.get('defense', 0),
                    stats.get('special-defense', 0),
                    stats.get('hp', 0),
                    stats.get('speed', 0),
                    poke_data['sprites']['front_default']
                ))
                
                # Insertar tipos en especie_tipo
                for type_info in poke_data['types']:
                    tipo = type_info['type']['name']
                    cursor.execute("""
                        INSERT OR IGNORE INTO especie_tipo (nombreEspecie, nombreTipo)
                        VALUES (?, ?)
                    """, (nombre, tipo))
                
                if pokemon_id % 10 == 0:
                    print(f"[+] {pokemon_id}/151 Pokémon cargados...")
                    conn.commit()
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                print(f"[!] Error cargando Pokémon {pokemon_id}: {str(e)}")
        
        conn.commit()
        print("[+] 151 Pokémon Gen 1 cargados")
        
    except Exception as e:
        print(f"[!] Error cargando especies: {str(e)}")
    finally:
        conn.close()

