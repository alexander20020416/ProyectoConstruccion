# Documentación Técnica del Código Fuente - Segunda Iteración (v2)

## Resumen de Cambios

Esta documentación complementa la versión anterior, detallando los cambios realizados en la segunda iteración del proyecto.

### Nuevas Funcionalidades

1. **Conversión Braille a Español** - Traducción completa con validación
2. **Generación de PDF en Espejo** - Para escritura manual con punzón
3. **Interfaz Mejorada** - Celda interactiva, edición de secuencia
4. **Accesibilidad** - Colores según principios HCI

---

## Backend

### models/braille_converter.py

#### Nuevos Métodos

**`braille_to_text(braille: str) -> dict`**

Convierte Braille Unicode a texto español con validación.

```python
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
```

**Características:**
- Mapeo inverso de puntos a caracteres
- Detección de indicadores de mayúscula y número
- Validación de secuencias inválidas
- Manejo de prioridad en puntuación (? vs ¿, ! vs ¡)

---

**`mirror_braille_dots(dots: tuple) -> tuple`**

Espeja una celda Braille horizontalmente.

```python
def mirror_braille_dots(self, dots: tuple) -> tuple:
    """
    Espeja una celda Braille horizontalmente para escritura manual.
    
    Sistema de puntos:
        Normal:  1 • • 4      Espejo:  4 • • 1
                 2 • • 5              5 • • 2
                 3 • • 6              6 • • 3
    
    Mapeo: 1↔4, 2↔5, 3↔6
    
    Args:
        dots: Tupla de puntos activos (1-6)
        
    Returns:
        Tupla de puntos espejados
    """
```

---

**`text_to_braille_dots_mirror(text: str) -> list`**

Convierte texto a puntos Braille en espejo para escritura manual.

```python
def text_to_braille_dots_mirror(self, text: str) -> list:
    """
    Convierte texto a puntos Braille en espejo.
    
    El texto se invierte (derecha a izquierda) y cada celda se espeja.
    
    Args:
        text: Texto en español a convertir
        
    Returns:
        Lista de tuplas de puntos espejados, en orden invertido
    """
```

#### Nuevas Constantes

```python
# Prioridad de puntuación para conversión inversa
PUNCTUATION_INVERSE_PRIORITY = {
    (2, 6): '?',      # Priorizar ? sobre ¿
    (2, 3, 5): '!',   # Priorizar ! sobre ¡
}
```

---

### routes/braille_routes.py

#### Endpoint Actualizado: `/api/convert/to-text`

**Request:**
```json
{
  "braille": "⠓⠕⠇⠁"
}
```

**Response (éxito):**
```json
{
  "success": true,
  "braille_input": "⠓⠕⠇⠁",
  "text": "hola",
  "valid": true,
  "errors": [],
  "character_count": 4,
  "timestamp": "2025-12-24T..."
}
```

**Response (error de validación):**
```json
{
  "success": true,
  "braille_input": "⠨",
  "text": "",
  "valid": false,
  "errors": ["Indicador de mayúscula sin letra siguiente"],
  "timestamp": "2025-12-24T..."
}
```

---

#### Endpoint Actualizado: `/api/generate-pdf`

**Nuevo parámetro:** `mirror` (boolean)

**Request:**
```json
{
  "text": "Hola mundo",
  "mirror": true
}
```

**Respuesta:** Archivo PDF

- Si `mirror: false` → PDF normal (lectura directa)
- Si `mirror: true` → PDF en espejo (escritura manual)

**Nombres de archivo:**
- Normal: `braille_YYYYMMDD_HHMMSS.pdf`
- Espejo: `braille_espejo_YYYYMMDD_HHMMSS.pdf`

---

### utils/pdf_generator.py

#### Nuevo Método: `generate_text_pdf_mirror()`

```python
def generate_text_pdf_mirror(self, text: str, filename: str = None) -> str:
    """
    Genera un PDF con texto en Braille ESPEJADO para escritura manual.
    
    La escritura manual Braille se realiza de derecha a izquierda,
    por lo que:
    1. El texto completo se invierte (última letra primero)
    2. Cada celda se espeja horizontalmente (puntos 1↔4, 2↔5, 3↔6)
    
    Al voltear la hoja, el texto quedará correctamente orientado.
    
    Args:
        text: Texto a convertir
        filename: Nombre del archivo (opcional)
        
    Returns:
        Ruta del PDF generado
    """
```

