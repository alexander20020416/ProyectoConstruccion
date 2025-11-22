"""
Tests Unitarios - Sistema Braille
==================================
Casos de prueba para el conversor Braille.

Ejecutar con:
    pytest tests/
    pytest tests/ -v
    pytest tests/ --cov=backend

Autor: GR4
Fecha: Noviembre 2025
"""

import pytest
import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models.braille_converter import BrailleConverter


@pytest.fixture
def converter():
    """Fixture que proporciona una instancia del conversor."""
    return BrailleConverter()


class TestBrailleAlphabet:
    """Tests para el abecedario completo."""
    
    def test_serie_1_letters(self, converter):
        """Test Serie 1: letras a-j."""
        test_cases = {
            'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
            'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚'
        }
        
        for letter, expected_braille in test_cases.items():
            result = converter.text_to_braille(letter)
            assert result == expected_braille, f"Falló conversión de '{letter}'"
    
    def test_serie_2_letters(self, converter):
        """Test Serie 2: letras k-t."""
        test_cases = {
            'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
            'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞'
        }
        
        for letter, expected_braille in test_cases.items():
            result = converter.text_to_braille(letter)
            assert result == expected_braille, f"Falló conversión de '{letter}'"
    
    def test_serie_3_letters(self, converter):
        """Test Serie 3: letras u-z."""
        test_cases = {
            'u': '⠥', 'v': '⠧', 'w': '⠺',
            'x': '⠭', 'y': '⠽', 'z': '⠵'
        }
        
        for letter, expected_braille in test_cases.items():
            result = converter.text_to_braille(letter)
            assert result == expected_braille, f"Falló conversión de '{letter}'"
    
    def test_full_alphabet(self, converter):
        """Test del abecedario completo."""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        result = converter.text_to_braille(alphabet)
        
        # Verificar que no está vacío
        assert len(result) > 0
        
        # Verificar que tiene caracteres Braille Unicode
        assert all(ord(char) >= 0x2800 and ord(char) <= 0x28FF for char in result)


class TestBrailleNumbers:
    """Tests para números."""
    
    def test_single_digits(self, converter):
        """Test números individuales (0-9)."""
        # Números llevan signo de número al inicio
        test_cases = {
            '0': '⠼⠚', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙',
            '5': '⠼⠑', '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊'
        }
        
        for number, expected_braille in test_cases.items():
            result = converter.text_to_braille(number)
            assert result == expected_braille, f"Falló conversión de '{number}'"
    
    def test_multi_digit_number(self, converter):
        """Test números de múltiples dígitos."""
        result = converter.text_to_braille('123')
        # Debe tener signo de número solo al inicio
        assert result.startswith('⠼')
        assert len(result) == 4  # Signo + 3 dígitos
    
    def test_number_with_spaces(self, converter):
        """Test números separados por espacios."""
        result = converter.text_to_braille('12 34')
        # Cada grupo de números debe tener su signo
        braille_parts = result.split('⠀')  # Espacio Braille
        assert len(braille_parts) == 2


class TestBrailleSpecialChars:
    """Tests para caracteres especiales."""
    
    def test_accented_vowels(self, converter):
        """Test vocales acentuadas."""
        test_cases = {
            'á': '⠷', 'é': '⠮', 'í': '⠌',
            'ó': '⠬', 'ú': '⠾'
        }
        
        for char, expected_braille in test_cases.items():
            result = converter.text_to_braille(char)
            assert result == expected_braille, f"Falló conversión de '{char}'"
    
    def test_spanish_special_chars(self, converter):
        """Test caracteres especiales del español."""
        test_cases = {
            'ñ': '⠻',
            'ü': '⠳'
        }
        
        for char, expected_braille in test_cases.items():
            result = converter.text_to_braille(char)
            assert result == expected_braille, f"Falló conversión de '{char}'"
    
    def test_punctuation(self, converter):
        """Test signos de puntuación."""
        punctuation = '.,;:?!'
        result = converter.text_to_braille(punctuation)
        
        # Verificar que se convirtió algo
        assert len(result) > 0


class TestBrailleBidirectional:
    """Tests de conversión bidireccional."""
    
    def test_text_to_braille_to_text(self, converter):
        """Test conversión texto → braille → texto."""
        original_texts = [
            'hola',
            'mundo',
            'python',
            'braille'
        ]
        
        for text in original_texts:
            braille = converter.text_to_braille(text)
            back_to_text = converter.braille_to_text(braille)
            assert back_to_text == text, f"Falló round-trip para '{text}'"
    
    def test_braille_to_text_simple(self, converter):
        """Test conversión braille → texto simple."""
        braille = '⠓⠕⠇⠁'  # 'hola'
        result = converter.braille_to_text(braille)
        assert result == 'hola'
    
    def test_roundtrip_with_spaces(self, converter):
        """Test round-trip con espacios."""
        original = 'hola mundo'
        braille = converter.text_to_braille(original)
        back = converter.braille_to_text(braille)
        assert back == original


