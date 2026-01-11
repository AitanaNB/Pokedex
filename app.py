# -*- coding: utf-8 -*-
"""
Main Flask application - Pokedex
MVC architecture with repository pattern.
"""
from flask import Flask
from config.database import init_database
import os


def create_app():
    """
    Factory function to create and configure Flask application.
    
    Returns:
        Flask: Configured application instance
    """
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Initialize database
    init_database()
    
    # Register blueprints (controllers)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.pokedex_controller import pokedex_bp
    from app.chatbot.chatbot_controller import chatbot_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.changelog_controller import changelog_bp
    from app.controllers.telegram_controller import telegram_bp
    from app.controllers.pokedle_controller import pokedle_bp
    
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(pokedex_bp, url_prefix='/pokedex')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(changelog_bp, url_prefix='/changelog')
    app.register_blueprint(telegram_bp, url_prefix='/telegram')
    app.register_blueprint(pokedle_bp, url_prefix='/pokedle')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return "Pagina no encontrada", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return "Error interno del servidor", 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("[*] Flask server started")
    print("[*] Available routes:")
    print("  - Login: http://localhost:5000/")
    print("  - Register: http://localhost:5000/register")
    print("  - Pokedex: http://localhost:5000/pokedex")
    print("  - ChatBot: http://localhost:5000/chatbot")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

