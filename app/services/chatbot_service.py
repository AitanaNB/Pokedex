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
        'rivales': 'Ver matchups de tipos: /rivales',
        'mejor': 'Ver el mejor Pokémon por stat: /mejor <stat>'
    }
    
    @staticmethod
    def procesar_consulta(mensaje: str, usuario: str) -> Dict[str, any]:
        """
        Procesa una consulta del usuario.

        Args:
            mensaje: Mensaje que contiene el comando (debe comenzar con '/').
            usuario: Nombre del usuario que realiza la consulta.

        Returns:
            Dict con las claves:
              - 'respuesta': texto que se mostrará al usuario.
              - 'tipo': categoría del mensaje ('info', 'success', 'error').
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
            elif comando == 'mejor':
                return ChatBotService.cmd_mejor(args)
            elif comando == 'rivales':
                return ChatBotService.cmd_rivales()
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
        """Comando: /help

        Devuelve una descripción de los comandos disponibles.

        Returns:
            Dict con 'respuesta' (texto con la lista de comandos) y 'tipo'='info'.
        """
        respuesta = "**Comandos disponibles del ChatBot:**\n\n"
        for cmd, desc in ChatBotService.COMANDOS.items():
            respuesta += f"• **/{cmd}** - {desc}\n"
        return {'respuesta': respuesta, 'tipo': 'info'}
    
    @staticmethod
    def cmd_stats(nombre: str) -> Dict[str, any]:
        """Comando: /stats <pokémon>

        Busca en la base de datos la especie por nombre y devuelve sus estadísticas y tipos.

        Args:
            nombre: Nombre (o parte) del Pokémon a consultar.

        Returns:
            Dict con la respuesta formateada y el tipo ('success' o 'error').
        """
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
                
                # Mostrar atributos, usando 'Unavailable' si falta alguno
                atk = especie.get('ataque', 'Unavailable')
                atk_esp = especie.get('ataqueEsp', 'Unavailable')
                df = especie.get('def', 'Unavailable')
                df_esp = especie.get('defEsp', 'Unavailable')
                vel = especie.get('velocidad', 'Unavailable')
                hp = especie.get('vida', 'Unavailable')

                respuesta = f"""
**{especie.get('nombreEspecie', 'Unknown')}** 

📊 **Estadísticas:**
• Ataque: {atk}
• Ataque Especial: {atk_esp}
• Defensa: {df}
• Defensa Especial: {df_esp}
• Velocidad: {vel}
• Vida: {hp}

