"""
Módulo de Conversión Braille
============================
Implementa la conversión bidireccional entre texto español y Braille
siguiendo el sistema de lectoescritura braille español.

Sistema de numeración de puntos:
    1 • • 4
    2 • • 5
    3 • • 6

Autor: GR4
Fecha: Noviembre 2025
"""

from typing import Dict, List, Tuple, Optional


class BrailleConverter:
    """
    Conversor bidireccional de texto español a Braille y viceversa.
    
    Implementa las tres series del sistema Braille:
    - Serie 1 (a-j): Letras básicas
    - Serie 2 (k-t): Serie 1 + punto 3
    - Serie 3 (u-z): Serie 1 + puntos 3,6
    """
    
    def __init__(self):
        """Inicializa los mapeos de conversión Braille."""
        self._init_alphabet_maps()
        self._init_number_maps()
        self._init_special_chars()
        self._init_unicode_braille()
    
    def _init_alphabet_maps(self):
        """
        Inicializa el mapeo del abecedario español según las tres series.
        Los puntos se representan como tuplas de números (1-6).
        """
        # SERIE 1: Letras a-j (matriz primitiva)
        self.SERIE_1 = {
            'a': (1,),           # •
            'b': (1, 2),         # • •
            'c': (1, 4),         # • 
            'd': (1, 4, 5),      # • • •
            'e': (1, 5),         # •   •
            'f': (1, 2, 4),      # • •
            'g': (1, 2, 4, 5),   # • • • •
            'h': (1, 2, 5),      # • •   •
            'i': (2, 4),         #   • •
            'j': (2, 4, 5),      #   • • •
        }
        
        # SERIE 2: Letras k-t (Serie 1 + punto 3)
        self.SERIE_2 = {
            'k': (1, 3),           # • 
            'l': (1, 2, 3),        # • •
            'm': (1, 3, 4),        # • 
            'n': (1, 3, 4, 5),     # • • •
            'o': (1, 3, 5),        # •   •
            'p': (1, 2, 3, 4),     # • •
            'q': (1, 2, 3, 4, 5),  # • • • •
            'r': (1, 2, 3, 5),     # • •   •
            's': (2, 3, 4),        #   • •
            't': (2, 3, 4, 5),     #   • • •
        }
        
        # SERIE 3: Letras u-z (Serie 1 + puntos 3,6)
        self.SERIE_3 = {
            'u': (1, 3, 6),           # • 
            'v': (1, 2, 3, 6),        # • •
            'x': (1, 3, 4, 6),        # • 
            'y': (1, 3, 4, 5, 6),     # • • •
            'z': (1, 3, 5, 6),        # •   •
        }
        
        # Letra W (añadida posteriormente al braille francés)
        self.EXTRA = {
            'w': (2, 4, 5, 6),        #   • • •
        }
        
        # Combinar todas las series
        self.ALPHABET = {
            **self.SERIE_1,
            **self.SERIE_2,
            **self.SERIE_3,
            **self.EXTRA
        }
    
    def _init_special_chars(self):
        """Inicializa caracteres especiales del español."""
        # Vocales acentuadas
        self.ACCENTED_VOWELS = {
            'á': (1, 2, 3, 5, 6),      # á
            'é': (2, 3, 4, 6),         # é
            'í': (3, 4),               # í
            'ó': (3, 4, 6),            # ó
            'ú': (2, 3, 4, 5, 6),      # ú
        }
        
        # Caracteres adicionales español
        self.SPANISH_SPECIAL = {
            'ñ': (1, 2, 4, 5, 6),      # ñ
            'ü': (1, 2, 5, 6),         # ü
        }
        
        # Signos de puntuación y símbolos
        self.PUNCTUATION = {
            '.': (3,),                 # punto (punto 3 - esquina inferior izquierda)
            ',': (2,),                 # coma
            ';': (2, 3),               # punto y coma
            ':': (2, 5),               # dos puntos
            '?': (2, 6),               # interrogación (cierre)
            '¿': (2, 6),               # interrogación apertura (igual que cierre)
            '!': (2, 3, 5),            # exclamación (cierre)
            '¡': (2, 3, 5),            # exclamación apertura (igual que cierre)
            '-': (3, 6),               # guion / resta
            '−': (3, 6),               # signo menos (matemático)
            '–': (3, 6),               # guion medio (en dash)
            '—': (3, 6),               # guion largo (em dash)
            '_': (3, 6),               # guion bajo (underscore)
            '(': (1, 2, 6),            # paréntesis apertura
            ')': (3, 4, 5),            # paréntesis cierre
            '"': (2, 3, 6),            # comillas
            "'": (3,),                 # apóstrofo
            '=': (2, 3, 5, 6),         # signo igual (4 puntos de abajo)
            '/': (2, 5, 6),            # división (barra)
            '÷': (2, 5, 6),            # división (símbolo)
            '+': (2, 3, 5),            # suma / más
            '×': (2, 3, 6),               # multiplicación
            '*': (2, 3, 6),               # asterisco / multiplicación
            ' ': tuple(),              # espacio en blanco
        }
        
        # Mapeo inverso preferido (para Braille -> Texto)
        # Cuando hay duplicados, se prefiere el carácter de cierre
        self.PUNCTUATION_INVERSE_PRIORITY = {
            (2, 6): '?',    # Preferir ? sobre ¿
            (2, 3, 5): '!', # Preferir ! sobre ¡
            (3,): '.',      # Preferir . sobre '
            (3, 6): '-',    # Preferir - sobre otros guiones
            (2, 5, 6): '/', # Preferir / sobre ÷
            (2, 3, 6): '"', # Preferir " sobre * y ×
        }
        
        # Combinar todos los caracteres especiales
        self.SPECIAL_CHARS = {
            **self.ACCENTED_VOWELS,
            **self.SPANISH_SPECIAL,
            **self.PUNCTUATION
        }
    
    def _init_number_maps(self):
        """
        Inicializa el mapeo de números.
        Los números usan el signo de número seguido de las letras de la serie 1.
        """
        # Signo de número (antepuesto a números)
        self.NUMBER_SIGN = (3, 4, 5, 6)  # ⠼
        
        # Cuadratín (espacio sin puntos - caja vacía)
        self.QUADRATIN = tuple()  # ⠀ (sin puntos)
        
        # Indicador de mayúscula (antepuesto a letras mayúsculas)
        self.CAPITAL_SIGN = (4, 6)  # ⠨ (puntos 4 y 6)
        
        # Números del 0-9 (usan serie 1: a=1, b=2, ..., j=0)
        self.NUMBERS = {
            '1': (1,),           # a
            '2': (1, 2),         # b
            '3': (1, 4),         # c
            '4': (1, 4, 5),      # d
            '5': (1, 5),         # e
            '6': (1, 2, 4),      # f
            '7': (1, 2, 4, 5),   # g
            '8': (1, 2, 5),      # h
            '9': (2, 4),         # i
            '0': (2, 4, 5),      # j
        }
    
    def _init_unicode_braille(self):
        """
        Inicializa el mapeo a Unicode Braille (U+2800 a U+28FF).
        Permite representar Braille en texto usando caracteres Unicode.
        """
        # Caracter base Braille en Unicode (sin puntos)
        self.BRAILLE_UNICODE_BASE = 0x2800
        
        # Mapeo de puntos a offset Unicode
        self.UNICODE_DOTS = {
            1: 0x01, 2: 0x02, 3: 0x04, 4: 0x08,
            5: 0x10, 6: 0x20, 7: 0x40, 8: 0x80
        }
    
    def dots_to_unicode(self, dots: Tuple[int, ...]) -> str:
        """
        Convierte una tupla de puntos a su representación Unicode Braille.
        
        Args:
            dots: Tupla de puntos activos (1-6)
            
        Returns:
            Carácter Unicode Braille
            
        Ejemplo:
            >>> dots_to_unicode((1, 2, 3))
            '⠇'
        """
        if not dots:  # Espacio en blanco
            return '⠀'  # Braille pattern blank
        
        unicode_value = self.BRAILLE_UNICODE_BASE
        for dot in dots:
            if 1 <= dot <= 8:
                unicode_value += self.UNICODE_DOTS[dot]
        
        return chr(unicode_value)
    
    def unicode_to_dots(self, braille_char: str) -> Tuple[int, ...]:
        """
        Convierte un carácter Unicode Braille a tupla de puntos.
        
        Args:
            braille_char: Carácter Unicode Braille
            
        Returns:
            Tupla de puntos activos
        """
        if not braille_char or braille_char == '⠀':
            return tuple()
        
        unicode_value = ord(braille_char) - self.BRAILLE_UNICODE_BASE
        dots = []
        
        for dot_num, dot_value in self.UNICODE_DOTS.items():
            if unicode_value & dot_value:
                dots.append(dot_num)
        
        return tuple(sorted(dots))
    
    def text_to_braille(self, text: str, output_format: str = 'unicode') -> str:
        """
        Convierte texto español a Braille.
        
        Args:
            text: Texto en español a convertir
            output_format: Formato de salida ('unicode', 'dots', 'description')
            
        Returns:
            Texto convertido a Braille según el formato especificado
            
        Ejemplo:
            >>> text_to_braille("Hola")
            '⠨⠓⠀⠕⠇⠁'
            >>> text_to_braille("123")
            '⠼⠁⠃⠉'
        """
        if not text:
            return ""
        
        result = []
        in_number_mode = False
        
        i = 0
        while i < len(text):
            char = text[i]
            char_lower = char.lower()
            
            # Detectar letra mayúscula - agregar indicador antes de cada una
            if char.isupper() and char.isalpha():
                # Agregar indicador de mayúscula antes de la letra
                if output_format == 'unicode':
                    result.append(self.dots_to_unicode(self.CAPITAL_SIGN))
                elif output_format == 'dots':
                    result.append(str(self.CAPITAL_SIGN))
                else:
                    result.append(f"[MAY]")
            
            # Detectar números
            if char.isdigit():
                if not in_number_mode:
                    # Añadir signo de número al inicio
                    if output_format == 'unicode':
                        result.append(self.dots_to_unicode(self.NUMBER_SIGN))
                    elif output_format == 'dots':
                        result.append(str(self.NUMBER_SIGN))
                    else:
                        result.append(f"[NUM]")
                    in_number_mode = True
                
                dots = self.NUMBERS.get(char, tuple())
                
            # Espacio termina modo número
            elif char == ' ':
                in_number_mode = False
                dots = tuple()
                
            # Letras y caracteres especiales
            else:
                # TANTO la coma COMO el punto mantienen el modo numérico si hay dígitos después
                if char in (',', '.')and in_number_mode:
                    if i + 1 < len(text) and text[i + 1].isdigit():
                        dots = self.PUNCTUATION.get(char, tuple())
                    else:
                        in_number_mode = False
                        dots = self.PUNCTUATION.get(char, tuple())
                else:
                    # Cualquier otro carácter termina modo numérico
                    in_number_mode = False
                    # Buscar en abecedario y caracteres especiales (usar minúscula)
                    dots = self.ALPHABET.get(char_lower) or self.SPECIAL_CHARS.get(char_lower)
                    
                    if dots is None:
                        # Carácter no soportado, usar espacio
                        dots = tuple()
            
            # Convertir según formato
            if output_format == 'unicode':
                result.append(self.dots_to_unicode(dots))
            elif output_format == 'dots':
                result.append(str(dots) if dots else '()')
            else:  # description
                result.append(f"{char}={dots}")
            
            i += 1
        
        return ''.join(result) if output_format == 'unicode' else ' '.join(result)
    
    def text_to_braille_dots(self, text: str) -> list:
        """
        Convierte texto español a una lista de tuplas de puntos Braille.
        Útil para renderizado visual o generación de PDFs.
        
        Args:
            text: Texto en español a convertir
            
        Returns:
            Lista de tuplas de puntos, cada tupla representa un carácter Braille
            
        Ejemplo:
            >>> text_to_braille_dots("Hola")
            [(4,6), (1,2,5), (), (1,3,5), (1,), (1,)]
        """
        if not text:
            return []
        
        result = []
        in_number_mode = False
        
        i = 0
        while i < len(text):
            char = text[i]
            char_lower = char.lower()
            
            # Detectar letra mayúscula - agregar indicador antes de cada una
            if char.isupper() and char.isalpha():
                # Agregar indicador de mayúscula antes de la letra
                result.append(self.CAPITAL_SIGN)
            
            # Detectar números
            if char.isdigit():
                if not in_number_mode:
                    # Añadir signo de número al inicio
                    result.append(self.NUMBER_SIGN)
                    in_number_mode = True
                
                dots = self.NUMBERS.get(char, tuple())
                
            # Espacio termina modo número
            elif char == ' ':
                in_number_mode = False
                dots = tuple()
                
            # Letras y caracteres especiales
            else:
                # TANTO la coma COMO el punto mantienen el modo numérico si hay dígitos después
                if char in (',', '.') and in_number_mode:
                    if i + 1 < len(text) and text[i + 1].isdigit():
                        dots = self.PUNCTUATION.get(char, tuple())
                    else:
                        in_number_mode = False
                        dots = self.PUNCTUATION.get(char, tuple())
                else:
                    # Cualquier otro carácter termina modo numérico
                    in_number_mode = False
                    # Buscar en abecedario y caracteres especiales (usar minúscula)
                    dots = self.ALPHABET.get(char_lower) or self.SPECIAL_CHARS.get(char_lower)
                    
                    if dots is None:
                        # Carácter no soportado, usar espacio
                        dots = tuple()
            
            result.append(dots)
            i += 1
        
        return result
    
    def braille_to_text(self, braille: str) -> dict:
        """
        Convierte Braille Unicode a texto español.
        
        Args:
            braille: Texto en Braille Unicode
            
        Returns:
            Diccionario con:
                - text: Texto en español
                - valid: Si la traducción es válida
                - errors: Lista de errores encontrados
            
        Ejemplo:
            >>> braille_to_text("⠓⠕⠇⠁")
            {'text': 'hola', 'valid': True, 'errors': []}
        """
        if not braille:
            return {'text': '', 'valid': True, 'errors': []}
        
        # Crear mapeo inverso completo (letras, vocales acentuadas, ñ, ü)
        inverse_map = {}
        for char, dots in {**self.ALPHABET, **self.SPECIAL_CHARS}.items():
            inverse_map[dots] = char
        
        # Agregar puntuación con prioridad para caracteres preferidos
        for char, dots in self.PUNCTUATION.items():
            if dots not in inverse_map:
                inverse_map[dots] = char
        
        # Aplicar prioridades para signos con duplicados
        for dots, preferred_char in self.PUNCTUATION_INVERSE_PRIORITY.items():
            inverse_map[dots] = preferred_char
        
        # Mapeo inverso de números
        inverse_numbers = {dots: num for num, dots in self.NUMBERS.items()}
        
        result = []
        errors = []
        in_number_mode = False
        next_is_capital = False
        pending_capital = False  # Para detectar indicador sin letra después
        pending_number = False   # Para detectar indicador sin número después
        
        i = 0
        while i < len(braille):
            braille_char = braille[i]
            dots = self.unicode_to_dots(braille_char)
            
            # Detectar indicador de mayúscula
            if dots == self.CAPITAL_SIGN:
                if pending_capital:
                    errors.append(f"Indicador de mayúscula (puntos 4,6) sin letra después en posición {i}")
                next_is_capital = True
                pending_capital = True
                i += 1
                continue
            
            # Detectar signo de número
            if dots == self.NUMBER_SIGN:
                if pending_number:
                    errors.append(f"Indicador de número (puntos 3,4,5,6) sin número después en posición {i}")
                in_number_mode = True
                pending_number = True
                i += 1
                continue
            
            # Espacio termina modo número
            if not dots:
                if pending_capital:
                    errors.append("Indicador de mayúscula (puntos 4,6) seguido de espacio")
                    pending_capital = False
                if pending_number:
                    errors.append("Indicador de número (puntos 3,4,5,6) seguido de espacio")
                    pending_number = False
                in_number_mode = False
                result.append(' ')
                i += 1
                continue
            
            # Limpiar flags de pendientes
            pending_capital = False
            pending_number = False
            
            # Convertir según modo
            if in_number_mode:
                # En modo número: convertir dígitos
                if dots in inverse_numbers:
                    char = inverse_numbers[dots]
                    result.append(char)
                # Coma o punto dentro de números se mantienen en modo número
                elif dots in [self.PUNCTUATION.get(','), self.PUNCTUATION.get('.')]:
                    # Verificar si hay más dígitos después
                    if i + 1 < len(braille):
                        next_dots = self.unicode_to_dots(braille[i + 1])
                        if next_dots in inverse_numbers:
                            # Mantener modo número y agregar el separador
                            char = inverse_map.get(dots, None)
                            if char:
                                result.append(char)
                            else:
                                errors.append(f"Carácter no reconocido (puntos {dots}) en posición {i}")
                        else:
                            # Terminar modo número
                            in_number_mode = False
                            char = inverse_map.get(dots, None)
                            if char:
                                result.append(char)
                            else:
                                errors.append(f"Carácter no reconocido (puntos {dots}) en posición {i}")
                    else:
                        # Fin de cadena, terminar modo número
                        in_number_mode = False
                        char = inverse_map.get(dots, None)
                        if char:
                            result.append(char)
                        else:
                            errors.append(f"Carácter no reconocido (puntos {dots}) en posición {i}")
                else:
                    # Cualquier otro carácter termina el modo número
                    in_number_mode = False
                    char = inverse_map.get(dots, None)
                    if char is None:
                        errors.append(f"Carácter no reconocido (puntos {dots}) en posición {i}")
                    else:
                        if next_is_capital:
                            char = char.upper()
                            next_is_capital = False
                        result.append(char)
            else:
                # Modo normal: convertir letras y símbolos
                char = inverse_map.get(dots, None)
                if char is None:
                    errors.append(f"Carácter no reconocido (puntos {dots}) en posición {i}")
                else:
                    # Aplicar mayúscula si corresponde
                    if next_is_capital:
                        char = char.upper()
                        next_is_capital = False
                    result.append(char)
            
            i += 1
        
        # Verificar indicadores pendientes al final
        if pending_capital:
            errors.append("Indicador de mayúscula (puntos 4,6) al final sin letra")
        if pending_number:
            errors.append("Indicador de número (puntos 3,4,5,6) al final sin número")
        
        text_result = ''.join(result)
        is_valid = len(errors) == 0 and len(text_result) > 0
        
        return {
            'text': text_result,
            'valid': is_valid,
            'errors': errors
        }
    
    def get_braille_info(self, char: str) -> Optional[Dict]:
        """
        Obtiene información detallada sobre un carácter en Braille.
        
        Args:
            char: Carácter a consultar
            
        Returns:
            Diccionario con información del carácter
        """
        char = char.lower()
        
        # Buscar en todos los mapeos
        dots = None
        char_type = None
        
        if char in self.ALPHABET:
            dots = self.ALPHABET[char]
            if char in self.SERIE_1:
                char_type = "Serie 1 (a-j)"
            elif char in self.SERIE_2:
                char_type = "Serie 2 (k-t)"
            elif char in self.SERIE_3:
                char_type = "Serie 3 (u-z)"
            else:
                char_type = "Letra extra"
        elif char in self.SPECIAL_CHARS:
            dots = self.SPECIAL_CHARS[char]
            if char in self.ACCENTED_VOWELS:
                char_type = "Vocal acentuada"
            elif char in self.SPANISH_SPECIAL:
                char_type = "Carácter especial español"
            else:
                char_type = "Signo de puntuación"
        elif char.isdigit():
            dots = self.NUMBERS[char]
            char_type = "Número"
        
        if dots is None:
            return None
        
        return {
            'character': char,
            'type': char_type,
            'dots': dots,
            'unicode': self.dots_to_unicode(dots),
            'description': f"Puntos: {', '.join(map(str, dots))}"
        }
    
    def validate_text(self, text: str) -> Tuple[bool, List[str]]:
        """
        Valida si un texto puede ser convertido completamente a Braille.
        
        Args:
            text: Texto a validar
            
        Returns:
            Tupla (es_válido, lista_de_caracteres_no_soportados)
        """
        text = text.lower()
        unsupported = []
        
        for char in text:
            if char.isdigit():
                continue
            if char in self.ALPHABET or char in self.SPECIAL_CHARS:
                continue
            if char not in unsupported:
                unsupported.append(char)
        
        return (len(unsupported) == 0, unsupported)


