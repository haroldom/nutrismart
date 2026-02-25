# Changelog - NutriSmart

## Versión 2.0 - Migración a PyQt6 (2026-02-24)

### Cambios Mayores

- **Framework UI**: Migrado completamente de Tkinter a PyQt6
- **Arquitectura**: Implementada arquitectura de múltiples vistas con navegación lateral
- **Base de datos**: Mejorada con soporte completo para nivel de actividad, recetas detalladas, y sistema de logros

### Nuevas Características

#### Interfaz Moderna con PyQt6
- Diseño moderno y profesional con componentes reutilizables
- Navegación lateral con menú intuitivo
- Animaciones y transiciones suaves
- Soporte completo para temas y estilos personalizados

#### Sistema de Vistas Separadas
1. **Dashboard**: Vista principal con resumen de calorías, macros, IMC y nivel de actividad
2. **Mi Perfil**: Gestión completa de datos personales con actualización en tiempo real
3. **Seguimiento**: Registro diario de comidas con progreso visual y stats
4. **Recetas**: Catálogo de recetas peruanas con ingredientes y pasos detallados
5. **Logros**: Sistema de rachas y logros desbloqueables

#### Mejoras en Funcionalidad

**Nivel de Actividad Física**
- 5 niveles: Sedentario, Ligeramente activo, Moderadamente activo, Muy activo, Extra activo
- Cálculo dinámico de TDEE basado en actividad
- Actualización en registro para mejores recomendaciones

**Recetas Detalladas**
- 15 recetas peruanas prepobladas con:
  - Lista completa de ingredientes
  - Pasos de preparación detallados
  - Tiempo de preparación
  - Nivel de dificultad
  - Información nutricional completa
- Diálogos clickeables para ver recetas completas
- Filtrado por tipo y búsqueda por nombre

**Sistema de Seguimiento Mejorado**
- Agregar comidas desde catálogo
- Ver progreso diario en tiempo real
- Barras de progreso visuales
- Comparación con metas diarias

**Sistema de Logros y Rachas**
- Racha de días consecutivos cumpliendo meta
- Racha máxima histórica
- Logros desbloqueables
- Estadísticas semanales

### Componentes Técnicos

#### Nuevos Archivos
- `ui/styles.py`: Estilos QSS globales y paleta de colores
- `ui/components.py`: Componentes reutilizables (Cards, Botones, NavItems, etc.)
- `ui/main_window.py`: Ventana principal con navegación
- `ui/views/dashboard.py`: Vista del dashboard
- `ui/views/perfil.py`: Vista del perfil de usuario
- `ui/views/tracker.py`: Vista de seguimiento diario
- `ui/views/recetas.py`: Vista de recetas con detalle
- `ui/views/logros.py`: Vista de logros y rachas

#### Archivos Actualizados
- `main.py`: Reescrito completamente para PyQt6
- `ui/login.py`: Nuevo diseño con panel lateral decorativo
- `ui/registro.py`: Formulario mejorado con nivel de actividad
- `database/models.py`: Nuevas funciones de utilidad
- `database/db.py`: Schema actualizado
- `requirements.txt`: PyQt6 como dependencia principal

### Mejoras de UX/UI

- **Colores consistentes**: Paleta de colores verde (#2e7d32) como primario
- **Tipografía**: Uso consistente de Segoe UI
- **Iconos**: Emojis como iconos para mejor visualización
- **Feedback visual**: Mensajes de éxito/error claros
- **Scroll areas**: Todas las vistas soportan scroll para contenido extenso
- **Responsive**: Layouts que se adaptan al tamaño de ventana

### Breaking Changes

- **Tkinter eliminado**: Ya no se usa Tkinter, todo está en PyQt6
- **Archivos obsoletos**: Los antiguos archivos de UI con Tkinter ya no funcionan
- **Base de datos**: Requiere recreación de la DB (el schema cambió)

### Instalación y Uso

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python3 main.py
```

### Próximas Mejoras Sugeridas

- Crear comidas personalizadas desde la UI
- Gráficos de progreso semanal/mensual
- Exportar datos a PDF/Excel
- Modo oscuro
- Notificaciones para recordar registro de comidas
- Integración con APIs de alimentos
- Backup y restauración de datos

---

## Versión 1.0 - Versión Inicial con Tkinter

- Calculadora de calorías y macros
- Registro de usuarios
- Menú básico de comidas peruanas
- Dashboard simple
- Base de datos SQLite