🏷️ **Tipos:** {', '.join(tipos) if tipos else 'N/A'}
                """
                return {'respuesta': respuesta.strip(), 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_tipo(nombre_tipo: str) -> Dict[str, any]:
        """Comando: /tipo <tipo>

        Lista Pokémon que pertenecen al tipo indicado (máx 20 resultados).

        Args:
            nombre_tipo: Nombre del tipo a consultar.

        Returns:
            Dict con la lista formateada o un mensaje de error.
        """
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
        """Comando: /evolucion <pokémon>

        Obtiene la cadena de evolución consultando el servicio PokeAPIService.

        Args:
            nombre: Nombre del Pokémon cuya cadena evolutiva se solicita.

        Returns:
            Dict con la cadena de evolución o información si no existe.
        """
        if not nombre.strip():
            return {'respuesta': 'Uso: /evolucion <nombre_pokémon>', 'tipo': 'error'}
        
        try:
            cadena = PokeAPIService.get_evolution_chain(nombre.strip())
            if not cadena or len(cadena) == 0:
                return {'respuesta': f'{nombre.strip().capitalize()} no tiene cadena evolutiva', 'tipo': 'info'}
            
            respuesta = f"**Cadena de Evolución de {nombre.capitalize()}:**\n\n"
            respuesta += " → ".join(cadena)
            return {'respuesta': respuesta, 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_comparar(args: str) -> Dict[str, any]:
        """Comando: /comparar <pok1> vs <pok2>

        Compara estadísticas básicas entre dos especies.

        Args:
            args: Cadena con el formato "<pok1> vs <pok2>".

        Returns:
            Dict con la tabla de comparación o un mensaje de error si el formato o
            las especies no existen.
        """
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
        """Comando: /equipo <equipo_id>

        (Placeholder) Devuelve información de un equipo del usuario.

        Args:
            equipo_id: Identificador del equipo.
            usuario: Nombre del usuario propietario del equipo.

        Returns:
            Dict con detalles del equipo o un mensaje informativo.
        """
        if not equipo_id.strip():
            return {'respuesta': 'Uso: /equipo <id_equipo>', 'tipo': 'error'}
        
        try:
            # TODO: Implementar consulta a EquipoRepository
            return {'respuesta': '[TODO] Detalles del equipo', 'tipo': 'info'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_buscar(texto: str) -> Dict[str, any]:
        """Comando: /buscar <texto>

        Busca especies cuyo nombre contenga el texto proporcionado (insensible a mayúsculas).

        Args:
            texto: Cadena de búsqueda.

        Returns:
            Dict con los resultados enumerados o un mensaje si no hay coincidencias.
        """
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

    @staticmethod
    def cmd_mejor(stat: str) -> Dict[str, any]:
        """Comando: /mejor <stat>

        Busca el/los Pokémon con el valor máximo para la estadística indicada.
        Si hay empate, se listan todos los Pokémon empatados (ordenados alfabéticamente).

        Args:
            stat: Nombre de la estadística (ej. 'ataque', 'def', 'velocidad', 'vida').

        Returns:
            Dict con la lista de los mejores Pokémon o un mensaje de error.
        """
        if not stat.strip():
            return {'respuesta': 'Uso: /mejor <stat>', 'tipo': 'error'}

        stat_col = stat.strip().lower()
        # Validar columna esperada (evitar SQL injection al usar parámetros)
        valid_stats = {'ataque', 'ataqueesp', 'def', 'defesp', 'velocidad', 'vida'}
        # Normalize possible variants
        stat_col_normalized = stat_col.replace(' ', '').replace('-', '')
        if stat_col_normalized not in valid_stats:
            return {'respuesta': f'Estadística desconocida: {stat}', 'tipo': 'error'}

        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                # Obtener valor máximo
                cursor.execute(f"SELECT MAX({stat_col_normalized}) FROM especie")
                max_row = cursor.fetchone()
                if not max_row or max_row[0] is None:
                    return {'respuesta': f'No hay datos para la estadística {stat}', 'tipo': 'error'}

                max_val = max_row[0]
                # Obtener todos los Pokémon con ese valor máximo
                cursor.execute(
                    f"SELECT nombreEspecie FROM especie WHERE {stat_col_normalized} = ? ORDER BY nombreEspecie ASC",
                    (max_val,)
                )
                rows = cursor.fetchall()
                nombres = [r[0] for r in rows]

                if not nombres:
                    return {'respuesta': 'No se encontraron Pokémon', 'tipo': 'error'}

                if len(nombres) == 1:
                    respuesta = f"**Mejor Pokémon ({stat_col}):**\n\n1. {nombres[0]}"
                else:
                    respuesta = f"**Mejor(es) Pokémon ({stat_col}) - Empate:**\n\n"
                    for i, n in enumerate(nombres, 1):
                        respuesta += f"{i}. {n}\n"

                return {'respuesta': respuesta, 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}
    
    @staticmethod
    def cmd_rivales() -> Dict[str, any]:
        """Comando: /rivales - Muestra tipos ventajosos y desventajosos

        Consulta la tabla de efectos entre tipos y devuelve un ejemplo de Pokémon
        que representa la mayor ventaja y la mayor desventaja.

        Returns:
            Dict con texto formateado de matchups y 'tipo'='success' o 'error'.
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                
                # Obtener el múltiplo más alto (ventaja)
                cursor.execute("""
                    SELECT afectaTipo, afectadoTipo, multiplo 
                    FROM afectado 
                    WHERE multiplo = (SELECT MAX(multiplo) FROM afectado)
                    LIMIT 1
                """)
                ventaja = cursor.fetchone()
                
                # Obtener el múltiplo más bajo (desventaja)
                cursor.execute("""
                    SELECT afectaTipo, afectadoTipo, multiplo 
                    FROM afectado 
                    WHERE multiplo = (SELECT MIN(multiplo) FROM afectado)
                    LIMIT 1
                """)
                desventaja = cursor.fetchone()
                
                respuesta = "**🔥 MATCHUPS DE TIPOS 🔥**\n\n"
                
                # Información de ventaja
                if ventaja:
                    tipo_ventaja = ventaja['afectaTipo']
                    tipo_afectado = ventaja['afectadoTipo']
                    multiplo_ventaja = ventaja['multiplo']
                    
                    # Obtener un Pokémon de tipo ventajoso
                    cursor.execute("""
                        SELECT DISTINCT es.nombreEspecie, es.ataque, es.def
                        FROM especie_tipo et
                        JOIN especie es ON et.nombreEspecie = es.nombreEspecie
                        WHERE et.nombreTipo = ?
                        LIMIT 1
                    """, (tipo_ventaja,))
                    pokemon_ventaja = cursor.fetchone()
                    
                    if pokemon_ventaja:
                        respuesta += f"✅ **Ventaja Máxima:**\n"
                        respuesta += f"   • Tipo: {tipo_ventaja} hace x{multiplo_ventaja} a {tipo_afectado}\n"
                        respuesta += f"   • Pokémon: {pokemon_ventaja['nombreEspecie']}\n"
                        respuesta += f"   • Ataque: {pokemon_ventaja['ataque']} | Defensa: {pokemon_ventaja['def']}\n\n"
                
                # Información de desventaja
                if desventaja:
                    tipo_desventaja = desventaja['afectaTipo']
                    tipo_afectado2 = desventaja['afectadoTipo']
                    multiplo_desventaja = desventaja['multiplo']
                    
                    # Obtener un Pokémon de tipo desventajoso
                    cursor.execute("""
                        SELECT DISTINCT es.nombreEspecie, es.ataque, es.def
                        FROM especie_tipo et
                        JOIN especie es ON et.nombreEspecie = es.nombreEspecie
                        WHERE et.nombreTipo = ?
                        LIMIT 1
                    """, (tipo_desventaja,))
                    pokemon_desventaja = cursor.fetchone()
                    
                    if pokemon_desventaja:
                        respuesta += f"❌ **Desventaja Máxima:**\n"
                        respuesta += f"   • Tipo: {tipo_desventaja} hace x{multiplo_desventaja} a {tipo_afectado2}\n"
                        respuesta += f"   • Pokémon: {pokemon_desventaja['nombreEspecie']}\n"
                        respuesta += f"   • Ataque: {pokemon_desventaja['ataque']} | Defensa: {pokemon_desventaja['def']}\n"
                
                return {'respuesta': respuesta, 'tipo': 'success'}
        except Exception as e:
            return {'respuesta': f'Error: {str(e)}', 'tipo': 'error'}

