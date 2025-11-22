"""
Servidor Principal Flask - Sistema Braille
==========================================
Punto de entrada de la aplicación web.

Ejecutar con:
    python run.py

La aplicación estará disponible en:
    http://localhost:5000

Autor: GR4
Fecha: Noviembre 2025
"""

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os
from backend.routes.braille_routes import braille_bp
from backend.database.db_manager import db_manager


def create_app():
    """
    Factory function para crear la aplicación Flask.
    
    Returns:
        Instancia de Flask configurada
    """
    # Crear instancia de Flask
    app = Flask(
        __name__,
        static_folder='frontend',
        static_url_path='',
        template_folder='frontend'
    )
    
    # Configuración
    app.config['SECRET_KEY'] = 'braille-secret-key-2025'  # En producción usar variable de entorno
    app.config['JSON_AS_ASCII'] = False  # Permitir caracteres Unicode en JSON
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Límite de 16MB para uploads
    
    # Habilitar CORS para permitir peticiones desde el frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # En producción especificar dominios permitidos
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Registrar blueprints (rutas)
    app.register_blueprint(braille_bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        """Página principal."""
        return send_from_directory('frontend', 'index.html')
    
    # Ruta para servir archivos estáticos adicionales
    @app.route('/<path:path>')
    def serve_static(path):
        """Sirve archivos estáticos del frontend."""
        return send_from_directory('frontend', path)
    
    # Manejo de errores
    @app.errorhandler(404)
    def not_found(error):
        """Maneja errores 404."""
        return {
            'success': False,
            'error': 'Recurso no encontrado',
            'message': str(error)
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Maneja errores 500."""
        return {
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(error)
        }, 500
    
    # Inicializar base de datos
    with app.app_context():
        db_manager.init_database()
    
    return app


def main():
    """Función principal para ejecutar el servidor."""
    # Crear aplicación
    app = create_app()
    
    # Obtener configuración del entorno
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Banner de inicio
    print("=" * 70)
    print("  SISTEMA DE TRANSCRIPCIÓN BRAILLE")
    print("  Versión 1.0.0")
    print("=" * 70)
    print(f"\n  🚀 Servidor iniciando en http://{host}:{port}")
    print(f"  🔧 Modo debug: {debug}")
    print(f"  📁 Base de datos: {db_manager.db_path}")
    print("\n  Presiona Ctrl+C para detener el servidor")
    print("=" * 70 + "\n")
    
    # Iniciar servidor
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )


if __name__ == '__main__':
    main()
