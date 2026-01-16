import sys
import types
import unittest
from unittest.mock import patch

# Evitar importar Flask real en el entorno de tests; crear un módulo 'flask' falso
if 'flask' not in sys.modules:
    _flask = types.ModuleType('flask')
    _flask.current_app = None
    sys.modules['flask'] = _flask

from app.services.chatbot_service import ChatBotService


class FakeCursor:
    def __init__(self, behavior=None):
        # behavior: dict mapping keywords to results
        self.behavior = behavior or {}
        self._last = None

    def execute(self, query, params=None):
        q = query.lower()
        self._last = q
        # determine response based on keywords
        if 'select nombretipo' in q:
            self._result = [('Fuego',)]
        elif 'max(' in q:
            # return a single-row tuple for MAX
            # behavior can specify 'max' key
            self._result = [(self.behavior.get('max', None),)]
        elif 'where' in q and ' = ?' in q:
            # return rows specified in behavior['names']
            self._result = [(n,) for n in self.behavior.get('names', [])]
        else:
            self._result = []

    def fetchall(self):
        return self._result

    def fetchone(self):
        return self._result[0] if self._result else None


class FakeConn:
    def __init__(self, cursor):
        self._cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def cursor(self):
        return self._cursor


class ChatBotAdvancedTests(unittest.TestCase):
    @patch('app.services.chatbot_service.get_db_context')
    @patch('app.services.chatbot_service.EspecieRepository')
    def test_stats_missing_attribute_shows_unavailable(self, mock_repo, mock_dbctx):
        # Simular especie sin 'ataqueEsp'
        especie = {
            'nombreEspecie': 'Pikachu',
            'ataque': 55,
            # 'ataqueEsp' ausente
            'def': 40,
            'defEsp': 30,
            'velocidad': 90,
            'vida': 35
        }

        mock_repo.find_by_name.return_value = especie

        cursor = FakeCursor()
        conn = FakeConn(cursor)
        mock_dbctx.return_value = conn

        res = ChatBotService.procesar_consulta('/stats Pikachu', 'tester')

        self.assertEqual(res['tipo'], 'success')
        # Debe mostrar Ataque Especial y 'Unavailable' porque falta el atributo
        self.assertIn('Ataque Especial', res['respuesta'])
        self.assertIn('Unavailable', res['respuesta'])

    @patch('app.services.chatbot_service.get_db_context')
    def test_mejor_handles_ties_and_orders_alphabetically(self, mock_dbctx):
        # Simular max valor y dos nombres empatados
        behavior = {'max': 100, 'names': ['Charizard', 'Blastoise']}
        cursor = FakeCursor(behavior=behavior)
        conn = FakeConn(cursor)
        mock_dbctx.return_value = conn

        res = ChatBotService.procesar_consulta('/mejor ataque', 'tester')

        self.assertEqual(res['tipo'], 'success')
        # Debe listar ambos nombres
        self.assertIn('Charizard', res['respuesta'])
        self.assertIn('Blastoise', res['respuesta'])
        # Debe mencionar 'Empate' o similar
        self.assertIn('Empate', res['respuesta'])


if __name__ == '__main__':
    unittest.main()
import unittest

from app.services.chatbot_service import ChatBotService


class TestChatBotService(unittest.TestCase):
    def test_help(self):
        res = ChatBotService.procesar_consulta('/help', 'tester')
        self.assertIn('Comandos disponibles', res['respuesta'])
        self.assertEqual(res['tipo'], 'info')

    def test_non_command(self):
        res = ChatBotService.procesar_consulta('hola', 'tester')
        self.assertEqual(res['tipo'], 'error')

    def test_stats_no_name(self):
        res = ChatBotService.procesar_consulta('/stats ', 'tester')
        self.assertEqual(res['tipo'], 'error')

    def test_tipo_no_name(self):
        res = ChatBotService.procesar_consulta('/tipo ', 'tester')
        self.assertEqual(res['tipo'], 'error')

    def test_buscar_no_text(self):
        res = ChatBotService.procesar_consulta('/buscar ', 'tester')
        self.assertEqual(res['tipo'], 'error')

    def test_comparar_format_error(self):
        res = ChatBotService.procesar_consulta('/comparar pikachu', 'tester')
        self.assertEqual(res['tipo'], 'error')


if __name__ == '__main__':
    unittest.main()
