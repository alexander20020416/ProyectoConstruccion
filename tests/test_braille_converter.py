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
            result = converter.braille_to_text(braille)
            assert result['text'] == text, f"Falló round-trip para '{text}'"
    
    def test_braille_to_text_simple(self, converter):
        """Test conversión braille → texto simple."""
        braille = '⠓⠕⠇⠁'  # 'hola'
        result = converter.braille_to_text(braille)
        assert result['text'] == 'hola'
    
    def test_roundtrip_with_spaces(self, converter):
        """Test round-trip con espacios."""
        original = 'hola mundo'
        braille = converter.text_to_braille(original)
        result = converter.braille_to_text(braille)
        assert result['text'] == original


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
        # Braille SÍ distingue mayúsculas con indicador
        assert result1 != result2  # 'Hola' tiene indicador mayúscula
        assert result1.startswith('⠨')  # Empieza con indicador mayúscula
    
    def test_long_text(self, converter):
        """Test texto largo."""
        long_text = 'a' * 1000
        result = converter.text_to_braille(long_text)
        assert len(result) == 1000
    
    def test_unicode_braille_input(self, converter):
        """Test entrada directa de Unicode Braille."""
        braille = '⠓⠕⠇⠁'
        result = converter.braille_to_text(braille)
        assert result['text'] == 'hola'


class TestBrailleComplexScenarios:
    """Tests de escenarios complejos."""
    
    def test_spanish_sentence(self, converter):
        """Test oración completa en español."""
        text = 'España en 2025'
        braille = converter.text_to_braille(text)
        
        # Verificar que tiene contenido
        assert len(braille) > 0
        
        # Verificar round-trip (mantiene mayúscula)
        result = converter.braille_to_text(braille)
        assert result['text'] == text
    
    def test_mixed_content(self, converter):
        """Test contenido mixto (letras, números, espacios)."""
        text = 'hola mundo 123'
        braille = converter.text_to_braille(text)
        result = converter.braille_to_text(braille)
        
        assert result['text'] == text
    
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


# === TESTS DE BRAILLE A ESPAÑOL ===

class TestBrailleToSpanish:
    """Tests para la conversión de Braille a Español."""
    
    def test_simple_word(self, converter):
        """Test palabra simple: hola."""
        braille = '⠓⠕⠇⠁'  # h-o-l-a
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'hola'
        assert result['errors'] == []
    
    def test_word_with_capital(self, converter):
        """Test palabra con mayúscula: Hola."""
        braille = '⠨⠓⠕⠇⠁'  # mayúscula + h-o-l-a
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'Hola'
    
    def test_numbers(self, converter):
        """Test números: 123."""
        braille = '⠼⠁⠃⠉'  # número + 1-2-3
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == '123'
    
    def test_punctuation(self, converter):
        """Test signos de puntuación."""
        # Coma (punto 2)
        braille = '⠂'
        result = converter.braille_to_text(braille)
        assert result['valid'] == True
        assert result['text'] == ','
        
        # Punto y coma (puntos 2,3)
        braille = '⠆'
        result = converter.braille_to_text(braille)
        assert result['valid'] == True
        assert result['text'] == ';'
    
    def test_sentence_with_space(self, converter):
        """Test oración con espacio."""
        # "hola mundo" en braille
        braille = '⠓⠕⠇⠁⠀⠍⠥⠝⠙⠕'
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'hola mundo'
    
    def test_accented_vowels(self, converter):
        """Test vocales acentuadas."""
        test_cases = [
            ('⠷', 'á'),  # á
            ('⠮', 'é'),  # é  
            ('⠌', 'í'),  # í
            ('⠬', 'ó'),  # ó
            ('⠾', 'ú'),  # ú
        ]
        
        for braille, expected in test_cases:
            result = converter.braille_to_text(braille)
            assert result['valid'] == True
            assert result['text'] == expected, f"Falló: {braille} debería ser {expected}"
    
    def test_special_spanish_chars(self, converter):
        """Test caracteres especiales del español: ñ, ü."""
        # ñ
        braille = '⠻'
        result = converter.braille_to_text(braille)
        assert result['text'] == 'ñ'
        
        # ü
        braille = '⠳'
        result = converter.braille_to_text(braille)
        assert result['text'] == 'ü'


