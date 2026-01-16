"""
Controlador del ChatBot - Sistema de Consultas sobre Pokémon.

Proporciona endpoints para:
- Mostrar interfaz de búsqueda de Pokémon
- Procesar comandos de consulta (/stats, /tipo, /evolucion)
- Retornar información en formato JSON

FUNCIONALIDADES IMPLEMENTADAS:
1. Ver estadísticas de Pokémon (/stats <nombre>)
2. Ver cadena de evolución (/evolucion <nombre>)
3. Listar Pokémon por tipo (/tipo <tipo>)

El ChatBot es un sistema de métodos de consulta, NO un chat con IA.
"""

from flask import Blueprint, render_template, request, session, jsonify
from app.utils.decorators import login_required, approved_required
from app.services.chatbot_service import ChatBotService

chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/')
@login_required
@approved_required
def index():
    """
    Página principal del chatbot.
    """
    return render_template('chatbot/index.html', user=session.get('user'))


@chatbot_bp.route('/api/message', methods=['POST'])
@login_required
@approved_required
def send_message():
    """
    Endpoint para enviar consultas al ChatBot.
    
    El ChatBot procesa comandos que hacen consultas a la BD:
    - /help: Ver ayuda
    - /stats <pokémon>: Ver estadísticas
    - /tipo <tipo>: Ver Pokémon de un tipo
    - /evolucion <pokémon>: Ver evoluciones
    - /buscar <texto>: Buscar Pokémon
    """
    data = request.get_json()
    user_message = data.get('message', '').strip()
    username = session.get('user')
    
    if not user_message:
        return jsonify({'error': 'Mensaje vacío'}), 400
    
    # Procesar consulta con ChatBotService
    resultado = ChatBotService.procesar_consulta(user_message, username)
    
    respuesta = {
        'message': resultado.get('respuesta', 'Error procesando consulta'),
        'type': resultado.get('tipo', 'info'),
        'timestamp': '2026-01-03 12:00:00'
    }
    
    return jsonify(respuesta)





