import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("../data/pokemon.db")
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


# Optionally insert some sample data
#cur.executemany("""
#INSERT INTO pokemon (name, type1, type2, hp, attack, defense)
#VALUES (?, ?, ?, ?, ?, ?)
#""", [
#    ("Pikachu", "Electric", None, 35, 55, 40),
#    ("Charmander", "Fire", None, 39, 52, 43),
#    ("Bulbasaur", "Grass", "Poison", 45, 49, 49),
#    ("Squirtle", "Water", None, 44, 48, 65),
#    ("Gengar", "Ghost", "Poison", 60, 65, 60)
#])

# Commit and close

cur.execute("SELECT * FROM pokemon")

for pok in cur.fetchall():
    tipo2 = ""
    if pok[3]!=None:
        tipo2 = "& "+pok[3]
    print(pok[1]+": "+pok[2]+" "+tipo2) #Va por indices -> 0:ID, 1:nombre, 2:tipo, 3:tipo2, etc..
conn.commit()
conn.close()

print("Database 'pokemon.db' created successfully with table 'pokemon' 🚀")