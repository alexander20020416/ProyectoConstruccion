# Documentación Técnica del Código Fuente

## Estructura General del Proyecto

### Backend

#### models/braille_converter.py

Clase principal para conversión bidireccional entre texto español y Braille.

**Clase: BrailleConverter**

```python
class BrailleConverter:
    """
    Conversor bidireccional de texto español a Braille y viceversa.
    
    Implementa las tres series del sistema Braille:
    - Serie 1 (a-j): Letras básicas
    - Serie 2 (k-t): Serie 1 + punto 3
    - Serie 3 (u-z): Serie 1 + puntos 3,6
    """
```

**Métodos principales:**

- `text_to_braille(text, format='unicode')`: Convierte texto español a Braille
  - Parámetros:
    - text (str): Texto a convertir
    - format (str): Formato de salida (unicode, dots, description)
  - Retorna: str - Texto en Braille

- `braille_to_text(braille)`: Convierte Braille a texto español
  - Parámetros:
    - braille (str): Texto en Braille Unicode
  - Retorna: str - Texto en español

- `validate_text(text)`: Valida si el texto puede convertirse
  - Parámetros:
    - text (str): Texto a validar
  - Retorna: tuple(bool, list) - (es_válido, caracteres_no_soportados)

- `get_braille_info(char)`: Obtiene información detallada de un carácter
  - Parámetros:
    - char (str): Carácter a consultar
  - Retorna: dict - Información del carácter

**Constantes:**
- SERIE_1, SERIE_2, SERIE_3: Mapeos de letras a puntos Braille
- ALPHABET: Diccionario completo a-z
- NUMBERS: Mapeo de dígitos 0-9
- PUNCTUATION: Signos de puntuación
- CAPITAL_SIGN: Indicador de mayúscula (4,6)
- NUMBER_SIGN: Indicador numérico (3,4,5,6)

#### routes/braille_routes.py

Define los endpoints HTTP de la API REST.

**Blueprint: braille_bp**

Prefijo: `/api`

**Endpoints:**

1. `GET /api/health`
   - Descripción: Verifica estado del servicio
   - Respuesta: JSON con status, service, version, timestamp

2. `POST /api/convert/to-braille`
   - Descripción: Convierte texto español a Braille
   - Body: `{"text": "...", "format": "unicode"}`
   - Respuesta: JSON con braille, dots_info, character_count

3. `POST /api/convert/to-text`
   - Descripción: Convierte Braille a texto español
   - Body: `{"braille": "⠓⠕⠇⠁"}`
   - Respuesta: JSON con text, character_count

4. `POST /api/generate-signage`
   - Descripción: Genera PDF de señalética
   - Body: `{"title": "...", "items": [...], "format": "elevator"}`
   - Respuesta: Archivo PDF

5. `GET /api/braille/info/<char>`
   - Descripción: Info detallada de carácter
   - Respuesta: JSON con character, dots, unicode

6. `GET /api/history`
   - Descripción: Historial de conversiones
   - Query params: limit, type
   - Respuesta: JSON con array de conversiones

7. `POST /api/validate`
   - Descripción: Valida texto para conversión
   - Body: `{"text": "..."}`
   - Respuesta: JSON con is_valid, unsupported_characters

#### utils/pdf_generator.py

Generación de PDFs con señalética Braille usando ReportLab.

**Clase: BrailleSignagePDFGenerator**

```python
class BrailleSignagePDFGenerator:
    """Generador de PDFs para señalética Braille."""
```

**Métodos:**

- `generate_signage_pdf(title, items, format_type)`: Genera PDF según formato
  - Formatos: elevator, door, label
  - Retorna: str - Ruta del PDF generado

- `generate_elevator_sign(title, items)`: Señalética para ascensores
- `generate_door_sign(title, text)`: Etiquetas de puertas
- `generate_custom_label(title, text, subtitle)`: Etiquetas personalizadas

- `_draw_braille_character(c, x, y, dots, dot_size, spacing)`: Dibuja carácter Braille
  - Círculos de 1.5mm para puntos táctiles
  - Posiciones según sistema 6 puntos (2x3)

#### database/db_manager.py

Gestión de base de datos SQLite.

**Clase: DatabaseManager**

```python
class DatabaseManager:
    """Gestor de base de datos SQLite para el sistema Braille."""
```

**Métodos:**

- `init_database()`: Crea tablas si no existen
- `save_conversion(original_text, braille_text, type)`: Guarda conversión
- `save_pdf_generation(title, file_path, format_type)`: Registra PDF
- `get_conversion_history(limit, conversion_type)`: Obtiene historial
- `get_pdf_history(limit)`: Historial de PDFs
- `get_statistics()`: Estadísticas del sistema
- `delete_old_records(days)`: Limpieza de registros antiguos

**Tablas:**
- conversions: Historial conversiones (id, original_text, braille_text, conversion_type, character_count, created_at)
- pdf_generations: Registro PDFs (id, title, file_path, format_type, file_size, created_at)
- settings: Configuración (key, value, updated_at)

### Frontend

#### index.html

Interfaz de usuario HTML5 con tabs de navegación.

**Secciones:**
- Conversor: Formularios conversión texto-Braille
- Señalética: Generación de PDFs
- Constructor Visual: Interfaz interactiva 6 dots

#### app.js

Lógica cliente JavaScript ES6+.

**Funciones principales:**

- `convertToText()`: Envía Braille al backend para conversión
- `convertToBraille()`: Envía texto español para conversión
- `generatePDF()`: Solicita generación de PDF
- `dotsToUnicode(dots)`: Convierte array de dots a Unicode Braille
- `updateSequenceDisplay()`: Renderiza celdas Braille visuales

**Variables de estado:**
- builderSequence: Array de objetos {dots, unicode}
- currentDots: Set de dots activos en constructor

#### styles.css

Estilos CSS3 con variables y Grid.

**Componentes clave:**
- .braille-dots-builder: Grid 2x3 para constructor visual
- .dot-builder: Círculos interactivos (30px)
- .braille-cell: Visualización celdas Braille
- Variables CSS para temas y colores

### Testing

#### tests/test_braille_converter.py

Suite de pruebas con pytest.

**Tests implementados:**
- test_text_to_braille(): Conversión básica
- test_uppercase(): Indicadores de mayúscula
- test_numbers(): Conversión numérica
- test_punctuation(): Signos de puntuación
- test_braille_to_text(): Conversión inversa
- test_validation(): Validación de caracteres

## Convenciones de Código

### Python
- PEP 8: Guía de estilo oficial
- Docstrings: Formato Google/NumPy
- Type hints: Anotaciones de tipo cuando es posible
- Nombres: snake_case para funciones/variables, PascalCase para clases

### JavaScript
- ES6+: Arrow functions, const/let, template literals
- Nombres: camelCase para funciones/variables
- Comentarios: JSDoc cuando es necesario

### HTML/CSS
- Semantic HTML5: Uso de etiquetas semánticas
- BEM naming: Para clases CSS (opcional)
- Mobile-first: Diseño responsive

## Patrones de Diseño Utilizados

1. Factory Pattern: Función create_app() en run.py
2. Singleton: Instancia global db_manager
3. Blueprint Pattern: Organización modular de rutas Flask
4. Repository Pattern: DatabaseManager abstrae acceso a datos

## Dependencias y Versiones

Ver requirements.txt para lista completa y versiones exactas.

## Configuración

Variables de entorno en archivo .env:
- FLASK_APP: Punto de entrada
- FLASK_ENV: development/production
- SECRET_KEY: Clave secreta Flask
- DATABASE_PATH: Ruta base de datos SQLite