**Caracteristicas del PDF en espejo:**
- Titulo: "MODO ESPEJO - Para escritura manual con punzon"
- Subtítulo: "Texto invertido: escribir de derecha a izquierda"
- Celdas Braille espejadas y en orden invertido
- Nota al pie explicativa
- Misma calidad de puntos que PDF normal

---

## Frontend

### index.html

#### Nueva Sección: Panel Braille a Texto

```html
<!-- Braille to Text Mode -->
<div id="braille-to-text-panel" class="conversion-panel">
    <!-- Celda Braille interactiva -->
    <div class="braille-builder">
        <div class="braille-dots-builder" id="braille-dots-builder">
            <!-- 6 puntos clicables -->
        </div>
    </div>
    
    <!-- Botones rápidos -->
    <div class="quick-indicators">
        <button id="btn-add-capital">⠨ Mayúscula</button>
        <button id="btn-add-number">⠼ Número</button>
        <button id="btn-add-punctuation">Puntuación...</button>
    </div>
    
    <!-- Botones de edición -->
    <div class="edit-buttons">
        <button id="btn-insert-before">Insertar antes</button>
        <button id="btn-delete-cell">Eliminar</button>
    </div>
    
    <!-- Secuencia visual -->
    <div id="braille-sequence-display"></div>
</div>
```

#### Nueva Sección: Selector de Modo PDF

```html
<!-- Selector de modo PDF -->
<div class="pdf-mode-selector">
    <label>Tipo de PDF:</label>
    <div class="radio-group">
        <label class="radio-option">
            <input type="radio" name="pdf-mode" value="normal" checked>
            <span class="radio-label">
                <strong>Normal</strong>
                <small>Para lectura e impresión directa</small>
            </span>
        </label>
        <label class="radio-option">
            <input type="radio" name="pdf-mode" value="mirror">
            <span class="radio-label">
                <strong>Espejo</strong>
                <small>Para escritura manual con punzón y regleta</small>
            </span>
        </label>
    </div>
</div>
```

---

### js/app.js

#### Nuevas Variables de Estado

```javascript
// Estado para edición de secuencia
let selectedCellIndex = -1;  // Índice de celda seleccionada (-1 = ninguna)
let insertMode = false;       // true = siguiente celda se inserta, no agrega
```

#### Nuevas Funciones

**`updateSequenceDisplay()`**
```javascript
function updateSequenceDisplay() {
    // Renderiza las celdas Braille con capacidad de selección
    // Muestra índice de cada celda
    // Resalta celda seleccionada
}
```

**`selectCell(index)`**
```javascript
function selectCell(index) {
    // Selecciona/deselecciona una celda para edición
    selectedCellIndex = selectedCellIndex === index ? -1 : index;
}
```

**`deleteSelectedCell()`**
```javascript
function deleteSelectedCell() {
    // Elimina la celda seleccionada de la secuencia
    if (selectedCellIndex >= 0) {
        builderSequence.splice(selectedCellIndex, 1);
    }
}
```

**`insertBeforeSelected()`**
```javascript
function insertBeforeSelected() {
    // Activa modo de inserción
    // La siguiente celda agregada se inserta antes de la seleccionada
    insertMode = true;
}
```

**`showPunctuationModal()` / `closePunctuationModal()`**
```javascript
function showPunctuationModal() {
    // Muestra modal con todos los signos de puntuación disponibles
}
```

**`generatePDF()` (actualizado)**
```javascript
async function generatePDF() {
    const pdfModeRadio = document.querySelector('input[name="pdf-mode"]:checked');
    const isMirror = pdfModeRadio ? pdfModeRadio.value === 'mirror' : false;
    
    const response = await fetch(`${API_BASE_URL}/generate-pdf`, {
        method: 'POST',
        body: JSON.stringify({ 
            text: text,
            mirror: isMirror  // Nuevo parámetro
        })
    });
}
```

---

### css/styles.css

