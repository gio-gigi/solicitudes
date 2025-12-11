# README - DSM5: Sistema de Gestión de Login, Usuarios y Roles

## 📋 Descripción General

**DSM5** es el módulo encargado de gestionar el **login, usuarios y roles** en el sistema de solicitudes. Es la base de autenticación y autorización que controla el acceso y permisos de todos los usuarios del sistema.

---

## 📁 Estructura de Archivos de DSM5

### Ubicación Principal
**Directorio:** `solicitudes_app/`

### Archivos Funcionales del Módulo DSM5

#### 1. **`models.py`** (96% cobertura ✅)
- **Propósito:** Define el modelo de usuario personalizado
- **Contenido:**
  - Modelo `Usuario` que extiende `AbstractBaseUser` y `PermissionsMixin`
  - Campos: username, email, first_name, last_name, telefono, rol, matricula, perfil_completo
  - Roles disponibles: alumno, control_escolar, responsable_programa, responsable_tutorias, director, administrador
  - Manager personalizado `UsuarioManager` para crear usuarios y superusuarios
- **Líneas de código:** 23 statements
- **Funcionalidad clave:** Base de datos de usuarios con roles y permisos

#### 2. **`forms.py`** (96% cobertura ✅)
- **Propósito:** Formularios para registro, actualización y gestión de usuarios
- **Contenido:**
  - `RegistroUsuarioForm`: Registro de nuevos usuarios (solo rol 'alumno')
  - `ActualizarPerfilForm`: Actualización de datos de perfil del usuario
  - `GestionarUsuarioForm`: Gestión de usuarios por administradores (todos los roles)
  - Validaciones: email único, contraseñas seguras, teléfono 10 dígitos, matrícula formato válido
  - Normalización: emails en minúsculas, eliminación de espacios extras
- **Líneas de código:** 185 statements
- **Funcionalidad clave:** Validación y procesamiento de datos de usuarios

#### 3. **`views.py`** (94% cobertura ✅)
- **Propósito:** Vistas para login, registro, perfil y gestión de usuarios
- **Contenido:**
  - `login_view`: Autenticación de usuarios
  - `logout_view`: Cierre de sesión
  - `registro_view`: Registro de nuevos usuarios (solo alumnos)
  - `perfil_view`: Completar/actualizar perfil de usuario
  - `cambiar_password_view`: Cambio de contraseña
  - `bienvenida_view`: Página de bienvenida después de login
  - `lista_usuarios_view`: Listar todos los usuarios (solo admin)
  - `editar_usuario_view`: Editar cualquier usuario (solo admin)
  - `eliminar_usuario_view`: Eliminar usuarios (solo admin, protección último admin)
- **Líneas de código:** 140 statements
- **Funcionalidad clave:** Lógica de negocio para gestión de usuarios

#### 4. **`decorators.py`** (93% cobertura ✅)
- **Propósito:** Decoradores para control de acceso basado en roles
- **Contenido:**
  - `@rol_requerido`: Verificar roles específicos
  - `@administrador_requerido`: Solo administradores
  - `@puede_crear_tipos_solicitudes`: Control escolar o administrador
  - `@puede_atender_solicitudes`: Responsables y director
  - `@puede_ver_dashboard`: Solo director
  - `@perfil_completo_requerido`: Usuario con perfil completo
- **Líneas de código:** 60 statements
- **Funcionalidad clave:** Seguridad y control de acceso por rol

#### 5. **`middleware.py`** (100% cobertura ✅)
- **Propósito:** Middleware para verificar perfil completo
- **Contenido:**
  - `PerfilCompletoMiddleware`: Redirige a completar perfil si `perfil_completo=False`
  - Excepciones: login, logout, registro, perfil, cambiar_password
- **Líneas de código:** 18 statements
- **Funcionalidad clave:** Forzar completar perfil antes de usar el sistema

#### 6. **`urls.py`**
- **Propósito:** Configuración de rutas URL del módulo
- **Contenido:**
  - Rutas para: login, logout, registro, perfil, cambiar_password, bienvenida
  - Rutas de gestión: lista_usuarios, crear_usuario, editar_usuario, eliminar_usuario
  - Namespace: `solicitudes_app`
- **Funcionalidad clave:** Mapeo de URLs a vistas

#### 7. **`admin.py`**
- **Propósito:** Configuración del panel de administración Django
- **Contenido:**
  - Registro del modelo `Usuario` en Django Admin
  - Configuración de campos visibles y editables
- **Funcionalidad clave:** Gestión administrativa de usuarios

---

## 🎯 Roles y Permisos Definidos

### Roles Disponibles (definidos en `models.py`)