class TestBrailleToSpanishValidation:
    """Tests para validación de errores en Braille a Español."""
    
    def test_capital_indicator_alone(self, converter):
        """Test indicador de mayúscula solo (sin letra después)."""
        braille = '⠨'  # Solo indicador mayúscula (puntos 4,6)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == False
        assert len(result['errors']) > 0
        assert 'mayúscula' in result['errors'][0].lower()
    
    def test_number_indicator_alone(self, converter):
        """Test indicador de número solo (sin número después)."""
        braille = '⠼'  # Solo indicador número (puntos 3,4,5,6)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == False
        assert len(result['errors']) > 0
        assert 'número' in result['errors'][0].lower()
    
    def test_capital_indicator_followed_by_space(self, converter):
        """Test indicador de mayúscula seguido de espacio."""
        braille = '⠨⠀'  # mayúscula + espacio
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == False
        assert len(result['errors']) > 0
    
    def test_number_indicator_followed_by_space(self, converter):
        """Test indicador de número seguido de espacio."""
        braille = '⠼⠀'  # número + espacio
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == False
        assert len(result['errors']) > 0
    
    def test_unrecognized_pattern(self, converter):
        """Test patrón no reconocido (punto 4 solo)."""
        braille = '⠈'  # Solo punto 4 - no existe en español
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == False
        assert len(result['errors']) > 0
        assert 'no reconocido' in result['errors'][0].lower()
    
    def test_multiple_errors(self, converter):
        """Test secuencia con múltiples errores."""
        braille = '⠨⠈⠼'  # mayúscula + punto4 + número
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == False
        assert len(result['errors']) >= 2  # Al menos 2 errores
    
    def test_partial_valid_sequence(self, converter):
        """Test secuencia parcialmente válida."""
        braille = '⠓⠕⠇⠁⠈'  # hola + patrón inválido
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == False
        assert result['text'] == 'hola'  # Parte válida
        assert len(result['errors']) > 0
    
    def test_empty_input(self, converter):
        """Test entrada vacía."""
        result = converter.braille_to_text('')
        
        assert result['valid'] == True
        assert result['text'] == ''
        assert result['errors'] == []
    
    def test_only_spaces(self, converter):
        """Test solo espacios."""
        braille = '⠀⠀⠀'  # Tres espacios braille
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == '   '


class TestBrailleRoundTrip:
    """Tests de ida y vuelta (español -> braille -> español)."""
    
    def test_roundtrip_lowercase(self, converter):
        """Test ida y vuelta con minúsculas."""
        original = 'hola mundo'
        braille = converter.text_to_braille(original)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == original
    
    def test_roundtrip_with_capital(self, converter):
        """Test ida y vuelta con mayúscula."""
        original = 'Hola'
        braille = converter.text_to_braille(original)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == original
    
    def test_roundtrip_numbers(self, converter):
        """Test ida y vuelta con números."""
        original = '12345'
        braille = converter.text_to_braille(original)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == original
    
    def test_roundtrip_mixed(self, converter):
        """Test ida y vuelta con contenido mixto."""
        original = 'sala 101'
        braille = converter.text_to_braille(original)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == original
    
    def test_roundtrip_accents(self, converter):
        """Test ida y vuelta con acentos."""
        original = 'está aquí'
        braille = converter.text_to_braille(original)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == original
    
    def test_roundtrip_special_spanish(self, converter):
        """Test ida y vuelta con ñ."""
        original = 'españa'
        braille = converter.text_to_braille(original)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == original


# === TESTS DE EDICIÓN DE SECUENCIA (Simulación Backend) ===

