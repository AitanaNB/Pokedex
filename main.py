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
            print("Fetching Pokemon from API...")
            # Try to fetch from PokeAPI, use fallback data if API is unavailable
            api_available = True
            
            # Test if API is available
            try:
                test_response = requests.get("https://pokeapi.co/api/v2/pokemon/1", timeout=5)
                if test_response.status_code != 200:
                    api_available = False
            except:
                api_available = False
                print("API not available, using fallback Pokemon data...")
            
            if api_available:
                # Fetch first 151 Pokemon from PokeAPI
                for i in range(1, 152):
                    try:
                        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}", timeout=5)
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
            else:
                # Fallback: Use sample Pokemon data
                sample_pokemon = [
                    ("Bulbasaur", "Grass", "Poison", 45, 49, 49),
                    ("Ivysaur", "Grass", "Poison", 60, 62, 63),
                    ("Venusaur", "Grass", "Poison", 80, 82, 83),
                    ("Charmander", "Fire", None, 39, 52, 43),
                    ("Charmeleon", "Fire", None, 58, 64, 58),
                    ("Charizard", "Fire", "Flying", 78, 84, 78),
                    ("Squirtle", "Water", None, 44, 48, 65),
                    ("Wartortle", "Water", None, 59, 63, 80),
                    ("Blastoise", "Water", None, 79, 83, 100),
                    ("Caterpie", "Bug", None, 45, 30, 35),
                    ("Metapod", "Bug", None, 50, 20, 55),
                    ("Butterfree", "Bug", "Flying", 60, 45, 50),
                    ("Weedle", "Bug", "Poison", 40, 35, 30),
                    ("Kakuna", "Bug", "Poison", 45, 25, 50),
                    ("Beedrill", "Bug", "Poison", 65, 90, 40),
                    ("Pidgey", "Normal", "Flying", 40, 45, 40),
                    ("Pidgeotto", "Normal", "Flying", 63, 60, 55),
                    ("Pidgeot", "Normal", "Flying", 83, 80, 75),
                    ("Rattata", "Normal", None, 30, 56, 35),
                    ("Raticate", "Normal", None, 55, 81, 60),
                    ("Spearow", "Normal", "Flying", 40, 60, 30),
                    ("Fearow", "Normal", "Flying", 65, 90, 65),
                    ("Ekans", "Poison", None, 35, 60, 44),
                    ("Arbok", "Poison", None, 60, 95, 69),
                    ("Pikachu", "Electric", None, 35, 55, 40),
                    ("Raichu", "Electric", None, 60, 90, 55),
                    ("Sandshrew", "Ground", None, 50, 75, 85),
                    ("Sandslash", "Ground", None, 75, 100, 110),
                    ("Nidoran♀", "Poison", None, 55, 47, 52),
                    ("Nidorina", "Poison", None, 70, 62, 67),
                    ("Nidoqueen", "Poison", "Ground", 90, 92, 87),
                    ("Nidoran♂", "Poison", None, 46, 57, 40),
                    ("Nidorino", "Poison", None, 61, 72, 57),
                    ("Nidoking", "Poison", "Ground", 81, 102, 77),
                    ("Clefairy", "Fairy", None, 70, 45, 48),
                    ("Clefable", "Fairy", None, 95, 70, 73),
                    ("Vulpix", "Fire", None, 38, 41, 40),
                    ("Ninetales", "Fire", None, 73, 76, 75),
                    ("Jigglypuff", "Normal", "Fairy", 115, 45, 20),
                    ("Wigglytuff", "Normal", "Fairy", 140, 70, 45),
                    ("Zubat", "Poison", "Flying", 40, 45, 35),
                    ("Golbat", "Poison", "Flying", 75, 80, 70),
                    ("Oddish", "Grass", "Poison", 45, 50, 55),
                    ("Gloom", "Grass", "Poison", 60, 65, 70),
                    ("Vileplume", "Grass", "Poison", 75, 80, 85),
                    ("Paras", "Bug", "Grass", 35, 70, 55),
                    ("Parasect", "Bug", "Grass", 60, 95, 80),
                    ("Venonat", "Bug", "Poison", 60, 55, 50),
                    ("Venomoth", "Bug", "Poison", 70, 65, 60),
                    ("Diglett", "Ground", None, 10, 55, 25),
                    ("Dugtrio", "Ground", None, 35, 100, 50),
                    ("Meowth", "Normal", None, 40, 45, 35),
                    ("Persian", "Normal", None, 65, 70, 60),
                    ("Psyduck", "Water", None, 50, 52, 48),
                    ("Golduck", "Water", None, 80, 82, 78),
                    ("Mankey", "Fighting", None, 40, 80, 35),
                    ("Primeape", "Fighting", None, 65, 105, 60),
                    ("Growlithe", "Fire", None, 55, 70, 45),
                    ("Arcanine", "Fire", None, 90, 110, 80),
                    ("Poliwag", "Water", None, 40, 50, 40),
                    ("Poliwhirl", "Water", None, 65, 65, 65),
                    ("Poliwrath", "Water", "Fighting", 90, 95, 95),
                    ("Abra", "Psychic", None, 25, 20, 15),
                    ("Kadabra", "Psychic", None, 40, 35, 30),
                    ("Alakazam", "Psychic", None, 55, 50, 45),
                    ("Machop", "Fighting", None, 70, 80, 50),
                    ("Machoke", "Fighting", None, 80, 100, 70),
                    ("Machamp", "Fighting", None, 90, 130, 80),
                    ("Bellsprout", "Grass", "Poison", 50, 75, 35),
                    ("Weepinbell", "Grass", "Poison", 65, 90, 50),
                    ("Victreebel", "Grass", "Poison", 80, 105, 65),
                    ("Tentacool", "Water", "Poison", 40, 40, 35),
                    ("Tentacruel", "Water", "Poison", 80, 70, 65),
                    ("Geodude", "Rock", "Ground", 40, 80, 100),
                    ("Graveler", "Rock", "Ground", 55, 95, 115),
                    ("Golem", "Rock", "Ground", 80, 120, 130),
                    ("Ponyta", "Fire", None, 50, 85, 55),
                    ("Rapidash", "Fire", None, 65, 100, 70),
                    ("Slowpoke", "Water", "Psychic", 90, 65, 65),
                    ("Slowbro", "Water", "Psychic", 95, 75, 110),
                    ("Magnemite", "Electric", "Steel", 25, 35, 70),
                    ("Magneton", "Electric", "Steel", 50, 60, 95),
                    ("Farfetch'd", "Normal", "Flying", 52, 90, 55),
                    ("Doduo", "Normal", "Flying", 35, 85, 45),
                    ("Dodrio", "Normal", "Flying", 60, 110, 70),
                    ("Seel", "Water", None, 65, 45, 55),
                    ("Dewgong", "Water", "Ice", 90, 70, 80),
                    ("Grimer", "Poison", None, 80, 80, 50),
                    ("Muk", "Poison", None, 105, 105, 75),
                    ("Shellder", "Water", None, 30, 65, 100),
                    ("Cloyster", "Water", "Ice", 50, 95, 180),
                    ("Gastly", "Ghost", "Poison", 30, 35, 30),
                    ("Haunter", "Ghost", "Poison", 45, 50, 45),
                    ("Gengar", "Ghost", "Poison", 60, 65, 60),
                    ("Onix", "Rock", "Ground", 35, 45, 160),
                    ("Drowzee", "Psychic", None, 60, 48, 45),
                    ("Hypno", "Psychic", None, 85, 73, 70),
                    ("Krabby", "Water", None, 30, 105, 90),
                    ("Kingler", "Water", None, 55, 130, 115),
                    ("Voltorb", "Electric", None, 40, 30, 50),
                    ("Electrode", "Electric", None, 60, 50, 70),
                    ("Exeggcute", "Grass", "Psychic", 60, 40, 80),
                    ("Exeggutor", "Grass", "Psychic", 95, 95, 85),
                    ("Cubone", "Ground", None, 50, 50, 95),
                    ("Marowak", "Ground", None, 60, 80, 110),
                    ("Hitmonlee", "Fighting", None, 50, 120, 53),
                    ("Hitmonchan", "Fighting", None, 50, 105, 79),
                    ("Lickitung", "Normal", None, 90, 55, 75),
                    ("Koffing", "Poison", None, 40, 65, 95),
                    ("Weezing", "Poison", None, 65, 90, 120),
                    ("Rhyhorn", "Ground", "Rock", 80, 85, 95),
                    ("Rhydon", "Ground", "Rock", 105, 130, 120),
                    ("Chansey", "Normal", None, 250, 5, 5),
                    ("Tangela", "Grass", None, 65, 55, 115),
                    ("Kangaskhan", "Normal", None, 105, 95, 80),
                    ("Horsea", "Water", None, 30, 40, 70),
                    ("Seadra", "Water", None, 55, 65, 95),
                    ("Goldeen", "Water", None, 45, 67, 60),
                    ("Seaking", "Water", None, 80, 92, 65),
                    ("Staryu", "Water", None, 30, 45, 55),
                    ("Starmie", "Water", "Psychic", 60, 75, 85),
                    ("Mr. Mime", "Psychic", "Fairy", 40, 45, 65),
                    ("Scyther", "Bug", "Flying", 70, 110, 80),
                    ("Jynx", "Ice", "Psychic", 65, 50, 35),
                    ("Electabuzz", "Electric", None, 65, 83, 57),
                    ("Magmar", "Fire", None, 65, 95, 57),
                    ("Pinsir", "Bug", None, 65, 125, 100),
                    ("Tauros", "Normal", None, 75, 100, 95),
                    ("Magikarp", "Water", None, 20, 10, 55),
                    ("Gyarados", "Water", "Flying", 95, 125, 79),
                    ("Lapras", "Water", "Ice", 130, 85, 80),
                    ("Ditto", "Normal", None, 48, 48, 48),
                    ("Eevee", "Normal", None, 55, 55, 50),
                    ("Vaporeon", "Water", None, 130, 65, 60),
                    ("Jolteon", "Electric", None, 65, 65, 60),
                    ("Flareon", "Fire", None, 65, 130, 60),
                    ("Porygon", "Normal", None, 65, 60, 70),
                    ("Omanyte", "Rock", "Water", 35, 40, 100),
                    ("Omastar", "Rock", "Water", 70, 60, 125),
                    ("Kabuto", "Rock", "Water", 30, 80, 90),
                    ("Kabutops", "Rock", "Water", 60, 115, 105),
                    ("Aerodactyl", "Rock", "Flying", 80, 105, 65),
                    ("Snorlax", "Normal", None, 160, 110, 65),
                    ("Articuno", "Ice", "Flying", 90, 85, 100),
                    ("Zapdos", "Electric", "Flying", 90, 90, 85),
                    ("Moltres", "Fire", "Flying", 90, 100, 90),
                    ("Dratini", "Dragon", None, 41, 64, 45),
                    ("Dragonair", "Dragon", None, 61, 84, 65),
                    ("Dragonite", "Dragon", "Flying", 91, 134, 95),
                    ("Mewtwo", "Psychic", None, 106, 110, 90),
                    ("Mew", "Psychic", None, 100, 100, 100),
                ]
                
                cur.executemany("""
                    INSERT INTO pokemon (name, type1, type2, hp, attack, defense)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, sample_pokemon)
                print(f"Loaded {len(sample_pokemon)} Pokemon from fallback data")
            
            conn.commit()
            print("Pokemon data loaded successfully!")
        
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