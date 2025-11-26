# Diseño Arquitectónico de Alto Nivel
## Sistema de Transcripción Braille

**Versión:** 1.0.0  
**Fecha:** Noviembre 2025  
**Autor:** GR4

---

## 1. Visión General del Sistema

El Sistema de Transcripción Braille es una aplicación web que permite:
- ✅ Conversión bidireccional Español ↔ Braille
- ✅ Generación de señalética táctil en PDF
- ✅ Constructor visual interactivo de caracteres Braille
- ✅ Historial de conversiones y registros

### Tecnologías Principales

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Backend** | Python + Flask | 3.12 + 3.0.0 |
| **Frontend** | HTML5 + CSS3 + JS | Vanilla |
| **Base de Datos** | SQLite | 3.x |
| **Generación PDF** | ReportLab | 4.0.7 |
| **Testing** | pytest | 7.4.3 |

---

## 2. Diagrama de Arquitectura de Alto Nivel

El diagrama PlantUML completo se encuentra en:
📄 **`docs/arquitectura/arquitectura-alto-nivel.puml`**

Para visualizarlo:
1. **VS Code:** Instalar extensión "PlantUML"
2. **Online:** https://www.plantuml.com/plantuml/
3. **Comando:** `plantuml arquitectura-alto-nivel.puml`

### Estructura de Capas

```
┌─────────────────────────────────────────────────────┐
│         USUARIO (Navegador Web)                     │
└─────────────────┬───────────────────────────────────┘
                  │ HTTP/JSON
┌─────────────────▼───────────────────────────────────┐
│   CAPA DE PRESENTACIÓN (Frontend)                   │
│   • index.html - Interfaz de usuario                │
│   • styles.css - Diseño visual (Grid 2×3)           │
│   • app.js - Lógica cliente (Fetch API)             │
└─────────────────┬───────────────────────────────────┘
                  │ API REST
┌─────────────────▼───────────────────────────────────┐
│   CAPA DE APLICACIÓN (Backend Flask)                │
│   ┌──────────────────────────────────────────────┐  │
│   │ run.py - Factory Pattern, CORS, Blueprints  │  │
│   └──────────────────────────────────────────────┘  │
│   ┌──────────────────────────────────────────────┐  │
│   │ routes/braille_routes.py - 7 Endpoints API   │  │
│   └──────────────────────────────────────────────┘  │
│   ┌──────────────────────────────────────────────┐  │
│   │ models/braille_converter.py - Lógica Braille│  │
│   │   • 3 Series (a-j, k-t, u-z)                 │  │
│   │   • Indicadores: Mayúscula (4,6), Número     │  │
│   │   • Conversión bidireccional                 │  │
│   └──────────────────────────────────────────────┘  │
│   ┌──────────────────────────────────────────────┐  │
│   │ utils/pdf_generator.py - ReportLab           │  │
│   │   • Círculos 1.5mm (táctil)                  │  │
│   │   • Formatos: ascensor, puerta, etiqueta     │  │
│   └──────────────────────────────────────────────┘  │
│   ┌──────────────────────────────────────────────┐  │
│   │ database/db_manager.py - Gestor SQLite       │  │
│   │   • Historial, PDFs, Configuración           │  │
│   └──────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│   CAPA DE DATOS                                     │
│   • braille_system.db (SQLite)                      │
│     - conversions (historial)                       │
│     - pdf_generations (registros)                   │
│     - settings (configuración)                      │
│   • output/ (PDFs generados)                        │
└─────────────────────────────────────────────────────┘
```

---

## 3. Componentes Principales

### 3.1 Frontend (Capa de Presentación)

#### **index.html**
- Estructura semántica HTML5
- Tabs de navegación (Conversor, Señalética, Historial)
- Constructor visual Braille (6 dots interactivos)
- Formularios de conversión

#### **styles.css**
- Grid 2×3 para celdas Braille
- Variables CSS para temas
- Diseño responsive (mobile-first)
- Efectos hover en dots

#### **app.js**
- Fetch API para comunicación backend
- Gestión de estado (builderSequence)
- Funciones clave:
  - `convertToText()` - Braille→Español
  - `convertToBraille()` - Español→Braille
  - `dotsToUnicode()` - Conversión dots a Unicode
  - `updateSequenceDisplay()` - Renderizado visual

