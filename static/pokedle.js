function startGame() {
    fetch('/pokedle/api/start', { method: 'POST' })
        .then(() => {
            document.querySelector('#results tbody').innerHTML = '';
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('guessInput').value = '';
        });
}

function sendGuess() {
    const input = document.getElementById('guessInput');
    const name = input.value.trim();
    if (!name) return;

    fetch('/pokedle/api/guess', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: name })
    })
    .then(res => res.json())
    .then(data => {

        if (data.error) {
            showMessage(data.error);
            return;
        }

        // 👉 SIEMPRE añade fila
        addRow(data.pokemon, data.comparison);
        input.value = '';

        // 👉 POPUP SOLO SI ACIERTA
        if (data.correct) {
            showPopup(`🎉 ¡Has adivinado el Pokémon!`);

        }
    });
}

function surrender() {
    fetch('/pokedle/api/surrender', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            showPopup(`😢 Te has rendido.<br>El Pokémon era: <b>${data.nombre}</b>`);
        });
}

function addRow(pokemon, comparison) {
    const tbody = document.querySelector('#results tbody');
    const tr = document.createElement('tr');

    function cell(value, ok) {
        const td = document.createElement('td');
        td.textContent = value;
        td.className = ok ? 'ok' : 'fail';
        return td;
    }

    // Primera columna: especie
    tr.appendChild(cell(pokemon.especie, comparison.especie));
    tr.appendChild(cell(pokemon.ataque, comparison.ataque));
    tr.appendChild(cell(pokemon.ataqueEsp, comparison.ataqueEsp));
    tr.appendChild(cell(pokemon.def, comparison.def));
    tr.appendChild(cell(pokemon.defEsp, comparison.defEsp));
    tr.appendChild(cell(pokemon.vel, comparison.vel));
    tr.appendChild(cell(pokemon.vida, comparison.vida));

    tbody.appendChild(tr);
}


function showPopup(text) {
    document.getElementById('popupText').innerHTML = text;
    document.getElementById('overlay').style.display = 'flex';
}

function showMessage(text) {
    const input = document.getElementById('guessInput');
    input.value = '';
    input.placeholder = text;
    input.classList.add('input-error');

    setTimeout(() => {
        input.placeholder = 'Escribe el nombre del Pokémon...';
        input.classList.remove('input-error');
    }, 2000);
}

// Arranca el juego al cargar
document.addEventListener('DOMContentLoaded', () => {
    startGame();
    document.getElementById('guessInput').addEventListener('keydown', e => {
        if (e.key === 'Enter') sendGuess();
    });
});


