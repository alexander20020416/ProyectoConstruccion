"""
Rutas API REST - Sistema Braille
=================================
Define los endpoints HTTP para la conversión de texto y generación de señalética.

Endpoints:
- POST /api/convert/to-braille: Convierte español a Braille
- POST /api/convert/to-text: Convierte Braille a español
- POST /api/generate-signage: Genera PDF de señalética
- GET /api/braille/info/<char>: Información sobre un carácter
    - /api/health: Estado del servidor

Autor: GR4
Fecha: Noviembre 2025
"""

from flask import Blueprint, request, jsonify, send_file
from backend.models.braille_converter import braille_converter
from backend.utils.pdf_generator import generate_signage_pdf
from backend.database.db_manager import db_manager
import os
from datetime import datetime

# Crear Blueprint para las rutas
braille_bp = Blueprint('braille', __name__, url_prefix='/api')


@braille_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de salud del servicio.
    
    Returns:
        JSON con estado del servicio
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Braille Converter API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200


@braille_bp.route('/convert/to-braille', methods=['POST'])
def convert_to_braille():
    """
    Convierte texto español a Braille.
    
    Request Body:
        {
            "text": "Hola mundo",
            "format": "unicode"  // opcional: unicode, dots, description
        }
    
    Response:
        {
            "success": true,
            "input_text": "Hola mundo",
            "braille": "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕",
            "format": "unicode",
            "character_count": 10,
            "timestamp": "2025-11-22T..."
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "text" es requerido'
            }), 400
        
        input_text = data['text']
        output_format = data.get('format', 'unicode')
        
        # Validar formato
        if output_format not in ['unicode', 'dots', 'description']:
            return jsonify({
                'success': False,
                'error': 'Formato inválido. Opciones: unicode, dots, description'
            }), 400
        
        # Validar texto
        is_valid, unsupported_chars = braille_converter.validate_text(input_text)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': 'Texto contiene caracteres no soportados',
                'unsupported_characters': unsupported_chars
            }), 400
        
        # Convertir a Braille
        braille_output = braille_converter.text_to_braille(input_text, output_format)
        
        # Guardar en base de datos
        db_manager.save_conversion(
            original_text=input_text,
            braille_text=braille_output,
            conversion_type='text_to_braille'
        )
        
        return jsonify({
            'success': True,
            'input_text': input_text,
            'braille': braille_output,
            'format': output_format,
            'character_count': len(input_text),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error en conversión: {str(e)}'
        }), 500


@braille_bp.route('/convert/to-text', methods=['POST'])
def convert_to_text():
    """
    Convierte Braille Unicode a texto español.
    
    Request Body:
        {
            "braille": "⠓⠕⠇⠁"
        }
    
    Response:
        {
            "success": true,
            "braille_input": "⠓⠕⠇⠁",
            "text": "hola",
            "character_count": 4,
            "timestamp": "2025-11-22T..."
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'braille' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "braille" es requerido'
            }), 400
        
        braille_input = data['braille']
        
        # Convertir a texto
        text_output = braille_converter.braille_to_text(braille_input)
        
        # Guardar en base de datos
        db_manager.save_conversion(
            original_text=text_output,
            braille_text=braille_input,
            conversion_type='braille_to_text'
        )
        
        return jsonify({
            'success': True,
            'braille_input': braille_input,
            'text': text_output,
            'character_count': len(text_output),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error en conversión: {str(e)}'
        }), 500


@braille_bp.route('/braille/info/<char>', methods=['GET'])
def get_character_info(char):
    """
    Obtiene información detallada sobre un carácter en Braille.
    
    Args:
        char: Carácter a consultar (en URL)
    
    Response:
        {
            "success": true,
            "character": "a",
            "type": "Serie 1 (a-j)",
            "dots": [1],
            "unicode": "⠁",
            "description": "Puntos: 1"
        }
    """
    try:
        if not char or len(char) != 1:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar exactamente un carácter'
            }), 400
        
        info = braille_converter.get_braille_info(char)
        
        if info is None:
            return jsonify({
                'success': False,
                'error': f'Carácter "{char}" no soportado en Braille'
            }), 404
        
        return jsonify({
            'success': True,
            **info
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener información: {str(e)}'
        }), 500


@braille_bp.route('/generate-signage', methods=['POST'])
def generate_signage():
    """
    Genera un PDF de señalética Braille.
    
    Request Body:
        {
            "title": "Ascensor",
            "items": [
                {"text": "Piso 1", "number": "1"},
                {"text": "Piso 2", "number": "2"}
            ],
            "format": "elevator"  // elevator, door, label
        }
    
    Response:
        Archivo PDF para descarga
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos'
            }), 400
        
        title = data.get('title', 'Señalética Braille')
        items = data.get('items', [])
        signage_format = data.get('format', 'elevator')
        
        if not items:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar al menos un elemento'
            }), 400
        
        # Generar PDF
        pdf_path = generate_signage_pdf(
            title=title,
            items=items,
            format_type=signage_format
        )
        
        # Guardar registro en base de datos
        db_manager.save_pdf_generation(
            title=title,
            file_path=pdf_path,
            format_type=signage_format
        )
        
        # Enviar archivo
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'senaletica_braille_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al generar PDF: {str(e)}'
        }), 500


@braille_bp.route('/history', methods=['GET'])
def get_conversion_history():
    """
    Obtiene el historial de conversiones.
    
    Query Params:
        limit: Número máximo de registros (default: 50)
        type: Filtrar por tipo (text_to_braille, braille_to_text)
    
    Response:
        {
            "success": true,
            "history": [
                {
                    "id": 1,
                    "original_text": "Hola",
                    "braille_text": "⠓⠕⠇⠁",
                    "conversion_type": "text_to_braille",
                    "timestamp": "2025-11-22T..."
                }
            ],
            "count": 1
        }
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        conversion_type = request.args.get('type', None)
        
        history = db_manager.get_conversion_history(
            limit=limit,
            conversion_type=conversion_type
        )
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener historial: {str(e)}'
        }), 500


@braille_bp.route('/validate', methods=['POST'])
def validate_text():
    """
    Valida si un texto puede ser convertido a Braille.
    
    Request Body:
        {
            "text": "Texto a validar"
        }
    
    Response:
        {
            "success": true,
            "is_valid": true,
            "unsupported_characters": [],
            "message": "Texto válido para conversión"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "text" es requerido'
            }), 400
        
        text = data['text']
        is_valid, unsupported = braille_converter.validate_text(text)
        
        return jsonify({
            'success': True,
            'is_valid': is_valid,
            'unsupported_characters': unsupported,
            'message': 'Texto válido para conversión' if is_valid else 'Texto contiene caracteres no soportados'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error en validación: {str(e)}'
        }), 500


# Manejo de errores globales
@braille_bp.errorhandler(404)
def not_found(error):
    """Maneja errores 404."""
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado',
        'message': str(error)
    }), 404


@braille_bp.errorhandler(500)
def internal_error(error):
    """Maneja errores 500."""
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor',
        'message': str(error)
    }), 500
