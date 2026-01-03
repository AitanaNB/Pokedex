# -*- coding: utf-8 -*-
"""
Telegram controller - Share teams on Telegram.
"""
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from app.utils.decorators import login_required
from app.repositories.equipo_repository import EquipoRepository

telegram_bp = Blueprint('telegram', __name__)


@telegram_bp.route('/')
@login_required
def share():
    """Show Telegram sharing page."""
    username = session.get('user')
    equipos = EquipoRepository.get_by_user(username)
    return render_template('telegram/share.html', equipos=equipos)


@telegram_bp.route('/send', methods=['POST'])
@login_required
def send_team():
    """Send team to Telegram."""
    equipo_id = request.form.get('equipo_id')
    
    if not equipo_id:
        flash('Selecciona un equipo', 'danger')
        return redirect(url_for('telegram.share'))
    
    # TODO: Implement Telegram bot integration
    flash('Funcionalidad de Telegram pendiente de implementar', 'info')
    return redirect(url_for('telegram.share'))
