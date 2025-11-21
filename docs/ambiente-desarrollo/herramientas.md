# Herramientas de Desarrollo

## Objetivo

Este documento detalla todas las herramientas utilizadas en el desarrollo del Sistema de Transcripción Braille, junto con sus versiones, propósitos y configuraciones.

## Lenguajes de Programación

### Python 3.12.10

**Propósito:** Lenguaje principal para el backend del sistema.

**Razones de elección:**
- Sintaxis clara y fácil de aprender
- Amplia disponibilidad de librerías
- Excelente para aplicaciones web con Flask
- Soporte nativo para SQLite
- Comunidad activa y documentación abundante

**Instalación:**
- Descargar desde: https://www.python.org/downloads/
- Verificar versión: `python --version`

### HTML5

**Propósito:** Estructura de la interfaz de usuario.

**Características utilizadas:**
- Elementos semánticos
- Formularios interactivos
- Canvas (si se requiere para visualización Braille)

### CSS3

**Propósito:** Diseño visual y estilos de la interfaz.

**Características utilizadas:**
- Flexbox para layouts responsivos
- Grid (si es necesario)
- Variables CSS
- Media queries para responsive design

### JavaScript (ES6+)

**Propósito:** Lógica del cliente e interacción con el backend.

**Características utilizadas:**
- Fetch API para peticiones HTTP
- Async/Await
- Módulos ES6
- Manipulación del DOM

## Frameworks y Librerías

### Backend

#### Flask 3.0.0

**Propósito:** Framework web para crear la API REST.

**Características utilizadas:**
- Rutas y endpoints
- Manejo de peticiones HTTP
- Renderizado de templates
- Manejo de JSON

**Instalación:**
```bash
pip install Flask==3.0.0
```

#### Flask-CORS 4.0.0

**Propósito:** Permitir peticiones desde el frontend durante desarrollo.

**Instalación:**
```bash
pip install Flask-CORS==4.0.0
```

#### ReportLab 4.0.7

**Propósito:** Generación de archivos PDF con señalética Braille.

**Características:**
- Creación de PDFs programáticamente
- Soporte para fuentes personalizadas
- Dibujo de formas y patrones

**Instalación:**
```bash
pip install reportlab==4.0.7
```

#### Pillow 10.1.0

**Propósito:** Procesamiento de imágenes.

**Uso:**
- Manipulación de logos
- Generación de imágenes con patrones Braille
- Conversión de formatos

**Instalación:**
```bash
pip install Pillow==10.1.0
```

#### python-dotenv 1.0.0

**Propósito:** Gestión de variables de entorno.

**Uso:**
- Configuraciones sensibles
- Diferentes entornos (desarrollo/producción)

**Instalación:**
```bash
pip install python-dotenv==1.0.0
```

### Base de Datos

#### SQLite3

**Propósito:** Sistema de base de datos embebido.

**Características:**
- Incluido en Python (no requiere instalación)
- Base de datos en un solo archivo
- Ideal para aplicaciones pequeñas
- Soporte completo SQL

**Versión:** 3.x (incluida en Python)

### Testing

#### pytest 7.4.3

**Propósito:** Framework de pruebas unitarias.

**Características:**
- Sintaxis simple
- Descubrimiento automático de tests
- Fixtures para setup/teardown
- Reportes detallados

**Instalación:**
```bash
pip install pytest==7.4.3
```

#### pytest-cov 4.1.0

**Propósito:** Medición de cobertura de código.

**Uso:**
```bash
pytest --cov=backend --cov-report=html tests/
```

**Instalación:**
```bash
pip install pytest-cov==4.1.0
```

## Herramientas de Desarrollo

### Editor de Código

#### Visual Studio Code

**Propósito:** Editor de código principal.

**Extensiones recomendadas:**
- Python (Microsoft)
- Pylance
- Python Test Explorer
- GitLens
- Live Server (para frontend)
- Prettier (formateo de código)
- ESLint (linting JavaScript)

**Configuración recomendada (.vscode/settings.json):**
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "files.autoSave": "afterDelay"
}
```

### Control de Versiones

#### Git 2.x

**Propósito:** Control de versiones del código.

**Comandos principales:**
- `git status`: Ver estado actual
- `git add .`: Agregar cambios
- `git commit -m "mensaje"`: Guardar cambios
- `git push`: Subir cambios
- `git pull`: Descargar cambios

**Instalación:**
- Windows: https://git-scm.com/download/win
- Verificar: `git --version`

#### GitHub

**Propósito:** Repositorio remoto y colaboración.

**URL del proyecto:** https://github.com/alexander20020416/ProyectoConstruccion

**Características utilizadas:**
- Hospedaje de código
- Gestión de ramas
- Pull requests (si hay equipo)
- Issues para tracking de tareas

### Terminal

#### PowerShell / Git Bash

**Propósito:** Ejecución de comandos y scripts.

**Comandos frecuentes:**
```bash
# Navegación
cd ruta/carpeta
ls                    # Listar archivos