| Rol | Código | Permisos Principales |
|-----|--------|---------------------|
| **Alumno** | `alumno` | Crear solicitudes, visualizar sus solicitudes |
| **Control Escolar** | `control_escolar` | Crear tipos de solicitudes, crear formularios, atender solicitudes |
| **Responsable de Programa** | `responsable_programa` | Atender solicitudes, crear solicitudes |
| **Responsable de Tutorías** | `responsable_tutorias` | Atender solicitudes, crear solicitudes |
| **Director** | `director` | Atender solicitudes, ver dashboard con métricas |
| **Administrador** | `administrador` | Gestionar usuarios y roles, crear tipos de solicitudes, acceso total |

---

## 🧪 Suite de Pruebas de DSM5

### Archivos de Pruebas (184 tests totales)

| Archivo | Tests | Propósito |
|---------|-------|-----------|
| `test_decorators.py` | 24 | Tests de decoradores de permisos |
| `test_views_extra.py` | 28 | Tests de vistas administrativas |
| `test_forms_extra.py` | 21 | Tests de validación de formularios |
| `test_views_coverage.py` | 18 | Cobertura adicional de vistas |
| `test_forms_coverage.py` | 24 | Cobertura completa de formularios |
| `test_views_final.py` | 4 | Tests de protección último admin |
| `test_forms_validation_extra.py` | 16 | Validaciones de campos vacíos |
| `test_views_edges.py` | 8 | Casos borde en vistas |
| `test_forms_complete.py` | 14 | Validaciones de caracteres y formato |
| `test_final_coverage.py` | 11 | Errores de decoradores y redirects |
| `test_ultra_specific.py` | 16 | Tests ultra-específicos para líneas faltantes |
| `test_extreme_coverage.py` | 12 | Tests finales para alcanzar 95% |
| `test_helper_functions.py` | 14 | Tests de funciones auxiliares de refactorización |

### Cobertura Actual (96% total ✅)

```
Archivo                  Cobertura   Estado
----------------------------------------
middleware.py            100%        ✅ Perfecto
models.py                96%         ✅ Excelente
forms.py                 96%         ✅ Excelente
views.py                 96%         ✅ Excelente
decorators.py            93%         ✅ Excelente
----------------------------------------
TOTAL DSM5               96%         ✅ META SUPERADA
```

---

## 🔧 Comandos para Ejecutar Tests de DSM5

### Ejecutar todos los tests de DSM5
```powershell
cd "solicitudes\app\solicitudes"
coverage run manage.py test solicitudes_app.test_decorators solicitudes_app.test_views_extra solicitudes_app.test_forms_extra solicitudes_app.test_views_coverage solicitudes_app.test_forms_coverage solicitudes_app.test_views_final solicitudes_app.test_forms_validation_extra solicitudes_app.test_views_edges solicitudes_app.test_forms_complete solicitudes_app.test_final_coverage solicitudes_app.test_ultra_specific solicitudes_app.test_extreme_coverage solicitudes_app.test_helper_functions
```

### Ver reporte de cobertura
```powershell
coverage report -m solicitudes_app/models.py solicitudes_app/forms.py solicitudes_app/middleware.py solicitudes_app/decorators.py solicitudes_app/views.py
```

### Generar reporte HTML
```powershell
coverage html --include="solicitudes_app/*" --omit="solicitudes_app/migrations/*,solicitudes_app/test_*.py"
```

---

## 📊 Métricas de Calidad Actual

| Métrica | Valor | Estado |
|---------|-------|--------|
| **Cobertura de código** | 96% | ✅ Cumple (≥95%) |
| **Tests totales** | 184 | ✅ Excelente |
| **Tests pasando** | 184/184 (100%) | ✅ Perfecto |
| **Complejidad ciclomática** | ≤6 todas las funciones | ✅ Cumple (meta: ≤7) |
| **Complejidad promedio** | 2.91 (A - Excelente) | ✅ Excelente |
| **PEP8** | 23 violaciones | ⚠️ Pendiente |

### Detalles de Complejidad Ciclomática ✅

**Estado:** ✅ **TODAS LAS FUNCIONES ≤6** (Meta solicitada: ≤7)

| Archivo | Complejidad Máxima | Promedio | Estado |
|---------|-------------------|----------|--------|
| `models.py` | 2 | 1.2 | ✅ A - Excelente |
| `forms.py` | 5 | 3.7 | ✅ A - Excelente |
| `views.py` | 6 | 3.5 | ✅ A - Excelente |
| `decorators.py` | 1 | 1.0 | ✅ A - Excelente |
| `middleware.py` | 4 | 2.7 | ✅ A - Excelente |

