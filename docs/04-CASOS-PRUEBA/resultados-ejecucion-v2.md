# Reporte de Casos de Prueba - Segunda Iteración (v2)

Este documento detalla los casos de prueba implementados para validar las nuevas funcionalidades de la segunda iteración.

## Resumen de Tests

| Categoría | Cantidad | Estado |
|-----------|----------|--------|
| Conversión Braille a Español | 15 | ✅ Pasados |
| Validación de Traducciones | 8 | ✅ Pasados |
| Edición de Secuencia | 9 | ✅ Pasados |
| Funcionalidad de Espejo | 10 | ✅ Pasados |
| **Total Nuevos** | **42** | ✅ **Todos pasados** |
| **Total General** | **71** | ✅ **Todos pasados** |

---

## 1. Tests de Conversión Braille a Español

### Clase: `TestBrailleToSpanish`

#### Test 1.1: Letras Simples

```python
def test_single_letters(self, converter):
    """Test conversión de letras individuales."""
    braille_a = '⠁'  # puntos (1,)
    result = converter.braille_to_text(braille_a)
    assert result['text'] == 'a'
    assert result['valid'] == True
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| ⠁ | a | a | ✅ |
| ⠃ | b | b | ✅ |
| ⠉ | c | c | ✅ |

#### Test 1.2: Palabras Completas

```python
def test_word_hola(self, converter):
    """Test palabra 'hola'."""
    braille = '⠓⠕⠇⠁'
    result = converter.braille_to_text(braille)
    assert result['text'] == 'hola'
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| ⠓⠕⠇⠁ | hola | hola | ✅ |
| ⠍⠥⠝⠙⠕ | mundo | mundo | ✅ |

#### Test 1.3: Mayúsculas

```python
def test_capital_letter(self, converter):
    """Test letra mayúscula con indicador."""
    braille = '⠨⠓⠕⠇⠁'  # indicador + h + o + l + a
    result = converter.braille_to_text(braille)
    assert result['text'] == 'Hola'
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| ⠨⠓ | H | H | ✅ |
| ⠨⠁⠨⠃ | AB | AB | ✅ |

#### Test 1.4: Números

```python
def test_numbers(self, converter):
    """Test números con indicador numérico."""
    braille = '⠼⠁⠃⠉'  # #123
    result = converter.braille_to_text(braille)
    assert result['text'] == '123'
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| ⠼⠁ | 1 | 1 | ✅ |
| ⠼⠁⠃⠉ | 123 | 123 | ✅ |
| ⠼⠚ | 0 | 0 | ✅ |

#### Test 1.5: Vocales Acentuadas

```python
def test_accented_vowels(self, converter):
    """Test vocales con acento."""
    result = converter.braille_to_text('⠷')  # á
    assert result['text'] == 'á'
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| ⠷ | á | á | ✅ |
| ⠮ | é | é | ✅ |
| ⠌ | í | í | ✅ |
| ⠬ | ó | ó | ✅ |
| ⠾ | ú | ú | ✅ |

#### Test 1.6: Puntuación

```python
def test_punctuation(self, converter):
    """Test signos de puntuación."""
    result = converter.braille_to_text('⠢')  # punto
    assert result['text'] == '.'
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| ⠢ | . | . | ✅ |
| ⠂ | , | , | ✅ |
| ⠦ | ? | ? | ✅ |
| ⠖ | ! | ! | ✅ |

---

## 2. Tests de Validación de Traducciones

### Clase: `TestBrailleToSpanishValidation`

#### Test 2.1: Indicador de Mayúscula Solo

```python
def test_capital_indicator_alone(self, converter):
    """Indicador de mayúscula sin letra siguiente."""
    result = converter.braille_to_text('⠨')
    assert result['valid'] == False
    assert 'mayúscula' in result['errors'][0].lower()
```

| Entrada | Valid | Error Esperado | Estado |
|---------|-------|----------------|--------|
| ⠨ | False | Indicador de mayúscula sin letra siguiente | ✅ |

#### Test 2.2: Indicador de Número Solo

```python
def test_number_indicator_alone(self, converter):
    """Indicador de número sin dígito siguiente."""
    result = converter.braille_to_text('⠼')
    assert result['valid'] == False
    assert 'número' in result['errors'][0].lower()
```

| Entrada | Valid | Error Esperado | Estado |
|---------|-------|----------------|--------|
| ⠼ | False | Indicador de número sin dígito siguiente | ✅ |

