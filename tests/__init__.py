# -*- coding: utf-8 -*-
"""Main application module."""
import unittest
from config.database import init_database
import os
from run import create_app


class TestBase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()

        # Configuración para usar BD para tests
        self.app.config['DATABASE'] = 'test.db'
        #  modo testing
        self.app.config['TESTING'] = True
        # desactivar para facilitar tests
        self.app.config['WTF_CSRF_ENABLED'] = False

        #crear el cliente
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Limpiamos el contexto
        self.app_context.pop()
        if os.path.exists('test.db'):
            os.remove('test.db')

    def test_app_is_testing(self):
        """Test para ver si la configuración se carga bien"""
        self.assertTrue(self.app.config['TESTING'])

