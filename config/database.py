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


if __name__ == "__main__":
    # Create data directory if not exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    init_database()