class TestSequenceEditing:
    """
    Tests para validar operaciones de edición de secuencia Braille.
    Estos tests simulan las operaciones que el frontend realiza.
    """
    
    def test_delete_cell_from_sequence(self, converter):
        """Test eliminar una celda de una secuencia."""
        # Simular secuencia: h-o-l-a
        sequence = ['⠓', '⠕', '⠇', '⠁']
        
        # Eliminar 'l' (índice 2)
        del sequence[2]
        
        # Convertir secuencia resultante
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'hoa'  # h-o-a sin la 'l'
    
    def test_insert_cell_in_sequence(self, converter):
        """Test insertar una celda en medio de una secuencia."""
        # Simular secuencia: h-o-a (falta 'l')
        sequence = ['⠓', '⠕', '⠁']
        
        # Insertar 'l' en posición 2
        sequence.insert(2, '⠇')
        
        # Convertir secuencia resultante
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'hola'
    
    def test_insert_capital_indicator(self, converter):
        """Test insertar indicador de mayúscula al inicio."""
        # Simular secuencia: h-o-l-a (minúscula)
        sequence = ['⠓', '⠕', '⠇', '⠁']
        
        # Insertar indicador de mayúscula al inicio
        sequence.insert(0, '⠨')  # puntos 4,6
        
        # Convertir secuencia resultante
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'Hola'  # Con mayúscula
    
    def test_insert_number_indicator(self, converter):
        """Test insertar indicador de número antes de dígitos."""
        # Simular secuencia: a-b-c (que son 1-2-3 sin indicador)
        sequence = ['⠁', '⠃', '⠉']
        
        # Insertar indicador de número al inicio
        sequence.insert(0, '⠼')  # puntos 3,4,5,6
        
        # Convertir secuencia resultante
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == '123'  # Ahora son números
    
    def test_delete_first_cell(self, converter):
        """Test eliminar la primera celda."""
        # Simular secuencia con mayúscula: ⠨-h-o-l-a
        sequence = ['⠨', '⠓', '⠕', '⠇', '⠁']
        
        # Eliminar indicador de mayúscula (índice 0)
        del sequence[0]
        
        # Convertir secuencia resultante
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'hola'  # Sin mayúscula
    
    def test_delete_last_cell(self, converter):
        """Test eliminar la última celda."""
        # Simular secuencia: h-o-l-a-s
        sequence = ['⠓', '⠕', '⠇', '⠁', '⠎']
        
        # Eliminar última celda
        del sequence[-1]
        
        # Convertir secuencia resultante
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'hola'
    
    def test_multiple_edits(self, converter):
        """Test múltiples ediciones en secuencia."""
        # Empezar con: h-l-a (falta 'o')
        sequence = ['⠓', '⠇', '⠁']
        
        # Insertar 'o' en posición 1
        sequence.insert(1, '⠕')
        
        # Agregar 's' al final
        sequence.append('⠎')
        
        # Convertir
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'holas'
        
        # Eliminar 's'
        del sequence[-1]
        
        # Insertar indicador mayúscula al inicio
        sequence.insert(0, '⠨')
        
        # Convertir de nuevo
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'Hola'
    
    def test_clear_sequence(self, converter):
        """Test limpiar toda la secuencia."""
        sequence = ['⠓', '⠕', '⠇', '⠁']
        
        # Limpiar
        sequence.clear()
        
        # Verificar vacía
        assert len(sequence) == 0
        
        # Convertir vacío
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == ''
    
    def test_replace_cell(self, converter):
        """Test reemplazar una celda (eliminar + insertar)."""
        # Simular secuencia: h-o-l-a
        sequence = ['⠓', '⠕', '⠇', '⠁']
        
        # Reemplazar 'o' por 'a' en posición 1
        sequence[1] = '⠁'
        
        # Convertir
        braille = ''.join(sequence)
        result = converter.braille_to_text(braille)
        
        assert result['valid'] == True
        assert result['text'] == 'hala'


# === EJECUCIÓN DIRECTA ===

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
