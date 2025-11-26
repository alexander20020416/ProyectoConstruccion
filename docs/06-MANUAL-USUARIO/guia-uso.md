# Manual de Usuario
## Sistema de Transcripción Braille

### Introducción

El Sistema de Transcripción Braille es una aplicación web que permite convertir texto español a Braille y viceversa, además de generar señalética táctil en formato PDF.

### Acceso al Sistema

1. Abrir navegador web (Chrome, Firefox o Edge)
2. Ingresar a la dirección: http://localhost:5000
3. La interfaz principal se mostrará automáticamente

---

### Interfaz Principal

La aplicación cuenta con 3 secciones principales accesibles mediante tabs:

1. Conversor
2. Señalética
3. Historial (si está disponible)

---

## Sección 1: Conversor

### Conversión de Español a Braille

**Pasos:**

1. Hacer clic en tab "Conversor"
2. En el área "Español → Braille":
   - Escribir o pegar el texto a convertir
   - El texto puede contener:
     - Letras (a-z, mayúsculas y minúsculas)
     - Números (0-9)
     - Vocales acentuadas (á, é, í, ó, ú)
     - Caracteres especiales (ñ, ü)
     - Signos de puntuación básicos
3. Hacer clic en botón "Convertir a Braille"
4. El resultado aparecerá en el área de resultados mostrando:
   - Texto en Braille Unicode
   - Representación visual de puntos
   - Número de caracteres convertidos

**Ejemplo:**

Entrada: `Hola Mundo`

Salida: `⠓⠕⠇⠁ ⠍⠥⠝⠙⠕`

### Conversión de Braille a Español

**Método 1: Usando el Constructor Visual**

1. En la sección "Braille → Español"
2. Usar el constructor de 6 puntos:
   - Hacer clic en los puntos para activarlos/desactivarlos
   - Los puntos activos se mostrarán en color oscuro
   - La celda completa se muestra en la vista previa
3. Hacer clic en "Agregar Carácter"
4. Repetir para construir la palabra completa
5. Hacer clic en "Convertir a Texto"

**Método 2: Pegando Braille Unicode** (si está disponible)

1. Pegar texto en Braille Unicode directamente
2. Hacer clic en "Convertir a Texto"

**Ejemplo Constructor:**

Para escribir "Hola":
- H: Activar puntos 1, 2, 5
- o: Activar puntos 1, 3, 5
- l: Activar puntos 1, 2, 3
- a: Activar punto 1

---

## Sección 2: Señalética

Esta sección permite generar PDFs con señalética táctil en Braille.

### Tipos de Señalética

**1. Señalética de Ascensor**

Para generar etiquetas de pisos:

1. Seleccionar formato "Ascensor"
2. Ingresar título (ej: "Edificio Principal")
3. Agregar pisos:
   - Hacer clic en "Agregar Piso"
   - Número: 1, 2, 3, etc.
   - Texto: "Planta Baja", "Piso 1", etc.
4. Hacer clic en "Generar PDF"
5. El archivo se descargará automáticamente

**2. Etiqueta de Puerta**

Para etiquetas de oficinas o habitaciones:

1. Seleccionar formato "Puerta"
2. Ingresar título (ej: "Departamento de Recursos Humanos")
3. Texto adicional (opcional)
4. Hacer clic en "Generar PDF"

**3. Etiqueta Personalizada**

Para señalética general:

1. Seleccionar formato "Personalizada"
2. Título principal
3. Subtítulo (opcional)
4. Texto descriptivo
5. Hacer clic en "Generar PDF"

### Características del PDF Generado

- Círculos táctiles de 1.5mm de diámetro
- Espaciado estándar entre puntos
- Incluye texto en español como referencia
- Formato listo para impresión

---

## Funciones Adicionales

### Validación Automática

El sistema valida automáticamente:
- Caracteres soportados
- Formato correcto del texto
- Longitud máxima permitida

Si se ingresan caracteres no soportados, se mostrará un mensaje indicando cuáles son.

### Copiar Resultados

Para copiar el texto en Braille generado:
1. Seleccionar el texto del área de resultados
2. Clic derecho → Copiar
3. O usar Ctrl+C (Cmd+C en Mac)

### Limpiar Formulario

Para borrar el contenido y comenzar de nuevo:
1. Hacer clic en botón "Limpiar" (si está disponible)
2. O refrescar la página (F5)

---

## Ejemplos de Uso

### Ejemplo 1: Etiquetar Medicamento

Objetivo: Crear etiqueta Braille para frasco de medicamento

Pasos:
1. Ir a "Conversor"
2. Escribir: "Paracetamol 500mg"
3. Convertir a Braille
4. Copiar resultado
5. Ir a "Señalética" → "Etiqueta Personalizada"
6. Título: "Paracetamol 500mg"
7. Generar PDF
8. Imprimir en papel adhesivo

### Ejemplo 2: Señalética de Edificio

Objetivo: Crear señales para pisos de edificio

Pasos:
1. Ir a "Señalética"
2. Seleccionar "Ascensor"
3. Agregar:
   - Planta Baja
   - Piso 1
   - Piso 2
   - Piso 3
4. Generar PDF
5. Imprimir y adherir cerca de botones del ascensor

### Ejemplo 3: Verificar Texto Braille

Objetivo: Verificar que un texto Braille dice "Baño"

Pasos:
1. Ir a "Conversor" → "Braille a Español"
2. Usar constructor para recrear el Braille
3. Hacer clic en "Convertir"
4. Verificar que la salida sea "Baño"

---

## Solución de Problemas

**Problema: El texto no se convierte**

Solución:
- Verificar que no haya caracteres especiales no soportados
- Revisar la conexión con el servidor
- Refrescar la página

**Problema: El PDF no se genera**

Solución:
- Verificar que todos los campos estén llenos
- Revisar que el navegador permite descargas
- Verificar espacio disponible en disco

**Problema: Los puntos Braille no se ven**

Solución:
- Verificar que el navegador soporta Unicode
- Actualizar el navegador a la última versión
- Probar en otro navegador

**Problema: La página no carga**

Solución:
- Verificar que el servidor está ejecutándose
- Revisar que la URL sea correcta (http://localhost:5000)
- Verificar firewall no bloquea el puerto 5000

---

## Límites y Restricciones

- Longitud máxima de texto: 10,000 caracteres
- Tamaño máximo de PDF: 16 MB
- Caracteres soportados: Alfabeto español completo, números, puntuación básica
- Navegadores soportados: Chrome 90+, Firefox 88+, Edge 90+

---

## Consejos de Uso

1. Probar primero con textos cortos
2. Guardar PDFs con nombres descriptivos
3. Imprimir PDFs en alta calidad para mejor definición táctil
4. Usar papel adhesivo transparente para etiquetas duraderas
5. Verificar conversiones importantes usando la conversión inversa

---

## Soporte

Para reportar problemas o sugerencias:
- Crear issue en: https://github.com/alexander20020416/ProyectoConstruccion/issues
- Revisar documentación técnica en carpeta docs/

---

## Glosario

- **Braille**: Sistema de lectura y escritura táctil para personas con discapacidad visual
- **Cuadratín**: Celda básica de 6 puntos del sistema Braille
- **Indicador**: Símbolo especial que modifica el significado del siguiente carácter
- **Señalética**: Sistema de señales o símbolos para orientación
- **Unicode Braille**: Representación digital de caracteres Braille (U+2800 a U+28FF)
