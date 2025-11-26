# Reporte de Casos de Prueba: API de Conversión Braille

Este documento detalla los casos de prueba ejecutados para validar la funcionalidad de la API de conversión y gestión de Braille. Incluye los endpoints probados, el código del servidor, los datos de entrada y el análisis de los resultados.

## 1. Caso de Prueba: Conversión de Texto a Braille

### Descripción
Este caso de prueba valida la conversión de un texto estándar en español a su equivalente en caracteres Braille Unicode.

### Especificaciones

- **Endpoint**: `/api/convert/to-braille`
- **Método**: POST
- **Entrada**:
  - Texto: `"Hola Mundo"`
  - Formato: `"unicode"`

### Código del Servidor

```python
@braille_bp.route('/convert/to-braille', methods=['POST'])
def convert_to_braille():
    """
    Convierte texto español a Braille.
    """
    data = request.get_json()
    input_text = data['text']
    output_format = data.get('format', 'unicode')

    braille_output = braille_converter.text_to_braille(input_text, output_format)

    return jsonify({
        'success': True,
        'input_text': input_text,
        'braille': braille_output,
        'format': output_format,
        'character_count': len(input_text),
        'timestamp': datetime.now().isoformat()
    }), 200
```
## Resultado de Ejecución

| **Parámetro**         | **Valor**                |
|-----------------------|--------------------------|
| **Entrada**           | `"Hola Mundo"`           |
| **Salida Esperada**   | `"⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"` |
| **Salida Obtenida**   | `"⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"` |
| **Estado**            | Exitoso                  |

**Análisis**: La conversión se realizó correctamente. La longitud de caracteres (10) coincide y el formato unicode fue respetado.

## 2. Caso de Prueba: Conversión de Braille a Texto

### Descripción
Este caso valida la conversión inversa: transformar una cadena de caracteres Braille a texto legible en español.

### Especificaciones

- **Endpoint**: `/api/convert/to-text`
- **Método**: POST
- **Entrada**:
  - Braille: `"⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"`

### Código del Servidor

```python
@braille_bp.route('/convert/to-text', methods=['POST'])
def convert_to_text():
    """
    Convierte Braille Unicode a texto español.
    """
    data = request.get_json()
    braille_input = data['braille']
    
    text_output = braille_converter.braille_to_text(braille_input)

    return jsonify({
        'success': True,
        'braille_input': braille_input,
        'text': text_output,
        'character_count': len(text_output),
        'timestamp': datetime.now().isoformat()
    }), 200
```

## Resultado de Ejecución

| **Parámetro**         | **Valor**                |
|-----------------------|--------------------------|
| **Entrada**           | `"⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"` |
| **Salida Esperada**   | `"Hola Mundo"`           |
| **Salida Obtenida**   | `"Hola Mundo"`           |
| **Estado**            | Exitoso                  |

**Análisis**: El decodificador interpretó correctamente los patrones unicode y devolvió la cadena de texto original sin errores.

## 3. Caso de Prueba: Generación de Señalética (PDF)

### Descripción
Valida la capacidad del sistema para generar un archivo PDF descargable con señalética en Braille basada en una lista de ítems.

### Especificaciones

- **Endpoint**: `/api/generate-signage`
- **Método**: POST
- **Entrada**:
  - Título: `"Ascensor"`
  - Pisos: `["Planta Baja", "Piso 1", "Piso 2"]`
  - Formato: `"elevator"`

### Código del Servidor

```python
@braille_bp.route('/generate-signage', methods=['POST'])
def generate_signage():
    """
    Genera un PDF de señalética Braille.
    """
    data = request.get_json()
    title = data.get('title', 'Señalética Braille')
    items = data.get('items', [])
    signage_format = data.get('format', 'elevator')

    pdf_path = generate_signage_pdf(
        title=title,
        items=items,
        format_type=signage_format
    )

    return send_file(
        pdf_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'senaletica_braille_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )
```

## Resultado de Ejecución

| **Parámetro**         | **Valor**                |
|-----------------------|--------------------------|
| **Resultado Esperado**| Archivo PDF generado con la señalética de los pisos proporcionados. |
| **Resultado Obtenido**| El servidor respondió con un archivo binario (PDF) correctamente estructurado. |
| **Estado**            | Exitoso                  |

**Análisis**: El archivo PDF fue generado, almacenado temporalmente y enviado al cliente correctamente.

## 4. Caso de Prueba: Validación de Texto para Conversión

### Descripción
Verifica que el sistema pueda identificar si un texto de entrada contiene únicamente caracteres soportados por el convertidor Braille.

### Especificaciones

- **Endpoint**: `/api/validate`
- **Método**: POST
- **Entrada**:
  - Texto: `"Hola Mundo 123"`

### Código del Servidor

```python
@braille_bp.route('/validate', methods=['POST'])
def validate_text():
    """
    Valida si un texto puede ser convertido a Braille.
    """
    data = request.get_json()
    text = data['text']
    
    is_valid, unsupported = braille_converter.validate_text(text)

    return jsonify({
        'success': True,
        'is_valid': is_valid,
        'unsupported_characters': unsupported,
        'message': 'Texto válido para conversión' if is_valid else 'Texto contiene caracteres no soportados'
    }), 200

```

## Resultado de Ejecución

| **Verificación**        | **Resultado**                |
|-------------------------|------------------------------|
| **Es Válido**           | True                         |
| **Caracteres No Soportados** | [] (Ninguno)              |
| **Mensaje**             | "Texto válido para conversión" |
| **Estado**              | Exitoso                      |

**Análisis**: El sistema confirmó correctamente que el texto alfanumérico es apto para la conversión.