# Python
python script.py      # Ejecutar script
pip install paquete   # Instalar librería

# Git
git status
git add .
git commit -m "mensaje"
git push
```

## Entorno Virtual

### venv

**Propósito:** Aislar dependencias del proyecto.

**Creación:**
```bash
python -m venv venv
```

**Activación:**
```bash
# Windows PowerShell
venv\Scripts\activate

# Git Bash / Linux
source venv/bin/activate
```

**Desactivación:**
```bash
deactivate
```

**Ventajas:**
- Dependencias aisladas por proyecto
- No contamina instalación global de Python
- Facilita reproducibilidad

## Herramientas Opcionales

### Postman / Thunder Client

**Propósito:** Probar endpoints de la API.

**Uso:**
- Hacer peticiones HTTP manualmente
- Verificar respuestas del backend
- Debugging de API

### DB Browser for SQLite

**Propósito:** Visualizar y editar base de datos SQLite.

**Descarga:** https://sqlitebrowser.org/

**Uso:**
- Inspeccionar tablas
- Ejecutar queries SQL
- Verificar datos

## Diagrama de Herramientas

```
Desarrollo
    ├─ VS Code (editor)
    ├─ Git (control versiones)
    └─ PowerShell (terminal)

Backend
    ├─ Python 3.12
    ├─ Flask (web framework)
    ├─ SQLite (base datos)
    └─ ReportLab (PDFs)

Frontend
    ├─ HTML5
    ├─ CSS3
    └─ JavaScript

Testing
    ├─ pytest
    └─ pytest-cov

Deployment
    └─ GitHub (repositorio)
```

## Instalación Completa

### Paso 1: Instalar Python 3.12

1. Descargar desde python.org
2. Marcar "Add Python to PATH"
3. Instalar
4. Verificar: `python --version`

### Paso 2: Instalar Git

1. Descargar desde git-scm.com
2. Instalar con opciones por defecto
3. Verificar: `git --version`

### Paso 3: Instalar VS Code

1. Descargar desde code.visualstudio.com
2. Instalar
3. Instalar extensión de Python

### Paso 4: Clonar Proyecto

```bash
git clone https://github.com/alexander20020416/ProyectoConstruccion.git
cd ProyectoConstruccion
```

### Paso 5: Crear Entorno Virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### Paso 6: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 7: Verificar Instalación

```bash
python -c "import flask; print(flask.__version__)"
pytest --version
```

## Configuración del Proyecto

### Archivo .env (crear manualmente)

```
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_PATH=backend/database/braille.db
```

### Archivo .gitignore

Ya está creado y configurado para:
- Ignorar entorno virtual (venv/)
- Ignorar archivos compilados Python (__pycache__)
- Ignorar base de datos con datos (*.db)
- Ignorar archivos generados (output/)

## Recursos y Documentación

### Python
- Documentación oficial: https://docs.python.org/3/
- Tutorial: https://docs.python.org/3/tutorial/

### Flask
- Documentación: https://flask.palletsprojects.com/
- Quickstart: https://flask.palletsprojects.com/quickstart/

### pytest
- Documentación: https://docs.pytest.org/
- Getting Started: https://docs.pytest.org/en/stable/getting-started.html

### Git
- Pro Git Book: https://git-scm.com/book/es/v2
- Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf

### HTML/CSS/JavaScript
- MDN Web Docs: https://developer.mozilla.org/es/
- W3Schools: https://www.w3schools.com/

## Soporte y Solución de Problemas

### Python no reconocido

**Problema:** `python` no se reconoce como comando

**Solución:**
1. Reinstalar Python marcando "Add to PATH"
2. O agregar manualmente a PATH de Windows

### pip no funciona

**Problema:** `pip install` no funciona

**Solución:**
```bash
python -m pip install paquete
```

### Entorno virtual no activa

**Problema:** No se activa venv

**Solución PowerShell:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Import Error

**Problema:** `ModuleNotFoundError`

**Solución:**
1. Verificar que venv está activado
2. Reinstalar dependencias: `pip install -r requirements.txt`

---

**Fecha de creación:** 20 de noviembre de 2025  
**Autor:** Alexander  
**Versión:** 1.0
