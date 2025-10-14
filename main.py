from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "aa"  # flask genera un runtime error si no esta esta linea

# Mock user
USER = {"username": "ash", "password": "pikachu"}

# Pa luego
pokemon_list = [
    {"name": "Bulbasaur", "type": "Grass/Poison", "id": 1},
    {"name": "Charmander", "type": "Fire", "id": 4},
    {"name": "Squirtle", "type": "Water", "id": 7},
]


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


@app.route("/pokedex")
def pokedex():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", pokemons=pokemon_list, user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)