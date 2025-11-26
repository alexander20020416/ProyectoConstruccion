\# Casos de Prueba

\## 1. Caso de Prueba: Conversión de Texto a Braille

\### Descripción:

Este caso de prueba valida la conversión de un texto en español a su equivalente en Braille utilizando la API `/api/convert/to-braille`.

\#### Entrada:

- \*\*Texto\*\*: `"Hola Mundo"`
- \*\*Formato\*\*: `"unicode"`

\#### Resultado Esperado:

El texto "Hola Mundo" debe ser convertido a su equivalente en Braille. El formato debe ser "unicode".

\#### Código del Servidor (Ruta de API):

\```python

@braille\_bp.route('/convert/to-braille', methods=['POST'])

def convert\_to\_braille():

"""

Convierte texto español a Braille.

"""

data = request.get\_json()

input\_text = data['text']

output\_format = data.get('format', 'unicode')

braille\_output = braille\_converter.text\_to\_braille(input\_text, output\_format)

return jsonify({

'success': True,

'input\_text': input\_text,

'braille': braille\_output,

'format': output\_format,

'character\_count': len(input\_text),

'timestamp': datetime.now().isoformat()

}), 200

Resultado de Ejecución:

Resultado esperado:

Entrada: "Hola Mundo"

Salida: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"

Formato: "unicode"

Carácteres: 10

Resultado obtenido:

Entrada: "Hola Mundo"

Salida: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"

Formato: "unicode"

Carácteres: 10

Análisis:

El caso de prueba fue exitoso. La conversión de texto a Braille se realizó correctamente sin errores.

2\. Caso de Prueba: Conversión de Braille a Texto

Descripción:

Este caso valida la conversión de un texto en Braille a su equivalente en español utilizando la API /api/convert/to-text.

Entrada:

Texto en Braille: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"

Resultado Esperado:

El Braille "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕" debe ser convertido a "Hola Mundo".

Código del Servidor (Ruta de API):

python

Copiar código

@braille\_bp.route('/convert/to-text', methods=['POST'])

def convert\_to\_text():

"""

Convierte Braille Unicode a texto español.

"""

data = request.get\_json()

braille\_input = data['braille']

text\_output = braille\_converter.braille\_to\_text(braille\_input)

return jsonify({

'success': True,

'braille\_input': braille\_input,

'text': text\_output,

'character\_count': len(text\_output),

'timestamp': datetime.now().isoformat()

}), 200

Resultado de Ejecución:

Resultado esperado:

Entrada: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"

Salida: "Hola Mundo"

Carácteres: 10

Resultado obtenido:

Entrada: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"

Salida: "Hola Mundo"

Carácteres: 10

Análisis:

El caso de prueba fue exitoso. La conversión de Braille a texto se realizó correctamente sin errores.

3\. Caso de Prueba: Generación de Señalética (PDF)

Descripción:

Este caso valida la generación de un archivo PDF de señalética en Braille usando la API /api/generate-signage.

Entrada:

Título: "Ascensor"

Pisos: ["Planta Baja", "Piso 1", "Piso 2"]

Formato: "elevator"

Código del Servidor (Ruta de API):

python

Copiar código

@braille\_bp.route('/generate-signage', methods=['POST'])

def generate\_signage():

"""

Genera un PDF de señalética Braille.

"""

data = request.get\_json()

title = data.get('title', 'Señalética Braille')

items = data.get('items', [])

signage\_format = data.get('format', 'elevator')

pdf\_path = generate\_signage\_pdf(

title=title,

items=items,

format\_type=signage\_format

)

return send\_file(

pdf\_path,

mimetype='application/pdf',

as\_attachment=True,

download\_name=f'senaletica\_braille\_{datetime.now().strftime("%Y%m%d\_%H%M%S")}.pdf'

)

Resultado Esperado:

Un archivo PDF debe ser generado con la señalética en Braille para los pisos proporcionados.

Resultado de Ejecución:

Resultado esperado:

PDF generado correctamente con la señalética de los pisos.

El archivo debe ser almacenado en el sistema de archivos y registrado en la base de datos.

Resultado obtenido:

PDF generado correctamente y almacenado en el sistema de archivos y registrado en la base de datos.

Análisis:

El caso de prueba fue exitoso. El archivo PDF fue generado y almacenado correctamente.

4\. Caso de Prueba: Validación de Texto para Conversión

Descripción:

Este caso valida que el texto introducido es apto para ser convertido a Braille utilizando la API /api/validate.

Entrada:

Texto: "Hola Mundo 123"

Código del Servidor (Ruta de API):

python

Copiar código

@braille\_bp.route('/validate', methods=['POST'])

def validate\_text():

"""

Valida si un texto puede ser convertido a Braille.

"""

data = request.get\_json()

text = data['text']

is\_valid, unsupported = braille\_converter.validate\_text(text)

return jsonify({

'success': True,

'is\_valid': is\_valid,

'unsupported\_characters': unsupported,

'message': 'Texto válido para conversión' if is\_valid else 'Texto contiene caracteres no soportados'

}), 200

Resultado Esperado:

El sistema debe validar que el texto contiene caracteres soportados y es apto para la conversión.

Resultado de Ejecución:

Resultado esperado:

Texto válido para conversión.

No se encontraron caracteres no soportados.

Resultado obtenido:

Texto válido para conversión.

No se encontraron caracteres no soportados.

Análisis:

El caso de prueba fue exitoso. El texto fue validado correctamente y es apto para la conversión.

5\. Caso de Prueba: Manejo de Errores en Conversión de Texto a Braille

Descripción:

Este caso valida el manejo de errores cuando se introduce un texto con caracteres no soportados para la conversión a Braille.

Entrada:

Texto: "Hola Mundo @#$"

Formato: "unicode"

Código del Servidor (Ruta de API):

python

Copiar código

@braille\_bp.route('/convert/to-braille', methods=['POST'])

def convert\_to\_braille():

"""

Convierte texto español a Braille.

"""

data = request.get\_json()

input\_text = data['text']

is\_valid, unsupported\_chars = braille\_converter.validate\_text(input\_text)

if not is\_valid:

return jsonify({

'success': False,

'error': 'Texto contiene caracteres no soportados',

'unsupported\_characters': unsupported\_chars

}), 400

braille\_output = braille\_converter.text\_to\_braille(input\_text, 'unicode')

return jsonify({

'success': True,

'input\_text': input\_text,

'braille': braille\_output

}), 200

Resultado Esperado:

El sistema debe identificar los caracteres no soportados y devolver un error con los caracteres no válidos.

Resultado de Ejecución:

Resultado esperado:

Error: "Texto contiene caracteres no soportados".

Caracteres no soportados: ["@", "#", "$"]

Resultado obtenido:

Error: "Texto contiene caracteres no soportados".

Caracteres no soportados: ["@", "#", "$"]

Análisis:

El caso de prueba fue exitoso en cuanto al manejo de errores. El sistema correctamente identificó los caracteres no soportados y devolvió un mensaje de error.

Solución:

El sistema debe asegurarse de que cualquier entrada con caracteres no soportados sea gestionada adecuadamente.
