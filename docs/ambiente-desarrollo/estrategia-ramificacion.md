# Estrategia de Ramificación - GitFlow Simplificado

## Objetivo

Este documento describe la estrategia de ramificación utilizada en el proyecto de Transcripción Braille para mantener un código organizado, facilitar el desarrollo en equipo y garantizar la estabilidad del producto.

## Modelo de Ramificación

El proyecto utiliza una variante simplificada de GitFlow, adaptada a un equipo pequeño y ciclos de desarrollo por bimestres.

## Ramas Principales

### 1. main (Rama Principal)

**Propósito:** Contiene el código estable y listo para producción.

**Características:**
- Solo contiene código completamente probado
- Cada commit representa una versión funcional del software
- Se actualiza únicamente al finalizar cada bimestre o iteración
- Está protegida contra commits directos

**Reglas:**
- NUNCA programar directamente en main
- Solo se permite merge desde develop después de testing completo
- Cada merge debe ir acompañado de un tag de versión (v1.0.0, v2.0.0)

### 2. develop (Rama de Desarrollo)

**Propósito:** Integra todas las funcionalidades en desarrollo.

**Características:**
- Base para crear todas las ramas de features
- Contiene las últimas funcionalidades completadas
- Puede tener bugs temporales durante el desarrollo
- Se actualiza continuamente

