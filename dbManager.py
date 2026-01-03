import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("pokemon.db")
cur = conn.cursor()

# Create the table
cur.execute("""
CREATE TABLE IF NOT EXISTS pokemon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type1 TEXT NOT NULL,
    type2 TEXT,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER
)
""")

# Commit and close
conn.commit()
conn.close()

print("Database 'pokemon.db' created successfully with table 'pokemon' 🚀")