#### Test 2.3: Patrón No Reconocido

```python
def test_unrecognized_pattern(self, converter):
    """Patrón Braille no reconocido."""
    result = converter.braille_to_text('⠿')  # todos los puntos
    assert result['valid'] == False
```

| Entrada | Valid | Estado |
|---------|-------|--------|
| ⠿ | False | ✅ |

#### Test 2.4: Secuencia Parcialmente Válida

```python
def test_partial_valid_sequence(self, converter):
    """Secuencia con parte válida y parte inválida."""
    result = converter.braille_to_text('⠓⠕⠇⠁⠨')  # hola + indicador solo
    assert result['valid'] == False
    assert 'hola' in result['text'].lower()
```

| Entrada | Text | Valid | Estado |
|---------|------|-------|--------|
| ⠓⠕⠇⠁⠨ | hola (parcial) | False | ✅ |

---

## 3. Tests de Edición de Secuencia

### Clase: `TestSequenceEditing`

#### Test 3.1: Eliminar Celda

```python
def test_delete_cell_from_sequence(self, converter):
    """Eliminar una celda de la secuencia."""
    sequence = ['⠓', '⠕', '⠇', '⠁']  # h-o-l-a
    del sequence[1]  # Eliminar 'o'
    
    braille = ''.join(sequence)
    result = converter.braille_to_text(braille)
    assert result['text'] == 'hla'
```

| Secuencia Original | Acción | Resultado | Estado |
|-------------------|--------|-----------|--------|
| h-o-l-a | Eliminar 'o' | hla | ✅ |

#### Test 3.2: Insertar Celda

```python
def test_insert_cell_in_sequence(self, converter):
    """Insertar celda en medio de la secuencia."""
    sequence = ['⠓', '⠇', '⠁']  # h-l-a
    sequence.insert(1, '⠕')  # Insertar 'o'
    
    braille = ''.join(sequence)
    result = converter.braille_to_text(braille)
    assert result['text'] == 'hola'
```

| Secuencia Original | Acción | Resultado | Estado |
|-------------------|--------|-----------|--------|
| h-l-a | Insertar 'o' pos 1 | hola | ✅ |

#### Test 3.3: Insertar Indicador de Mayúscula

```python
def test_insert_capital_indicator(self, converter):
    """Insertar indicador de mayúscula."""
    sequence = ['⠓', '⠕', '⠇', '⠁']
    sequence.insert(0, '⠨')  # Agregar mayúscula al inicio
    
    braille = ''.join(sequence)
    result = converter.braille_to_text(braille)
    assert result['text'] == 'Hola'
```

| Secuencia Original | Acción | Resultado | Estado |
|-------------------|--------|-----------|--------|
| h-o-l-a | Insertar ⠨ pos 0 | Hola | ✅ |

#### Test 3.4: Limpiar Secuencia

```python
def test_clear_sequence(self, converter):
    """Limpiar toda la secuencia."""
    sequence = ['⠓', '⠕', '⠇', '⠁']
    sequence.clear()
    
    braille = ''.join(sequence)
    result = converter.braille_to_text(braille)
    assert result['text'] == ''
```

| Acción | Resultado | Estado |
|--------|-----------|--------|
| Clear | '' (vacío) | ✅ |

---

## 4. Tests de Funcionalidad de Espejo

### Clase: `TestBrailleMirror`

#### Test 4.1: Espejo de Puntos Individuales

```python
def test_mirror_single_dot(self, converter):
    """Espejo de puntos individuales."""
    assert converter.mirror_braille_dots((1,)) == (4,)
    assert converter.mirror_braille_dots((4,)) == (1,)
    assert converter.mirror_braille_dots((2,)) == (5,)
    assert converter.mirror_braille_dots((5,)) == (2,)
    assert converter.mirror_braille_dots((3,)) == (6,)
    assert converter.mirror_braille_dots((6,)) == (3,)
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| (1,) | (4,) | (4,) | ✅ |
| (4,) | (1,) | (1,) | ✅ |
| (2,) | (5,) | (5,) | ✅ |
| (5,) | (2,) | (2,) | ✅ |
| (3,) | (6,) | (6,) | ✅ |
| (6,) | (3,) | (3,) | ✅ |

#### Test 4.2: Espejo de Múltiples Puntos

```python
def test_mirror_multiple_dots(self, converter):
    """Espejo de múltiples puntos."""
    # Letra 'h' = (1,2,5) -> espejo = (2,4,5)
    result = converter.mirror_braille_dots((1, 2, 5))
    assert result == (2, 4, 5)
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| (1,2,5) | (2,4,5) | (2,4,5) | ✅ |
| (1,3,5) | (2,4,6) | (2,4,6) | ✅ |

