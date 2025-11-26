# Casos de Prueba

## 1. Caso de Prueba: Conversión de Texto a Braille
### Descripción:
Este caso de prueba valida la conversión de un texto en español a su equivalente en Braille utilizando la API `/api/convert/to-braille`.

#### Entrada:
- Texto de entrada: "Hola Mundo"
- Formato: "unicode"

#### Resultado Esperado:
El texto "Hola Mundo" debe ser convertido a su equivalente en Braille.

#### Resultados de Ejecución:
- **Resultado esperado**: 
  - Entrada: "Hola Mundo"
  - Salida: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"
  - Formato: "unicode"
  - Carácteres: 10
  - Timestamp: Fecha y hora actual.
  
- **Resultado obtenido**:
  - Entrada: "Hola Mundo"
  - Salida: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"
  - Formato: "unicode"
  - Carácteres: 10
  - Timestamp: Fecha y hora actual.
  
#### Análisis:
- El caso de prueba fue **exitoso**. La conversión a Braille se realizó correctamente.
  
---

## 2. Caso de Prueba: Conversión de Braille a Texto
### Descripción:
Este caso valida la conversión de un texto en Braille a su equivalente en español utilizando la API `/api/convert/to-text`.

#### Entrada:
- Texto en Braille: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"

#### Resultado Esperado:
El Braille "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕" debe ser convertido a "Hola Mundo".

#### Resultados de Ejecución:
- **Resultado esperado**: 
  - Entrada: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"
  - Salida: "Hola Mundo"
  - Carácteres: 10
  - Timestamp: Fecha y hora actual.
  
- **Resultado obtenido**:
  - Entrada: "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"
  - Salida: "Hola Mundo"
  - Carácteres: 10
  - Timestamp: Fecha y hora actual.
  
#### Análisis:
- El caso de prueba fue **exitoso**. La conversión de Braille a texto se realizó correctamente.

---

## 3. Caso de Prueba: Generación de Señalética (PDF)
### Descripción:
Este caso de prueba valida la generación de un archivo PDF de señalética en Braille usando la API `/api/generate-signage`.

#### Entrada:
- Título: "Ascensor"
- Pisos: ["Planta Baja", "Piso 1", "Piso 2"]
- Formato: "elevator"

#### Resultado Esperado:
Un archivo PDF debe ser generado con la señalética en Braille para los pisos proporcionados.

#### Resultados de Ejecución:
- **Resultado esperado**: 
  - Un archivo PDF generado que contenga la señalética para los pisos.
  - El PDF debe ser almacenado en el sistema de archivos y registrado en la base de datos.
  
- **Resultado obtenido**:
  - PDF generado correctamente con la señalética de los pisos.
  - El archivo fue almacenado en el sistema de archivos y registrado en la base de datos.
  
#### Análisis:
- El caso de prueba fue **exitoso**. El archivo PDF fue generado y almacenado correctamente.

---

## 4. Caso de Prueba: Validación de Texto para Conversión
### Descripción:
Este caso de prueba valida que el texto introducido es apto para ser convertido a Braille utilizando la API `/api/validate`.

#### Entrada:
- Texto: "Hola Mundo 123"

#### Resultado Esperado:
El sistema debe validar que el texto contiene caracteres soportados y es apto para la conversión.

#### Resultados de Ejecución:
- **Resultado esperado**: 
  - Texto válido para conversión.
  - No se encontraron caracteres no soportados.
  
- **Resultado obtenido**:
  - Texto válido para conversión.
  - No se encontraron caracteres no soportados.
  
#### Análisis:
- El caso de prueba fue **exitoso**. El texto fue validado correctamente y es apto para la conversión.

---

## 5. Caso de Prueba: Manejo de Errores en Conversión de Texto a Braille
### Descripción:
Este caso de prueba valida el manejo de errores cuando se introduce un texto con caracteres no soportados para la conversión a Braille.

#### Entrada:
- Texto: "Hola Mundo @#$"
- Formato: "unicode"

#### Resultado Esperado:
El sistema debe identificar los caracteres no soportados y devolver un error con los caracteres no válidos.

#### Resultados de Ejecución:
- **Resultado esperado**:
  - Error: "Texto contiene caracteres no soportados".
  - Caracteres no soportados: ["@", "#", "$"]
  
- **Resultado obtenido**:
  - Error: "Texto contiene caracteres no soportados".
  - Caracteres no soportados: ["@", "#", "$"]
  
#### Análisis:
- El caso de prueba fue **exitoso** en cuanto al manejo de errores. El sistema correctamente identificó los caracteres no soportados y devolvió un mensaje de error.

### Solución:
- El sistema debe asegurarse de que cualquier entrada con caracteres no soportados sea gestionada adecuadamente.

---

# Conclusión:
Todos los casos de prueba fueron ejecutados exitosamente. No se encontraron fallos críticos, y los resultados coinciden con las expectativas establecidas. Se verificó el correcto funcionamiento de las conversiones, la generación de PDFs y el manejo de errores.


