# Estrategia de Ramificación - Segunda Iteración (v2)

## Actualización del Modelo de Ramificación

Este documento actualiza la estrategia de ramificación para la segunda iteración del proyecto, siguiendo el modelo GitFlow simplificado establecido en la primera iteración.

## Estado Actual de Ramas

| Rama | Propósito | Estado |
|------|-----------|--------|
| `main` | Producción estable | Primera iteración |
| `develop` | Desarrollo primera iteración | Completada |
| `develop-v2` | Desarrollo segunda iteración | **Activa** |
| `documentacion` | Documentación primera iteración | Completada |
| `documentacion-v2` | Documentación segunda iteración | **Activa** |

## Flujo de Trabajo Segunda Iteración

### Diagrama de Ramas

```
main ─────────────────────────────────────────────────────────▶
  │
  │ (v1.0.0)                                       (v2.0.0)
  │                                                   │
  └──▶ develop ──────────────────┐                    │
                                 │                    │
                                 ▼                    │
                          develop-v2 ─────────────────┤
                               │                      │
                               │  commits v2          │
                               │   ▼ ▼ ▼ ▼           │
                               └──────────────────────┘
                                        │
                                        ▼
                              documentacion-v2
                                   │
                                   │ docs v2
                                   ▼
```

### Commits Realizados en develop-v2

| # | Hash | Mensaje | Archivos |
|---|------|---------|----------|
| 1 | `94e5744` | feat: agregar validación de traducciones Braille | braille_converter.py, braille_routes.py |
| 2 | `d230682` | feat: agregar botones rápidos de indicadores | index.html |
| 3 | `a01c966` | feat: agregar estilos para modal y celdas | styles.css |
| 4 | `b87dabe` | feat: implementar edición de secuencia | app.js |
| 5 | `cb281d4` | test: agregar tests Braille-Español | test_braille_converter.py |
| 6 | `7298838` | style: Mejorar colores según HCI | styles.css |
| 7 | `d2e29ac` | feat: funciones de espejo | braille_converter.py |
| 8 | `7158829` | feat: PDF en espejo | pdf_generator.py |
| 9 | `760a3ad` | feat: parámetro mirror en endpoint | braille_routes.py |
| 10 | `57f85ef` | feat: selector modo PDF en UI | index.html |
| 11 | `70f7846` | feat: enviar parámetro mirror | app.js |
| 12 | `1a3539e` | test: tests funcionalidad espejo | test_braille_converter.py |

**Total: 12 commits**

## Convenciones de Commits

### Prefijos Utilizados

| Prefijo | Descripción | Ejemplo |
|---------|-------------|---------|
| `feat:` | Nueva funcionalidad | feat: agregar validación de traducciones |
| `fix:` | Corrección de errores | fix: corregir prioridad de puntuación |
| `style:` | Cambios de estilo/UI | style: mejorar colores según HCI |
| `test:` | Tests nuevos o modificados | test: agregar tests para espejo |
| `docs:` | Documentación | docs: actualizar análisis de cambio |
| `refactor:` | Refactorización | refactor: optimizar mapeo inverso |

### Formato de Mensaje

```
<tipo>: <descripción corta>

[cuerpo opcional con más detalles]

[referencias a issues si aplica]
```

## Proceso de Integración

### Paso 1: Finalizar desarrollo en develop-v2
✅ **Completado** - 12 commits realizados

### Paso 2: Documentación en documentacion-v2
🔄 **En progreso** - Documentos de análisis de cambio

### Paso 3: Merge develop-v2 → main
⏳ **Pendiente** - Después de aprobación

### Paso 4: Tag de versión
⏳ **Pendiente** - v2.0.0

## Comandos Utilizados

### Desarrollo

```bash
# Cambiar a rama de desarrollo v2
git checkout develop-v2

# Ver estado
git status

# Agregar cambios
git add <archivo>

# Commit con mensaje descriptivo
git commit -m "feat: descripción del cambio"

# Push a remoto
git push origin develop-v2
```

### Documentación

```bash
# Cambiar a rama de documentación v2
git checkout documentacion-v2

# Actualizar documentos
# ... editar archivos ...

# Commit
git commit -m "docs: actualizar análisis de cambio"

# Push
git push origin documentacion-v2
```

### Integración (cuando esté listo)

```bash
# Merge documentación a develop-v2
git checkout develop-v2
git merge documentacion-v2

# Merge develop-v2 a main
git checkout main
git merge develop-v2

# Crear tag de versión
git tag -a v2.0.0 -m "Segunda iteración: Braille a Español + PDF Espejo"
git push origin v2.0.0

# Push main
git push origin main
```

## Protección de Ramas

| Rama | Protección | Commits Directos |
|------|------------|------------------|
| main | Alta | ❌ No permitidos |
| develop | Media | Solo fixes menores |
| develop-v2 | Media | Solo fixes menores |
| documentacion-v2 | Baja | ✅ Permitidos |

## Historial de Versiones

| Versión | Fecha | Descripción | Rama Origen |
|---------|-------|-------------|-------------|
| v1.0.0 | Nov 2025 | Primera iteración | develop |
| v2.0.0 | Dic 2025 | Segunda iteración | develop-v2 |

## Notas

1. **No se realiza merge a main** hasta completar la documentación y pruebas finales
2. **develop-v2** se creó desde `develop` para mantener historial limpio
3. **documentacion-v2** se mantiene separada para revisión independiente
4. Los **commits son atómicos** - cada uno representa un cambio específico