**Reglas:**
- No programar features complejas directamente aquí
- Recibe merges de ramas feature/* cuando están completas
- Debe mantenerse funcional (compilable)

### 3. documentacion (Rama de Documentación)

**Propósito:** Contiene toda la documentación del proyecto.

**Características:**
- Independiente del código
- Se actualiza en paralelo al desarrollo
- Incluye arquitectura, manuales, casos de prueba
- Se mantiene sincronizada con develop

**Contenido:**
- Diseño arquitectónico
- Documentación de ambiente de desarrollo
- Casos de prueba y resultados
- Manuales de instalación y usuario

## Ramas Temporales

### feature/* (Ramas de Funcionalidades)

**Propósito:** Desarrollar funcionalidades específicas de forma aislada.

**Nomenclatura:** feature/nombre-descriptivo

**Ejemplos:**
- feature/database
- feature/conversion-braille
- feature/frontend
- feature/pdf-generation
- feature/special-characters

**Ciclo de vida:**
```
develop → feature/nombre → [desarrollo] → develop → [eliminar feature]
```

**Proceso:**
1. Crear desde develop: `git checkout develop` → `git checkout -b feature/nombre`
2. Desarrollar la funcionalidad
3. Hacer commits frecuentes con mensajes descriptivos
4. Escribir tests para la funcionalidad
5. Ejecutar todos los tests
6. Hacer merge a develop: `git checkout develop` → `git merge feature/nombre`
7. Eliminar la rama: `git branch -d feature/nombre`

### bugfix/* (Ramas de Corrección de Errores)

**Propósito:** Corregir bugs encontrados durante el desarrollo.

**Nomenclatura:** bugfix/descripcion-error

**Ejemplos:**
- bugfix/acentos-no-convierten
- bugfix/pdf-caracteres-especiales

**Proceso:** Similar a feature/*, pero para correcciones específicas.

## Flujo de Trabajo Completo

```
main (producción)
  │
  │ (merge solo al finalizar bimestre)
  │
develop (integración)
  │
  ├─── feature/database
  │      ├─ commit: "Crear estructura tablas"
  │      ├─ commit: "Poblar patrones primera serie"
  │      ├─ commit: "Tests base de datos"
  │      └─ merge → develop
  │
  ├─── feature/conversion-braille
  │      ├─ commit: "Implementar primera serie"
  │      ├─ commit: "Implementar segunda serie"
  │      ├─ commit: "Implementar tercera serie"
  │      └─ merge → develop
  │
  ├─── feature/frontend
  │      ├─ commit: "Crear estructura HTML"
  │      ├─ commit: "Estilos CSS"
  │      ├─ commit: "JavaScript API calls"
  │      └─ merge → develop
  │
  └─── feature/pdf-generation
         ├─ commit: "Setup ReportLab"
         ├─ commit: "Generar PDF básico"
         └─ merge → develop

documentacion (paralela)
  ├─ commit: "Documentar estrategia ramificación"
  ├─ commit: "Casos de prueba database"
  ├─ commit: "Manual instalación"
  └─ (continúa en paralelo)
```

## Comandos Git Principales

### Crear y cambiar a nueva rama
```bash
git checkout -b nombre-rama
```

### Ver todas las ramas
```bash
git branch -a
```

### Cambiar de rama
```bash
git checkout nombre-rama
```

### Hacer merge de una rama a develop
```bash
git checkout develop
git merge feature/nombre
```

### Eliminar rama local
```bash
git branch -d nombre-rama
```

### Subir rama al repositorio remoto
```bash
git push -u origin nombre-rama
```

## Convenciones de Commits

### Formato
```
tipo: descripción breve

Descripción detallada (opcional)
```

### Tipos de commits
- **feat:** Nueva funcionalidad
- **fix:** Corrección de bug
- **docs:** Cambios en documentación
- **test:** Agregar o modificar tests
- **refactor:** Refactorización de código
- **style:** Cambios de formato (espacios, etc.)

### Ejemplos de buenos commits
```bash
git commit -m "feat: implementar conversión primera serie (a-j)"
git commit -m "test: agregar casos de prueba para números"
git commit -m "fix: corregir conversión de vocales acentuadas"
git commit -m "docs: actualizar manual de usuario"
```

## Estrategia por Bimestre

### Primer Bimestre

**Semanas 1-2:**
- Crear estructura base
- Rama feature/database
- Rama feature/conversion-braille (primera y segunda serie)

**Semanas 3-4:**
- Rama feature/special-characters (tercera serie, números, acentos)
- Rama feature/frontend (interfaz básica)

**Semanas 5-6:**
- Rama feature/pdf-generation
- Integración y testing
- Merge develop → main
- Tag v1.0.0

**Paralelamente:**
- Documentar en rama documentacion todo lo desarrollado

### Segundo Bimestre

Se seguirá el mismo modelo para nuevas funcionalidades.

## Resolución de Conflictos

Si hay conflictos al hacer merge:

1. Git te avisará qué archivos tienen conflictos
2. Abrir los archivos y buscar las marcas:
   ```
   <<<<<<< HEAD
   código actual
   =======
   código de la rama
   >>>>>>> feature/nombre
   ```
3. Decidir qué código mantener
4. Eliminar las marcas de conflicto
5. Hacer commit del merge

## Reglas del Equipo

1. **NUNCA** hacer commits directamente a main
2. **SIEMPRE** crear una rama feature para funcionalidades nuevas
3. **SIEMPRE** hacer pull antes de empezar a trabajar
4. **SIEMPRE** escribir tests antes de hacer merge
5. **SIEMPRE** escribir mensajes de commit descriptivos
6. Hacer commits pequeños y frecuentes
7. Revisar código antes de hacer merge
8. Mantener develop siempre funcional (que compile)

## Herramientas Recomendadas

- **Git Bash / PowerShell:** Para comandos Git
- **VS Code:** Editor con integración Git
- **GitKraken / SourceTree:** Clientes visuales de Git (opcional)
- **GitHub Desktop:** Interfaz simple para operaciones básicas (opcional)

## Estado Actual de las Ramas

- **main:** Código inicial (v0.1.0)
- **develop:** Recién creada, lista para desarrollo
- **documentacion:** Recién creada, documentando estrategia

## Referencias

- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pro Git Book](https://git-scm.com/book/es/v2)

---

**Fecha de creación:** 20 de noviembre de 2025  
**Autor:** Alexander  
**Versión:** 1.0