#### Variables CSS Actualizadas (HCI)

```css
:root {
    /* Colores optimizados según principios de IHC:
       - Contraste WCAG 2.1 AA (mínimo 4.5:1)
       - Accesibles para daltonismo
    */
    
    /* Estados semánticos */
    --success-color: #059669;    /* Verde: Contraste 4.6:1 */
    --error-color: #dc2626;      /* Rojo: Contraste 4.5:1 */
    --warning-color: #d97706;    /* Naranja: Contraste 4.5:1 */
    
    /* Texto optimizado */
    --text-secondary: #475569;   /* Mejorado a 5.4:1 (antes 4.0:1) */
    
    /* Focus para accesibilidad de teclado */
    --focus-ring: 0 0 0 3px rgba(37, 99, 235, 0.4);
}
```

#### Nuevos Estilos

**Selector de Modo PDF:**
```css
.pdf-mode-selector { /* Contenedor */ }
.radio-group { /* Flex container */ }
.radio-option { /* Opción individual */ }
.radio-option:has(input:checked) { /* Estado seleccionado */ }
```

**Celdas Seleccionables:**
```css
.braille-cell.selectable { cursor: pointer; }
.braille-cell.selectable:hover { transform: scale(1.05); }
.braille-cell.selected { box-shadow: 0 0 0 3px #3b82f6; }
```

**Mensajes de Error Accesibles:**
```css
.translation-error::before { content: "⚠"; }  /* Ícono para daltonismo */
.status-message.success::before { content: "✓"; }
.status-message.error::before { content: "✕"; }
```

---

## Testing

### tests/test_braille_converter.py

#### Nuevas Clases de Test

| Clase | Tests | Descripción |
|-------|-------|-------------|
| `TestBrailleToSpanish` | 15 | Conversión Braille → Español |
| `TestBrailleToSpanishValidation` | 8 | Validación de secuencias |
| `TestSequenceEditing` | 9 | Edición de secuencia |
| `TestBrailleMirror` | 10 | Funcionalidad de espejo |

**Total tests v2: 42 nuevos (71 total)**

#### Tests de Espejo Destacados

```python
def test_mirror_single_dot(self, converter):
    """Espejo de puntos individuales."""
    assert converter.mirror_braille_dots((1,)) == (4,)
    assert converter.mirror_braille_dots((2,)) == (5,)
    assert converter.mirror_braille_dots((3,)) == (6,)

def test_double_mirror_returns_original(self, converter):
    """Aplicar espejo dos veces devuelve el original."""
    original = (1, 2, 5)
    once = converter.mirror_braille_dots(original)
    twice = converter.mirror_braille_dots(once)
    assert twice == original
```

---

## Diagrama de Flujo: Generación PDF

```
┌─────────────────┐
│ Usuario ingresa │
│     texto       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Selecciona modo │
│ Normal/Espejo   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────────┐
│ mirror = false  │────►│ text_to_braille_dots │
└─────────────────┘     └──────────┬───────────┘
                                   │
┌─────────────────┐     ┌──────────▼───────────┐
│ mirror = true   │────►│text_to_braille_dots_ │
└─────────────────┘     │       mirror         │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │   Generar PDF con    │
                        │   puntos calculados  │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │   Descargar PDF      │
                        └──────────────────────┘
```

---

## Commits de la Segunda Iteración

| Hash | Tipo | Mensaje |
|------|------|---------|
| `94e5744` | feat | Validación de traducciones Braille inválidas |
| `d230682` | feat | Botones rápidos de indicadores y modal |
| `a01c966` | feat | Estilos para modal y celdas seleccionables |
| `b87dabe` | feat | Edición de secuencia Braille |
| `cb281d4` | test | Tests para Braille-Español y edición |
| `7298838` | style | Colores según principios HCI |
| `d2e29ac` | feat | Funciones de espejo para escritura manual |
| `7158829` | feat | Generación de PDF en espejo |
| `760a3ad` | feat | Parámetro mirror en endpoint |
| `57f85ef` | feat | Selector de modo PDF en UI |
| `70f7846` | feat | Envío de parámetro mirror |
| `1a3539e` | test | Tests para funcionalidad de espejo |