**Funciones refactorizadas - Fase 1:**
- `editar_usuario_view`: 13 → 6 (-54% ✅)
- `login_view`: 10 → 5 (-50% ✅)
- `CompletarPerfilMiddleware.__call__`: 9 → 3 (-67% ✅)

**Funciones refactorizadas - Fase 2:**
- `clean_password1`: 7 → 3 (-57% ✅)
- `eliminar_usuario_view`: 6 → 4 (-33% ✅)
- `_obtener_redireccion_necesaria`: 6 → 4 (-33% ✅)
- `_validar_ultimo_admin`: 6 → 5 (-17% ✅)

**Funciones auxiliares creadas:** 11 funciones para mejorar legibilidad y mantenibilidad

---

## 🔄 Flujo de Trabajo del Sistema

### 1. **Registro de Usuario**
```
Usuario nuevo → registro_view → RegistroUsuarioForm (rol='alumno')
→ Usuario creado → Login automático → Redirigir a bienvenida
```

### 2. **Login**
```
Usuario existente → login_view → Autenticación Django
→ Verificar perfil_completo → Middleware → Redirigir según estado
```

### 3. **Completar Perfil**
```
perfil_completo=False → PerfilCompletoMiddleware → Redirige a perfil_view
→ ActualizarPerfilForm → perfil_completo=True → Acceso completo
```

### 4. **Gestión de Usuarios (Admin)**
```
Administrador → lista_usuarios_view → Ver todos los usuarios
→ editar_usuario_view → GestionarUsuarioForm → Actualizar rol/datos
→ eliminar_usuario_view → Protección último admin → Eliminar
```

### 5. **Control de Acceso**
```
Vista protegida → Decorador (@rol_requerido, etc.)
→ Verificar rol → Permitir/Denegar acceso → Redirigir si no autorizado
```

---

## 📝 Archivos NO Pertenecientes a DSM5

Los siguientes módulos son independientes y NO son parte de DSM5:

- **`tipo_solicitudes/`** - Gestión de tipos de solicitudes (DSM diferente)
- **`atender_solicitudes/`** - Atención y seguimiento de solicitudes (DSM diferente)
- **`tickets/`** - Sistema de tickets (DSM diferente)
- **`solicitudes/`** (settings) - Configuración general del proyecto

---

## ✅ Estado Actual del Proyecto DSM5

### Completado ✅
- [x] PEP8: Reducción de 452 a 23 violaciones (95% reducción)
- [x] Tests unitarios: 184 tests creados
- [x] Cobertura 96%: Meta superada
- [x] Todos los tests pasando (100%)
- [x] Middleware con cobertura 100%
- [x] Complejidad ciclomática ≤7: Todas las funciones cumplen
- [x] Refactorización completada: 3 funciones optimizadas

### Pendiente ⚠️
- [ ] Corregir últimas 23 violaciones PEP8

### Documentación Generada 📄
- [x] README_DSM5.md (este archivo)
- [x] REPORTE_COMPLEJIDAD_DSM5.md (reporte técnico detallado)

---

## 🎯 Próximos Pasos Recomendados

1. ✅ ~~Verificar complejidad ciclomática~~ **COMPLETADO**
2. ✅ ~~Refactorizar funciones complejas~~ **COMPLETADO**
3. **Corregir violaciones PEP8 restantes** (23 violaciones - principalmente líneas largas)
4. **Documentación adicional** de funciones auxiliares creadas

---

## 📄 Reportes Técnicos Disponibles

- **README_DSM5.md** (este archivo): Documentación general del módulo
- **REPORTE_COMPLEJIDAD_DSM5.md**: Análisis técnico detallado de complejidad ciclomática, estrategias de refactorización y métricas completas

---

## 📌 Notas Importantes

- **DSM5 es CRÍTICO** para el funcionamiento de todo el sistema (autenticación/autorización)
- **Todos los cambios** en DSM5 deben mantener la cobertura ≥95%
- **Tests deben ejecutarse** antes de cualquier commit
- **Protección último admin** implementada para evitar bloqueo del sistema
- **Middleware** fuerza completar perfil para mejorar calidad de datos

---

## 📧 Contacto y Mantenimiento

**Módulo:** DSM5 - Gestión de Login, Usuarios y Roles  
**Cobertura:** 96% ✅  
**Tests:** 184/184 pasando ✅  
**Complejidad:** ≤7 todas las funciones ✅  
**Última actualización:** 11 de Diciembre de 2025

### Documentación Técnica
- 📄 **README_DSM5.md**: Documentación general
- 📊 **REPORTE_COMPLEJIDAD_DSM5.md**: Análisis técnico de refactorización

---

**Fin del README DSM5**
