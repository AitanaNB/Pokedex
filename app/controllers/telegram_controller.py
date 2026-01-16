# -*- coding: utf-8 -*-
"""
Telegram controller - Share teams on Telegram.
"""
from flask import Blueprint, render_template, request, session, jsonify
from app.utils.decorators import login_required
from app.controllers import Pokedex
telegram_bp = Blueprint('telegram', __name__)


@telegram_bp.route('/share', methods=['GET'])
@login_required
def share_page():
    return render_template("telegram/share.html")


@telegram_bp.route('/share', methods=['POST'])
@login_required
def share(): #Pide JSON con el user de telegram y devuelve status
    data = request.get_json()
    username = session["user"]
    data['username'] = username

    result = Pokedex.vincularUsuario(username, data['telegramUsername'])
    return jsonify({"status": "ok" if result == 1 else "fatalitico"})

