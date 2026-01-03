# -*- coding: utf-8 -*-
"""
ChatBot - Sistema de Consultas sobre Pokémon
NO es un chat con IA, sino un sistema de métodos que hacen consultas a la BD.
Proporciona información sobre Pokémon, tipos, estadísticas, evoluciones, etc.
"""
from typing import Dict, List, Optional
from app.repositories.pokemon_repository import EspecieRepository, TipoRepository
from app.services.pokeapi_service import PokeAPIService
from config.database import get_db_context
import logging

logger = logging.getLogger(__name__)


class ChatBotService:
    """
    Servicio de ChatBot - Sistema de Consultas sobre Pokémon.
    
    Métodos de búsqueda:
    - /help - Mostrar ayuda
    - /stats <pokémon> - Ver estadísticas de un Pokémon
    - /tipo <tipo> - Ver todos los Pokémon de un tipo
    - /evolucion <pokémon> - Ver cadena de evolución
    - /comparar <pok1> <pok2> - Comparar dos Pokémon
    - /equipo <equipo_id> - Ver detalles de un equipo
    - /buscar <texto> - Buscar Pokémon por nombre
    """
    
    COMANDOS = {
        'help': 'Ver todos los comandos disponibles',
        'stats': 'Ver estadísticas: /stats <nombre>',
        'tipo': 'Ver Pokémon por tipo: /tipo <tipo>',
        'evolucion': 'Ver evoluciones: /evolucion <nombre>',
        'comparar': 'Comparar: /comparar <pok1> <pok2>',
        'equipo': 'Ver equipo: /equipo <equipo_id>',
        'buscar': 'Buscar: /buscar <texto>',
    }
    
    @staticmethod
    def procesar_consulta(mensaje: str, usuario: str) -> Dict[str, any]:
        """
        Procesa una consulta del usuario.
        
        Args:
            mensaje: Mensaje con el comando
            usuario: Nombre del usuario
            
        Returns:
            Dict con respuesta y tipo
        """
        try:
            if not mensaje.startswith('/'):
                return {
                    'respuesta': 'Los comandos deben comenzar con /. Usa /help para ver los comandos.',
                    'tipo': 'error'
                }
            
            partes = mensaje.split(maxsplit=1)
            comando = partes[0].lstrip('/').lower()
            args = partes[1] if len(partes) > 1 else ''
            
            if comando == 'help':
                return ChatBotService.cmd_help()
            elif comando == 'stats':
                return ChatBotService.cmd_stats(args)
            elif comando == 'tipo':
                return ChatBotService.cmd_tipo(args)
            elif comando == 'evolucion':
                return ChatBotService.cmd_evolucion(args)
            elif comando == 'comparar':
                return ChatBotService.cmd_comparar(args)
            elif comando == 'equipo':
                return ChatBotService.cmd_equipo(args, usuario)
            elif comando == 'buscar':
                return ChatBotService.cmd_buscar(args)
            else:
                return {
                    'respuesta': f'Comando desconocido: {comando}. Usa /help',
                    'tipo': 'error'
                }
        except Exception as e:
            logger.error(f"Error en ChatBot: {str(e)}")
            return {
                'respuesta': f'Error: {str(e)}',
                'tipo': 'error'
            }
    
    # ===== COMANDOS =====
    
    @staticmethod
    def cmd_help() -> Dict[str, any]:
        """Comando: /help"""
        respuesta = "**Comandos disponibles del ChatBot:**\n\n"
        for cmd, desc in ChatBotService.COMANDOS.items():
            respuesta += f"• **/{cmd}** - {desc}\n"
        return {'respuesta': respuesta, 'tipo': 'info'}
    
    @staticmethod
    def cmd_stats(nombre: str) -> Dict[str, any]:
        """Comando: /stats <pokémon>"""
        if not nombre.strip():
            return {'respuesta': 'Uso: /stats <nombre_pokémon>', 'tipo': 'error'}
        
        try:
            with get_db_context() as conn:
                especie = EspecieRepository.find_by_name(conn, nombre.strip())
                if not especie:
                    return {'respuesta': f'Pokémon "{nombre}" no encontrado', 'tipo': 'error'}
                
                # Obtener tipos
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nombreTipo FROM especie_tipo
                    WHERE nombreEspecie = ?
                """, (especie['nombreEspecie'],))
                tipos = [row[0] for row in cursor.fetchall()]
                
                respuesta = f"""
**{especie['nombreEspecie']}** 

📊 **Estadísticas:**
• Ataque: {especie['ataque']}
• Ataque Especial: {especie['ataqueEsp']}
• Defensa: {especie['def']}
• Defensa Especial: {especie['defEsp']}
• Velocidad: {especie['velocidad']}
• Vida: {especie['vida']}

