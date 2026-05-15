# 📥 Peticiones al Back-end (finit)

Este archivo sirve como canal de comunicación para que el equipo de Front-end (Okupo) solicite cambios o nuevos servicios al motor Back-end (finit).

---

## 🚀 Peticiones Pendientes
- [ ] **Soporte para múltiples fotos en evidencia**: Permitir que el endpoint `/solicitudes/:id/evidencia` acepte un array de URLs o archivos.
- [ ] **Endpoint de Notificaciones**: Necesitamos saber cuándo hay un nuevo mensaje sin hacer polling constante.
- [ ] **Búsqueda global**: Un endpoint `/buscar?q=termino` que devuelva categorías o subcategorías relevantes para evitar el clasificador hardcodeado en el front.

---

## 📋 Cambios Recientes Implementados (Sync Mayo 2026)

### 📸 Gestión de Portafolio
- **Endpoint**: `POST /colaboradores/:id/portafolio`
- **Cambio**: Los campos ahora son `titulo`, `imagen` y `descripcion` (anteriormente `foto_antes`/`foto_despues`).
- **Estado**: Sincronizado en Okupo.

### 🧾 Evidencia de Trabajo
- **Endpoint**: `POST /solicitudes/:id/evidencia`
- **Uso**: Se usa para subir fotos al inicio y al final del servicio.
- **Campo añadido**: `fotos_evidencia_final` en el modelo de base de datos.

### 🛡️ Administración
- **Endpoint**: `POST /colaboradores/:id/verificar`
- **Uso**: Para que el administrador apruebe técnicos desde el panel Tauri.

### ⏰ Horarios y Precios
- **Endpoints**: `/horarios` y `/precios-dinamicos`.
- **Estado**: Completamente operativos en el motor Rust.