---

### 3.2 Backend (Capa de Aplicación)

#### **run.py** - Punto de Entrada
```python
create_app()  # Factory Pattern
├── Configuración Flask
├── CORS para /api/*
├── Registro de blueprints
├── Error handlers (404, 500)
└── Inicialización DB
```

#### **braille_routes.py** - API REST

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/health` | GET | Estado del servicio |
| `/api/convert/to-braille` | POST | Español → Braille Unicode |
| `/api/convert/to-text` | POST | Braille → Español |
| `/api/generate-signage` | POST | Genera PDF señalética |
| `/api/braille/info/<char>` | GET | Info de carácter |
| `/api/history` | GET | Historial conversiones |
| `/api/validate` | POST | Valida texto |

#### **braille_converter.py** - Modelo de Negocio

**Mapeos Braille:**
```python
SERIE_1 = {'a': (1,), 'b': (1,2), ...}      # a-j
SERIE_2 = {'k': (1,3), 'l': (1,2,3), ...}   # k-t
SERIE_3 = {'u': (1,3,6), 'v': (1,2,3,6)...} # u-z
CAPITAL_SIGN = (4,6)      # Indicador mayúscula
NUMBER_SIGN = (3,4,5,6)   # Indicador numérico
```

**Métodos Clave:**
- `text_to_braille(text, format='unicode')` - Convierte a Braille
- `braille_to_text(braille)` - Reconoce indicadores
- `text_to_braille_dots(text)` - Retorna lista de tuplas para PDF
- `validate_text(text)` - Verifica caracteres soportados

#### **pdf_generator.py** - Generación de Señalética

```python
BrailleSignagePDFGenerator
├── generate_elevator_sign()      # Números de pisos
├── generate_door_sign()          # Etiquetas puertas
├── generate_custom_label()       # Etiqueta personalizada
└── _draw_braille_character()     # Círculos 1.5mm táctiles
```

**Características PDF:**
- Círculos de 1.5mm (norma táctil)
- Espaciado 6mm entre puntos
- Subtítulos en Braille incluidos
- Sin renderizado de espacios vacíos

#### **db_manager.py** - Gestor de Base de Datos

```python
DatabaseManager (Singleton)
├── init_database()              # Crea tablas
├── save_conversion()            # Guarda historial
├── save_pdf_generation()        # Registra PDFs
├── get_conversion_history()     # Consulta historial
└── get_statistics()             # Métricas agregadas
```

---

### 3.3 Base de Datos (SQLite)

#### Esquema de Tablas

**conversions** (Historial de Conversiones)
```sql
CREATE TABLE conversions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_text TEXT NOT NULL,
    braille_text TEXT NOT NULL,
    conversion_type TEXT NOT NULL,  -- text_to_braille | braille_to_text
    character_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_conversions_type ON conversions(conversion_type);
CREATE INDEX idx_conversions_date ON conversions(created_at DESC);
```

**pdf_generations** (Registro de PDFs)
```sql
CREATE TABLE pdf_generations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    format_type TEXT,  -- elevator | door | label
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_pdf_date ON pdf_generations(created_at DESC);
```

**settings** (Configuración del Sistema)
```sql
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Flujo de Datos

### 4.1 Conversión Texto → Braille

```
┌──────────┐     ┌──────────┐     ┌─────────────────┐     ┌──────────┐
│ Usuario  │────▶│ Frontend │────▶│ Backend API     │────▶│ BD       │
│ (input)  │     │ (JS)     │     │ BrailleConverter│     │ (SQLite) │
└──────────┘     └──────────┘     └─────────────────┘     └──────────┘
     │                │                    │                     │
     │ 1. "Hola"      │                    │                     │
     ├───────────────▶│ 2. Validación JS   │                     │
     │                ├───────────────────▶│ 3. POST /convert    │
     │                │                    │ 4. text_to_braille()│
     │                │                    ├────────────────────▶│ 5. save
     │                │                    │◀────────────────────┤
     │                │◀───────────────────┤ 6. JSON response    │
     │◀───────────────┤ 7. Renderizar      │                     │
     │ "⠓⠕⠇⠁"         │                    │                     │
```

