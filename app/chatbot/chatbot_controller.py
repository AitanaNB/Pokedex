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
from app.repositories.equipo_repository import EquipoRepository

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



@chatbot_bp.route('/api/teams', methods=['GET'])
@login_required
@approved_required
def api_get_teams():
    """
    Devuelve la lista de equipos del usuario (id y nombre) para poblar un selector.
    """
    username = session.get('user')
    equipos = EquipoRepository.get_by_user(username)
    res = [{'id': e.idEquipo, 'nombre': e.nombre} for e in equipos]
    return jsonify({'teams': res})


@chatbot_bp.route('/api/team/best', methods=['POST'])
@login_required
@approved_required
def api_team_best():
    """
    Recibe JSON con {'team_id': <id>} y devuelve el Pokémon del equipo con la
    mayor media de estadísticas. Si hay empate, devuelve todos.
    """
    data = request.get_json() or {}
    team_id = data.get('team_id')
    username = session.get('user')

    if not team_id:
        return jsonify({'error': 'team_id is required'}), 400

    equipo = EquipoRepository.find_by_id(team_id)
    if not equipo or equipo.username != username:
        return jsonify({'error': 'Equipo no encontrado o acceso denegado'}), 404

    # Calcular media por Pokémon
    best = []
    best_avg = None
    for p in equipo.pokemons:
        # Algunos campos usan nombres diferentes en el dataclass
        try:
            stats_sum = (
                (getattr(p, 'ataque', 0) or 0) +
                (getattr(p, 'ataqueEsp', 0) or 0) +
                (getattr(p, 'def_', 0) or 0) +
                (getattr(p, 'defEsp', 0) or 0) +
                (getattr(p, 'vel', 0) or 0) +
                (getattr(p, 'vida', 0) or 0)
            )
        except Exception:
            stats_sum = 0

        avg = stats_sum / 6.0

        if best_avg is None or avg > best_avg:
            best_avg = avg
            best = [{'nombre': p.nombre, 'avg': round(avg, 2)}]
        elif avg == best_avg:
            best.append({'nombre': p.nombre, 'avg': round(avg, 2)})

    if not best:
        return jsonify({'respuesta': 'El equipo no tiene Pokémon', 'tipo': 'info'})

    # Ordenar por nombre alfabéticamente si hay empates
    if len(best) > 1:
        best = sorted(best, key=lambda x: x['nombre'])
        texto = f"Mejor(es) Pokémon (empate, avg={best[0]['avg']}):\n"
        for i, b in enumerate(best, 1):
            texto += f"{i}. {b['nombre']}\n"
    else:
        texto = f"Mejor Pokémon: {best[0]['nombre']} (avg={best[0]['avg']})"

    return jsonify({'respuesta': texto, 'tipo': 'success'})