class TestBrailleValidation:
    """Tests de validación."""
    
    def test_validate_valid_text(self, converter):
        """Test validación de texto válido."""
        is_valid, unsupported = converter.validate_text('hola mundo 123')
        assert is_valid == True
        assert len(unsupported) == 0
    
    def test_validate_text_with_unsupported_chars(self, converter):
        """Test validación con caracteres no soportados."""
        is_valid, unsupported = converter.validate_text('hola@mundo#')
        assert is_valid == False
        assert '@' in unsupported
        assert '#' in unsupported
    
    def test_validate_empty_text(self, converter):
        """Test validación de texto vacío."""
        is_valid, unsupported = converter.validate_text('')
        assert is_valid == True
        assert len(unsupported) == 0


class TestBrailleInfo:
    """Tests de información de caracteres."""
    
    def test_get_info_letter(self, converter):
        """Test obtener información de una letra."""
        info = converter.get_braille_info('a')
        
        assert info is not None
        assert info['character'] == 'a'
        assert 'dots' in info
        assert 'unicode' in info
        assert info['type'] == 'Serie 1 (a-j)'
    
    def test_get_info_number(self, converter):
        """Test obtener información de un número."""
        info = converter.get_braille_info('5')
        
        assert info is not None
        assert info['character'] == '5'
        assert info['type'] == 'Número'
    
    def test_get_info_accented(self, converter):
        """Test obtener información de vocal acentuada."""
        info = converter.get_braille_info('á')
        
        assert info is not None
        assert info['type'] == 'Vocal acentuada'
    
    def test_get_info_unsupported(self, converter):
        """Test información de carácter no soportado."""
        info = converter.get_braille_info('@')
        assert info is None


class TestBrailleEdgeCases:
    """Tests de casos extremos."""
    
    def test_empty_string(self, converter):
        """Test conversión de cadena vacía."""
        result = converter.text_to_braille('')
        assert result == ''
    
    def test_only_spaces(self, converter):
        """Test solo espacios."""
        result = converter.text_to_braille('   ')
        # Espacios se representan como espacios Braille
        assert len(result) == 3
    
    def test_mixed_case(self, converter):
        """Test texto con mayúsculas y minúsculas."""
        result1 = converter.text_to_braille('Hola')
        result2 = converter.text_to_braille('hola')
        # Braille no distingue mayúsculas
        assert result1 == result2
    
    def test_long_text(self, converter):
        """Test texto largo."""
        long_text = 'a' * 1000
        result = converter.text_to_braille(long_text)
        assert len(result) == 1000
    
    def test_unicode_braille_input(self, converter):
        """Test entrada directa de Unicode Braille."""
        braille = '⠓⠕⠇⠁'
        result = converter.braille_to_text(braille)
        assert result == 'hola'


class TestBrailleComplexScenarios:
    """Tests de escenarios complejos."""
    
    def test_spanish_sentence(self, converter):
        """Test oración completa en español."""
        text = 'España en 2025'
        braille = converter.text_to_braille(text)
        
        # Verificar que tiene contenido
        assert len(braille) > 0
        
        # Verificar round-trip
        back = converter.braille_to_text(braille)
        assert back == text.lower()
    
    def test_mixed_content(self, converter):
        """Test contenido mixto (letras, números, espacios)."""
        text = 'hola mundo 123'
        braille = converter.text_to_braille(text)
        back = converter.braille_to_text(braille)
        
        assert back == text
    
    def test_accented_sentence(self, converter):
        """Test oración con acentos."""
        text = 'está aquí'
        braille = converter.text_to_braille(text)
        
        # Verificar que contiene caracteres Braille
        assert len(braille) > 0


# === TESTS DE INTEGRACIÓN ===

class TestBrailleIntegration:
    """Tests de integración del sistema completo."""
    
    def test_common_phrases(self, converter):
        """Test frases comunes."""
        phrases = [
            'buenos días',
            'gracias',
            'por favor',
            'salida',
            'entrada',
            'ascensor',
        ]
        
        for phrase in phrases:
            braille = converter.text_to_braille(phrase)
            assert len(braille) > 0, f"Falló conversión de '{phrase}'"
    
    def test_signage_numbers(self, converter):
        """Test números para señalética."""
        for i in range(11):  # 0-10
            text = str(i)
            braille = converter.text_to_braille(text)
            assert braille.startswith('⠼'), f"Número {i} no tiene signo de número"


# === EJECUCIÓN DIRECTA ===

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
