# -*- coding: utf-8 -*-
"""
Pokedle controller - Pokemon guessing game.
"""
from flask import Blueprint, render_template, request, session, jsonify
from app.utils.decorators import login_required
import random
from datetime import datetime

pokedle_bp = Blueprint('pokedle', __name__)


@pokedle_bp.route('/')
@login_required
def game():
    """Show Pokedle game page."""
    return render_template('pokedle/game.html')


@pokedle_bp.route('/api/daily-pokemon')
def get_daily_pokemon():
    """Get the daily Pokemon to guess."""
    # TODO: Implement logic to get random Pokemon from database
    # For now, return a placeholder
    today = datetime.now().strftime('%Y-%m-%d')
    random.seed(today)  # Same Pokemon for everyone on the same day
    
    # Placeholder Pokemon
    pokemon = {
        'id': random.randint(1, 151),
        'name': 'Mystery Pokemon',
        'hints': [
            'Este Pokemon es muy popular',
            'Tiene un tipo especial',
            'Aparece en la primera generacion'
        ]
    }
    
    return jsonify(pokemon)


@pokedle_bp.route('/api/check-guess', methods=['POST'])
@login_required
def check_guess():
    """Check if the guessed Pokemon is correct."""
    data = request.get_json()
    guessed_pokemon = data.get('pokemon', '').lower()
    
    # TODO: Implement proper checking logic
    return jsonify({
        'correct': False,
        'message': 'Funcionalidad pendiente de implementar'
    })