🏷️ **Tipos:** {', '.join(tipos) if tipos else 'N/A'}
                """
                return {'respuesta': respuesta.strip(), 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_tipo(nombre_tipo: str) -> Dict[str, any]:
        """Comando: /tipo <tipo>"""
        if not nombre_tipo.strip():
            return {'respuesta': 'Uso: /tipo <nombre_tipo>', 'tipo': 'error'}
        
        try:
            with get_db_context() as conn:
                # Buscar Pokémon del tipo
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT nombreEspecie FROM especie_tipo
                    WHERE LOWER(nombreTipo) = LOWER(?)
                    LIMIT 20
                """, (nombre_tipo.strip(),))
                
                pokemon_list = [row[0] for row in cursor.fetchall()]
                if not pokemon_list:
                    return {'respuesta': f'No hay Pokémon de tipo "{nombre_tipo}"', 'tipo': 'error'}
                
                respuesta = f"**Pokémon de tipo {nombre_tipo.capitalize()}:**\n\n"
                for i, pk in enumerate(pokemon_list, 1):
                    respuesta += f"{i}. {pk}\n"
                
                return {'respuesta': respuesta, 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_evolucion(nombre: str) -> Dict[str, any]:
        """Comando: /evolucion <pokémon>"""
        if not nombre.strip():
            return {'respuesta': 'Uso: /evolucion <nombre_pokémon>', 'tipo': 'error'}
        
        try:
            cadena = PokeAPIService.get_evolution_chain(nombre.strip())
            if not cadena:
                return {'respuesta': f'No se encontró cadena de evolución para "{nombre}"', 'tipo': 'error'}
            
            respuesta = f"**Cadena de Evolución de {nombre.capitalize()}:**\n\n"
            respuesta += " → ".join(cadena)
            return {'respuesta': respuesta, 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_comparar(args: str) -> Dict[str, any]:
        """Comando: /comparar <pok1> <pok2>"""
        partes = args.split(' vs ')
        if len(partes) != 2:
            return {'respuesta': 'Uso: /comparar <pokémon1> vs <pokémon2>', 'tipo': 'error'}
        
        pk1_nombre = partes[0].strip()
        pk2_nombre = partes[1].strip()
        
        try:
            with get_db_context() as conn:
                pk1 = EspecieRepository.find_by_name(conn, pk1_nombre)
                pk2 = EspecieRepository.find_by_name(conn, pk2_nombre)
                
                if not pk1 or not pk2:
                    return {'respuesta': 'Uno o ambos Pokémon no encontrados', 'tipo': 'error'}
                
                respuesta = f"""
**Comparación: {pk1['nombreEspecie']} vs {pk2['nombreEspecie']}**

| Stat | {pk1['nombreEspecie']} | {pk2['nombreEspecie']} |
|------|----------|----------|
| Ataque | {pk1.get('ataque', 0)} | {pk2.get('ataque', 0)} |
| Defensa | {pk1.get('def', 0)} | {pk2.get('def', 0)} |
| Velocidad | {pk1.get('velocidad', 0)} | {pk2.get('velocidad', 0)} |
| Vida | {pk1.get('vida', 0)} | {pk2.get('vida', 0)} |
                """
                return {'respuesta': respuesta.strip(), 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_equipo(equipo_id: str, usuario: str) -> Dict[str, any]:
        """Comando: /equipo <equipo_id>"""
        if not equipo_id.strip():
            return {'respuesta': 'Uso: /equipo <id_equipo>', 'tipo': 'error'}
        
        try:
            # TODO: Implementar consulta a EquipoRepository
            return {'respuesta': '[TODO] Detalles del equipo', 'tipo': 'info'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_buscar(texto: str) -> Dict[str, any]:
        """Comando: /buscar <texto>"""
        if not texto.strip():
            return {'respuesta': 'Uso: /buscar <texto>', 'tipo': 'error'}
        
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nombreEspecie FROM especie
                    WHERE LOWER(nombreEspecie) LIKE LOWER(?)
                    LIMIT 10
                """, (f"%{texto.strip()}%",))
                
                resultados = [row[0] for row in cursor.fetchall()]
                if not resultados:
                    return {'respuesta': f'No hay resultados para "{texto}"', 'tipo': 'error'}
                
                respuesta = f"**Resultados de búsqueda para \"{texto}\":**\n\n"
                for i, resultado in enumerate(resultados, 1):
                    respuesta += f"{i}. {resultado}\n"
                
                return {'respuesta': respuesta, 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}

