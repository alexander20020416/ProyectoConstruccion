# Análisis de Cambio - Requisito 2: Impresión en Espejo para Escritura Manual

## Información del Cambio

| Campo | Valor |
|-------|-------|
| **ID del Requisito** | REQ-V2-002 |
| **Fecha** | Diciembre 2025 |
| **Iteración** | Segunda Iteración |
| **Prioridad** | Alta |
| **Estado** | Completado |

## Descripción del Requisito

Generar impresión en espejo de textos Braille para escritura manual con punzón y regleta.

### Contexto
La escritura Braille manual se realiza de **derecha a izquierda** utilizando:
- **Punzón**: Herramienta puntiaguda para perforar el papel
- **Regleta**: Guía con celdas para mantener el espaciado correcto

Al escribir desde el reverso del papel, el texto queda espejado. Por ello, la hoja guía debe imprimirse en espejo para que al voltear el papel, el texto quede correctamente orientado.

### Transformación Requerida

```
Texto Normal:    H O L A
                 → → → →

Texto Espejo:    A L O H
                 ← ← ← ←

Cada celda también se espeja horizontalmente:
  Normal:  1 • • 4      Espejo:  4 • • 1
           2 • • 5              5 • • 2
           3 • • 6              6 • • 3
```

## Análisis del Impacto

### 1. Componentes Afectados

| Componente | Tipo de Cambio | Impacto |
|------------|----------------|---------|
| `backend/models/braille_converter.py` | Modificación | Alto |
| `backend/utils/pdf_generator.py` | Modificación | Alto |
| `backend/routes/braille_routes.py` | Modificación | Medio |
| `frontend/index.html` | Modificación | Medio |
| `frontend/js/app.js` | Modificación | Medio |
| `frontend/css/styles.css` | Modificación | Bajo |
| `tests/test_braille_converter.py` | Nuevo | Alto |

### 2. Funcionalidades Nuevas Implementadas

#### 2.1 Backend - Funciones de Espejo

**Método 1**: `mirror_braille_dots(dots: tuple) -> tuple`

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

**Método 2**: `text_to_braille_dots_mirror(text: str) -> list`

```python
def text_to_braille_dots_mirror(self, text: str) -> list:
    """
    Convierte texto a puntos Braille en espejo para escritura manual.
    
    El texto se invierte (derecha a izquierda) y cada celda se espeja.
    Esto permite que al escribir con punzón desde el reverso,
    el texto quede correctamente orientado al voltear la hoja.
    
    Args:
        text: Texto en español a convertir
        
    Returns:
        Lista de tuplas de puntos espejados, en orden invertido
    """
```

#### 2.2 Generador de PDF en Espejo

**Método**: `generate_text_pdf_mirror(text: str, filename: str = None) -> str`

Características:
- Título indicando "MODO ESPEJO - Para escritura manual con punzón"
- Subtítulo explicativo: "Texto invertido: escribir de derecha a izquierda"
- Celdas Braille espejadas y en orden invertido
- Nota al pie: "Al voltear la hoja, el texto quedará en orientación correcta"
- Misma calidad y tamaño de puntos que el PDF normal

#### 2.3 Endpoint API Actualizado

**Endpoint**: `POST /api/generate-pdf`

**Nuevo parámetro**: `mirror` (boolean)

```json
{
  "text": "Texto a convertir",
  "mirror": true  // false = normal, true = espejo
}
```

**Respuesta**: Archivo PDF con nombre diferenciado
- Normal: `braille_YYYYMMDD_HHMMSS.pdf`
- Espejo: `braille_espejo_YYYYMMDD_HHMMSS.pdf`

#### 2.4 Frontend - Selector de Modo

Interfaz con radio buttons para seleccionar el tipo de PDF:

```
┌─────────────────────────────────────────┐
│  📄 Tipo de PDF:                        │
│                                         │
│  ○ Normal                               │
│    Para lectura e impresión directa     │
│                                         │
│  ○ 🪞 Espejo                            │
│    Para escritura manual con punzón     │
│    y regleta                            │
│                                         │
│  [Descargar PDF]                        │
└─────────────────────────────────────────┘
```

### 3. Archivos Modificados

#### backend/models/braille_converter.py
- **Líneas añadidas**: ~52
- **Cambios principales**:
  - Método `mirror_braille_dots()`
  - Método `text_to_braille_dots_mirror()`
  - Diccionario de mapeo de espejo

#### backend/utils/pdf_generator.py
- **Líneas añadidas**: ~104
- **Cambios principales**:
  - Método `generate_text_pdf_mirror()`
  - Título y subtítulo para modo espejo
  - Nota explicativa al pie

