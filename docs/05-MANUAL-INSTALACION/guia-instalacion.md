# Manual de Instalación
## Sistema de Transcripción Braille

### Requisitos del Sistema

**Hardware mínimo:**
- Procesador: 1 GHz o superior
- RAM: 2 GB mínimo (4 GB recomendado)
- Espacio en disco: 500 MB

**Software requerido:**
- Python 3.10 o superior
- Git 2.x
- Navegador web moderno (Chrome, Firefox, Edge)

**Sistemas operativos soportados:**
- Windows 10/11
- macOS 12+
- Linux (Ubuntu 20.04+, Debian 11+)

---

### Paso 1: Instalar Python

**Windows:**
1. Descargar Python desde https://www.python.org/downloads/
2. Ejecutar instalador
3. Marcar "Add Python to PATH"
4. Clic en "Install Now"
5. Verificar: `python --version`

**macOS:**
```bash
brew install python@3.12
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

### Paso 2: Instalar Git

**Windows:**
1. Descargar desde https://git-scm.com/download/win
2. Ejecutar instalador con opciones por defecto
3. Verificar: `git --version`

**macOS:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

---

### Paso 3: Clonar el Repositorio

```bash
git clone https://github.com/alexander20020416/ProyectoConstruccion.git
cd ProyectoConstruccion
```

---

### Paso 4: Crear Entorno Virtual

```bash
python -m venv venv
```

---

### Paso 5: Activar Entorno Virtual

**Windows (PowerShell):**
```bash
venv\Scripts\activate
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu terminal.

---

### Paso 6: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0
- Flask-CORS 4.0.0
- ReportLab 4.0.7
- pytest 7.4.3
- Otras dependencias necesarias

---

### Paso 7: Verificar Instalación

```bash
python -c "import flask; print(f'Flask {flask.__version__} instalado')"
pytest --version
```

---

### Paso 8: Ejecutar la Aplicación

```bash
python run.py
```

Deberías ver:
```
======================================================================
  SISTEMA DE TRANSCRIPCIÓN BRAILLE
  Versión 1.0.0
======================================================================

  Servidor iniciando en http://0.0.0.0:5000
  Modo debug: True
  Base de datos: <ruta>/backend/database/braille_system.db

  Presiona Ctrl+C para detener el servidor
======================================================================
```

---

### Paso 9: Acceder a la Aplicación

Abrir navegador y acceder a:
```
http://localhost:5000
```

---

### Problemas Comunes y Soluciones

**1. "python no se reconoce como comando"**

Solución: Agregar Python al PATH del sistema

Windows:
1. Buscar "Variables de entorno"
2. Editar PATH
3. Agregar ruta de Python (ej: C:\Python312)

**2. "No se puede activar el entorno virtual (PowerShell)"**

Solución:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**3. "Error al importar módulo Flask"**

Solución:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**4. "Puerto 5000 ya está en uso"**

Solución: Cambiar puerto en run.py o matar proceso:

Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <numero> /F
```

Linux/Mac:
```bash
lsof -ti:5000 | xargs kill -9
```

**5. "No se puede conectar a la base de datos"**

Solución: La base de datos se crea automáticamente. Si hay problemas:
```bash
rm backend/database/braille_system.db
python run.py
```

---

### Desinstalación

1. Desactivar entorno virtual:
```bash
deactivate
```

2. Eliminar carpeta del proyecto:
```bash
cd ..
rm -rf ProyectoConstruccion  # Linux/Mac
rmdir /s ProyectoConstruccion  # Windows
```

---

### Configuración Opcional

**Variables de entorno (.env):**

Crear archivo `.env` en raíz del proyecto:
```
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
SECRET_KEY=<generar-clave-segura>
```

Para generar SECRET_KEY:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

### Próximos Pasos

- Ver Manual de Usuario para aprender a usar la aplicación
- Revisar documentación técnica en docs/
- Ejecutar pruebas: `pytest tests/`