# Instancia global para uso en toda la aplicación
braille_converter = BrailleConverter()


if __name__ == "__main__":
    # Pruebas rápidas
    converter = BrailleConverter()
    
    print("=" * 60)
    print("SISTEMA DE CONVERSIÓN BRAILLE - PRUEBAS")
    print("=" * 60)
    
    # Prueba 1: Abecedario
    print("\n1. Abecedario completo:")
    alphabet_text = "abcdefghijklmnopqrstuvwxyz"
    braille_alphabet = converter.text_to_braille(alphabet_text)
    print(f"Texto:   {alphabet_text}")
    print(f"Braille: {braille_alphabet}")
    print(f"Vuelta:  {converter.braille_to_text(braille_alphabet)}")
    
    # Prueba 2: Números
    print("\n2. Números:")
    numbers_text = "12345 67890"
    braille_numbers = converter.text_to_braille(numbers_text)
    print(f"Texto:   {numbers_text}")
    print(f"Braille: {braille_numbers}")
    print(f"Vuelta:  {converter.braille_to_text(braille_numbers)}")
    
    # Prueba 3: Vocales acentuadas
    print("\n3. Vocales acentuadas:")
    accented_text = "aéiou"
    braille_accented = converter.text_to_braille(accented_text)
    print(f"Texto:   {accented_text}")
    print(f"Braille: {braille_accented}")
    
    # Prueba 4: Español completo
    print("\n4. Texto completo:")
    full_text = "Hola España 2025"
    braille_full = converter.text_to_braille(full_text)
    print(f"Texto:   {full_text}")
    print(f"Braille: {braille_full}")
    print(f"Vuelta:  {converter.braille_to_text(braille_full)}")
    
    print("\n" + "=" * 60)