#### Test 4.3: Espejo de Tupla Vacía

```python
def test_mirror_empty(self, converter):
    """Espejo de tupla vacía (espacio)."""
    assert converter.mirror_braille_dots(tuple()) == tuple()
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| () | () | () | ✅ |

#### Test 4.4: Espejo del Indicador de Mayúscula

```python
def test_mirror_capital_sign(self, converter):
    """Espejo del indicador de mayúscula."""
    # (4,6) -> espejo = (1,3)
    result = converter.mirror_braille_dots((4, 6))
    assert result == (1, 3)
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| (4,6) | (1,3) | (1,3) | ✅ |

#### Test 4.5: Espejo del Indicador de Número

```python
def test_mirror_number_sign(self, converter):
    """Espejo del indicador de número."""
    # (3,4,5,6) -> 3->6, 4->1, 5->2, 6->3 = (1,2,3,6)
    result = converter.mirror_braille_dots((3, 4, 5, 6))
    assert result == (1, 2, 3, 6)
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| (3,4,5,6) | (1,2,3,6) | (1,2,3,6) | ✅ |

#### Test 4.6: Texto Simple Espejado

```python
def test_text_to_braille_dots_mirror_simple(self, converter):
    """Conversión a puntos espejo - texto simple."""
    # 'ab' espejo = [(4,5), (4,)] - invertido y espejado
    result = converter.text_to_braille_dots_mirror('ab')
    assert result == [(4, 5), (4,)]
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| 'ab' | [(4,5), (4,)] | [(4,5), (4,)] | ✅ |

#### Test 4.7: Preservación de Longitud

```python
def test_mirror_preserves_length(self, converter):
    """El espejo preserva la longitud de la secuencia."""
    text = "hola mundo"
    normal = converter.text_to_braille_dots(text)
    mirror = converter.text_to_braille_dots_mirror(text)
    assert len(normal) == len(mirror)
```

| Texto | Longitud Normal | Longitud Espejo | Estado |
|-------|-----------------|-----------------|--------|
| "hola mundo" | 10 | 10 | ✅ |

#### Test 4.8: Doble Espejo Retorna Original

```python
def test_double_mirror_returns_original(self, converter):
    """Aplicar espejo dos veces devuelve el original."""
    original = (1, 2, 5)
    once = converter.mirror_braille_dots(original)
    twice = converter.mirror_braille_dots(once)
    assert twice == original
```

| Original | Una vez | Dos veces | Estado |
|----------|---------|-----------|--------|
| (1,2,5) | (2,4,5) | (1,2,5) | ✅ |

#### Test 4.9: Celda Completa (Simétrica)

```python
def test_mirror_full_cell(self, converter):
    """Espejo de celda completa - es simétrica."""
    full_cell = (1, 2, 3, 4, 5, 6)
    result = converter.mirror_braille_dots(full_cell)
    assert result == full_cell
```

| Entrada | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| (1,2,3,4,5,6) | (1,2,3,4,5,6) | (1,2,3,4,5,6) | ✅ |

---

## Ejecución de Tests

### Comando

```bash
pytest tests/test_braille_converter.py -v
```

### Resultado

```
========================= test session starts ==========================
collected 71 items

tests/test_braille_converter.py::TestBrailleAlphabet::test_serie_1_letters PASSED
tests/test_braille_converter.py::TestBrailleAlphabet::test_serie_2_letters PASSED
tests/test_braille_converter.py::TestBrailleAlphabet::test_serie_3_letters PASSED
...
tests/test_braille_converter.py::TestBrailleMirror::test_mirror_single_dot PASSED
tests/test_braille_converter.py::TestBrailleMirror::test_mirror_multiple_dots PASSED
tests/test_braille_converter.py::TestBrailleMirror::test_double_mirror_returns_original PASSED
tests/test_braille_converter.py::TestBrailleMirror::test_mirror_full_cell PASSED

========================= 71 passed in 0.07s ===========================
```

---

## Conclusiones

✅ **Todos los tests pasan exitosamente**

- 71 tests en total
- 42 tests nuevos para la segunda iteración
- Cobertura completa de nuevas funcionalidades
- Tiempo de ejecución: ~0.07 segundos
