from flask import Flask, render_template, request, redirect, url_for, session
import requests
import sqlite3

app = Flask(__name__)
app.secret_key = "aa"  # flask genera un runtime error si no esta esta linea

# Mock user
USER = {"username": "ash", "password": "pikachu"}

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fetch Pokemon from API and store in database
def fetch_and_store_pokemon():
    """Fetch Pokemon from PokeAPI and store in database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if we already have Pokemon in the database
        cur.execute("SELECT COUNT(*) FROM pokemon")
        count = cur.fetchone()[0]
        
        if count == 0:
            # Fetch first 151 Pokemon from PokeAPI
            for i in range(1, 152):
                try:
                    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
                    if response.status_code == 200:
                        data = response.json()
                        name = data['name'].capitalize()
                        types = data['types']
                        type1 = types[0]['type']['name'].capitalize()
                        type2 = types[1]['type']['name'].capitalize() if len(types) > 1 else None
                        
                        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                        hp = stats.get('hp', 0)
                        attack = stats.get('attack', 0)
                        defense = stats.get('defense', 0)
                        
                        cur.execute("""
                            INSERT INTO pokemon (name, type1, type2, hp, attack, defense)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (name, type1, type2, hp, attack, defense))
                except Exception as e:
                    print(f"Error fetching Pokemon {i}: {e}")
                    continue
            
            conn.commit()
        
        conn.close()
    except Exception as e:
        print(f"Error in fetch_and_store_pokemon: {e}")


# Get Pokemon from database
def get_pokemon_list():
    """Retrieve all Pokemon from database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, type1, type2 FROM pokemon ORDER BY id")
        rows = cur.fetchall()
        conn.close()
        
        pokemon_list = []
        for row in rows:
            type_str = row['type1']
            if row['type2']:
                type_str += f"/{row['type2']}"
            pokemon_list.append({
                "id": row['id'],
                "name": row['name'],
                "type": type_str
            })
        return pokemon_list
    except Exception as e:
        print(f"Error getting Pokemon list: {e}")
        return []


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            return redirect(url_for("pokedex"))
        else:
            return render_template("login.html", error="Datos incorrectos, prueba con User: ash, pwd: pikachu")

    return render_template("login.html")

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@app.route("/pokedex")
def pokedex():
    if "user" not in session:
        return redirect(url_for("login"))
    pokemon_list = get_pokemon_list()
    return render_template("index.html", pokemons=pokemon_list, user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    # Initialize database with Pokemon from API on first run
    fetch_and_store_pokemon()
    app.run(debug=True)