### 4.2 Generación de PDF

```
┌──────────┐     ┌──────────┐     ┌─────────┐     ┌──────────┐     ┌────────┐
│ Usuario  │────▶│ Frontend │────▶│ Backend │────▶│ ReportLab│────▶│ output/│
└──────────┘     └──────────┘     └─────────┘     └──────────┘     └────────┘
     │                │                 │                │               │
     │ Config.        │                 │                │               │
     ├───────────────▶│ POST /generate  │                │               │
     │                ├────────────────▶│ Convertir      │               │
     │                │                 ├───────────────▶│ Dibujar       │
     │                │                 │                ├──────────────▶│ PDF
     │                │◀────────────────┤ send_file()    │               │
     │◀───────────────┤ Descarga PDF    │                │               │
```

---

## 5. Patrones de Diseño Implementados

### 5.1 Factory Pattern
```python
# run.py
def create_app():
    app = Flask(__name__)
    # Configuración centralizada
    # Registro de blueprints
    # Inicialización de BD
    return app
```

### 5.2 Singleton Pattern
```python
# db_manager.py
db_manager = DatabaseManager()  # Instancia única global
```

### 5.3 Blueprint Pattern
```python
# braille_routes.py
braille_bp = Blueprint('braille', __name__, url_prefix='/api')
# Rutas modulares y reutilizables
```

---

## 6. Seguridad

| Medida | Implementación |
|--------|----------------|
| **CORS** | Configurado para `/api/*` |
| **Validación** | Doble: Frontend (JS) + Backend (Python) |
| **Límite Upload** | 16MB máximo |
| **Secret Key** | Configurable por variable entorno |
| **SQL Injection** | Queries parametrizadas (sqlite3) |
| **Unicode Safety** | Validación de caracteres soportados |

---

## 7. Testing

```python
# tests/test_braille_converter.py
pytest
├── test_text_to_braille()      # Conversión básica
├── test_uppercase()            # Indicador (4,6)
├── test_numbers()              # Indicador (3,4,5,6)
├── test_punctuation()          # Mapeo español
└── test_braille_to_text()      # Conversión inversa
```

**Ejecutar:**
```bash
pytest tests/ -v
pytest --cov=backend --cov-report=html
```

---

## 8. Despliegue

### Requisitos del Sistema
- Python 3.12+
- 50MB espacio disco
- 512MB RAM mínimo
- Navegador moderno (Chrome, Firefox, Edge)

### Configuración de Producción

**.env**
```bash
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
SECRET_KEY=<clave-segura-aleatoria>
```

**Ejecución:**
```bash
python run.py
```

**URL:** http://localhost:5000

---

## 9. Mantenimiento

### Limpieza Automática
```python
# Eliminar registros > 30 días
db_manager.delete_old_records(days=30)
```

### Estadísticas
```python
stats = db_manager.get_statistics()
# {
#   'total_conversions': 150,
#   'total_pdfs': 45,
#   'total_characters_converted': 5230
# }
```

---

## 10. Documentos Relacionados

| Documento | Ubicación |
|-----------|-----------|
| 📐 **Diagrama PlantUML** | `docs/arquitectura/arquitectura-alto-nivel.puml` |
| 🛠️ **Herramientas** | `docs/ambiente-desarrollo/herramientas.md` |
| 🌿 **Estrategia Git** | `docs/ambiente-desarrollo/estrategia-ramificacion.md` |
| 📋 **Casos de Prueba** | `docs/casos-prueba/03-CASOS-PRUEBA.md` |
| 📖 **Manual Instalación** | `docs/manuales/04-MANUAL-INSTALACION.md` |
| 👤 **Manual Usuario** | `docs/manuales/05-MANUAL-USUARIO.md` |
| 🔧 **Documentación Técnica** | `docs/referencias/06-DOCUMENTACION-TECNICA.md` |

---

**Versión del Documento:** 1.0  
**Última Actualización:** 26 de Noviembre de 2025  
**Estado:** ✅ Completo y Actualizado

