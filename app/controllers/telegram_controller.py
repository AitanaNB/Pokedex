# -*- coding: utf-8 -*-
"""
Telegram controller - Share teams on Telegram.
"""
from flask import Blueprint, render_template, request, session, jsonify
from app.utils.decorators import login_required
from app.controllers import Pokedex
telegram_bp = Blueprint('telegram', __name__)


@telegram_bp.route('/', methods=['GET'])
@login_required
def page():
    return render_template("telegram/share.html")


@telegram_bp.route('/share', methods=['POST'])
@login_required
def share():
    data = request.get_json(silent=True)
    username = session["user"]
    data['username'] = username
    #print(data)
    result = Pokedex.vincularUsuario(data['username'], data['telegramUsername'])
    if result == 1:
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "fatalitico"})