#### backend/routes/braille_routes.py
- **Líneas añadidas**: ~18
- **Cambios principales**:
  - Parámetro `mirror` en endpoint `/api/generate-pdf`
  - Lógica de selección de generador
  - Nombre de archivo diferenciado

#### frontend/index.html
- **Líneas añadidas**: ~22
- **Cambios principales**:
  - Selector de modo PDF con radio buttons
  - Etiquetas descriptivas para cada modo

#### frontend/js/app.js
- **Líneas añadidas**: ~13
- **Cambios principales**:
  - Obtención del modo seleccionado
  - Envío del parámetro `mirror` al API
  - Mensajes diferenciados según modo

#### frontend/css/styles.css
- **Líneas añadidas**: ~70
- **Cambios principales**:
  - Estilos para `.pdf-mode-selector`
  - Estilos para `.radio-group` y `.radio-option`
  - Estado visual para opción seleccionada

### 4. Tests Implementados

| Clase de Test | Cantidad | Descripción |
|---------------|----------|-------------|
| `TestBrailleMirror` | 10 | Funcionalidad completa de espejo |

**Tests específicos:**

| Test | Descripción |
|------|-------------|
| `test_mirror_single_dot` | Espejo de puntos individuales (1↔4, 2↔5, 3↔6) |
| `test_mirror_multiple_dots` | Espejo de múltiples puntos |
| `test_mirror_empty` | Espejo de tupla vacía (espacio) |
| `test_mirror_capital_sign` | Espejo del indicador de mayúscula |
| `test_mirror_number_sign` | Espejo del indicador de número |
| `test_text_to_braille_dots_mirror_simple` | Texto simple espejado |
| `test_text_to_braille_dots_mirror_with_space` | Texto con espacios espejado |
| `test_mirror_preserves_length` | Longitud preservada |
| `test_double_mirror_returns_original` | Doble espejo = original |
| `test_mirror_full_cell` | Celda completa (simétrica) |

**Total: 10 tests nuevos**

## Estrategia de Implementación

### Fase 1: Backend - Lógica de Espejo
1. Implementar `mirror_braille_dots()` con mapeo 1↔4, 2↔5, 3↔6
2. Implementar `text_to_braille_dots_mirror()` con inversión de orden
3. Crear tests unitarios para espejo

### Fase 2: Backend - Generador PDF
1. Crear `generate_text_pdf_mirror()` basado en `generate_text_pdf()`
2. Agregar título y notas explicativas
3. Usar puntos espejados

### Fase 3: API y Frontend
1. Agregar parámetro `mirror` al endpoint
2. Crear selector de modo en HTML
3. Actualizar JavaScript para enviar parámetro
4. Agregar estilos CSS

## Commits Relacionados

| Hash | Mensaje |
|------|---------|
| `7298838` | style: Mejorar colores según principios HCI y accesibilidad |
| `d2e29ac` | feat: Agregar funciones de espejo para escritura manual Braille |
| `7158829` | feat: Agregar generación de PDF en espejo para punzón y regleta |
| `760a3ad` | feat: Agregar parámetro mirror al endpoint generate-pdf |
| `57f85ef` | feat: Agregar selector de modo PDF normal y espejo en UI |
| `70f7846` | feat: Enviar parámetro mirror según modo seleccionado |
| `1a3539e` | test: Agregar 10 tests para funcionalidad de espejo Braille |

## Diagrama de Transformación

```
ENTRADA: "ab"

PROCESO NORMAL:
  'a' → (1,)     'b' → (1,2)
  
  Resultado: [(1,), (1,2)]
  
  PDF:  [•  ]  [•  ]
        [   ]  [•  ]
        [   ]  [   ]
          a      b

PROCESO ESPEJO:
  1. Invertir orden: 'b', 'a'
  2. Espejar cada celda:
     'b' (1,2) → (4,5)
     'a' (1,)  → (4,)
  
  Resultado: [(4,5), (4,)]
  
  PDF:  [  •]  [  •]
        [  •]  [   ]
        [   ]  [   ]
          b      a
          
AL VOLTEAR LA HOJA:
  [•  ]  [•  ]
  [•  ]  [   ]
  [   ]  [   ]
    a      b     ← Texto correctamente orientado
```

## Resultado

✅ **Requisito completado exitosamente**

El sistema ahora permite:
1. Seleccionar entre modo Normal y Espejo para generación de PDF
2. Generar PDF en espejo con texto invertido y celdas espejadas
3. Incluir instrucciones claras en el PDF para el usuario
4. Verificar la transformación mediante 10 tests automatizados
5. Usar el PDF espejo como guía para escritura manual con punzón y regleta
