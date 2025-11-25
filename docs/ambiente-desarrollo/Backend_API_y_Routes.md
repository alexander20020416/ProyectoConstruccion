

## `Backend_API_y_Routes`


````
Responsabilidades

1.1 Documentación de Endpoints de la API

La API REST del sistema Braille está implementada utilizando Flask y se encuentra definida en:

backend/routes/braille_routes.py

Todos los endpoints utilizan el prefijo:

/api
````

Todos los endpoints utilizan el prefijo:

```text
/api
```

Desde este archivo se controlan todas las operaciones de:

* Conversión de texto a Braille
* Conversión de Braille a texto
* Generación de señalética en PDF
* Validación de texto
* Consulta de historial
* Consulta de información de caracteres Braille

---

### 1.2 Comunicación Backend – Frontend

La comunicación entre el backend y el frontend se realiza mediante peticiones HTTP usando `fetch` desde el archivo:

```text
frontend/js/app.js
```

**Flujo de comunicación:**

1. El usuario ingresa información en la interfaz web (`frontend/index.html`).
2. El frontend envía solicitudes HTTP (GET o POST) a la API.
3. El backend recibe la solicitud en:

   ```text
   backend/routes/braille_routes.py
   ```
4. Se procesa la información usando:

   * `backend/models/braille_converter.py`
   * `backend/utils/pdf_generator.py`
   * `backend/database/db_manager.py`
5. El backend responde en formato **JSON** o devuelve un archivo PDF.
6. El frontend recibe la respuesta y actualiza la interfaz.

---

### 1.3 Manejo de errores

El sistema implementa manejo de errores mediante:

* Validaciones en cada endpoint.
* Bloques `try-except`.
* Manejadores globales de errores.

**Códigos de estado HTTP utilizados:**

| Código | Significado                                     |
| ------ | ----------------------------------------------- |
| 400    | Error de petición (datos faltantes o inválidos) |
| 404    | Recurso o endpoint no encontrado                |
| 500    | Error interno del servidor                      |

**Ejemplo de respuesta de error:**

```json
{
  "success": false,
  "error": "Campo \"text\" es requerido"
}
```

---

## 2. Documentación requerida

---

## 2.1 Descripción de cada Endpoint

---

### ✅ 1. Estado del servidor

**URL:**
`GET /api/health`

**Descripción:**
Comprueba que el servidor esté activo.

**Respuesta:**

```json
{
  "status": "healthy",
  "service": "Braille Converter API",
  "version": "1.0.0"
}
```

---

### ✅ 2. Convertir texto a Braille

**URL:**
`POST /api/convert/to-braille`

**Parámetros de entrada:**

```json
{
  "text": "Hola mundo",
  "format": "unicode"
}
```

**Respuesta:**

```json
{
  "success": true,
  "input_text": "Hola mundo",
  "braille": "⠓⠕⠇⠁ ⠍⠥⠝⠙⠕"
}
```

---

### ✅ 3. Convertir Braille a texto

**URL:**
`POST /api/convert/to-text`

**Parámetros:**

```json
{
  "braille": "⠓⠕⠇⠁"
}
```

**Respuesta:**

```json
{
  "success": true,
  "braille_input": "⠓⠕⠇⠁",
  "text": "hola"
}
```

---

### ✅ 4. Información de un carácter

**URL:**
`GET /api/braille/info/<char>`

**Ejemplo:**

```
GET /api/braille/info/a
```

**Respuesta:**

```json
{
  "success": true,
  "character": "a",
  "unicode": "⠁",
  "dots": [1]
}
```

---

### ✅ 5. Generar señalética en PDF

**URL:**
`POST /api/generate-signage`

**Parámetros:**

```json
{
  "title": "Ascensor",
  "items": [
    {"text": "Piso 1", "number": "1"}
  ]
}
```

**Respuesta:**
Se descarga un archivo **PDF** con la señalética generada.

---

### ✅ 6. Historial de conversiones

**URL:**
`GET /api/history`

**Parámetros por URL:**

| Parámetro | Descripción                |
| --------- | -------------------------- |
| limit     | Número máximo de registros |
| type      | Tipo de conversión         |

**Respuesta:**

```json
{
  "success": true,
  "history": [],
  "count": 0
}
```

---

### ✅ 7. Validar texto

**URL:**
`POST /api/validate`

**Parámetros:**

```json
{
  "text": "Hola123"
}
```

**Respuesta:**

```json
{
  "success": true,
  "is_valid": true,
  "unsupported_characters": []
}
```

---

## 2.2 Ejemplos de solicitudes y respuestas

**Solicitud:**

```http
POST /api/convert/to-braille
```

```json
{
  "text": "Braille"
}
```

**Respuesta:**

```json
{
  "success": true,
  "braille": "⠃⠗⠁⠊⠇⠇⠑"
}
```

---

## 2.3 Gestión de errores y respuestas

**Errores controlados:**

| Código | Causa                                |
| ------ | ------------------------------------ |
| 400    | Datos incompletos o formato inválido |
| 404    | Endpoint o recurso no encontrado     |
| 500    | Error interno del servidor           |

**Ejemplo de error:**

```json
{
  "success": false,
  "error": "Error en conversión"
}
```

---

## 3. Archivos relevantes

Los endpoints se encuentran en:

```text
backend/routes/braille_routes.py
```

Archivos relacionados:

| Archivo                               | Función                 |
| ------------------------------------- | ----------------------- |
| `backend/models/braille_converter.py` | Conversión Braille      |
| `backend/utils/pdf_generator.py`      | Generación de PDFs      |
| `backend/database/db_manager.py`      | Manejo de base de datos |

---


