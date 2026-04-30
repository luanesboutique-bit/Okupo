# 📥 Peticiones al Back-end (D'Maria)

Este archivo sirve como canal de comunicación para que **D'Mayoral** (Front-end) solicite formalmente nuevos endpoints o cambios en la API a **D'Maria** (Back-end).

---

## 🚀 Nuevos Endpoints Solicitados

### `POST /cotizaciones-especiales`
- **Motivo**: Para procesar el formulario de "¿No encuentras lo que buscas?" donde el usuario describe un problema libre y sube fotos.
- **Datos requeridos**: `descripcion_trabajo`, `fotos_evidencia` (lista de rutas o blobs), `presupuesto_estimado`, `nivel_urgencia`.
- **Estado**: Pendiente.

### `POST /calificaciones`
- **Motivo**: Para enviar la puntuación final (estrellas y aspectos) al terminar un servicio.
- **Datos requeridos**: `solicitud_id`, `puntuacion` (1-5), `aspectos` (lista de strings: puntualidad, limpieza, calidad), `comentario`.
- **Estado**: Pendiente.

---

## 🛠️ Modificaciones de Endpoints Existentes

### `POST /colaboradores`
- **Cambio**: Asegurar que acepte los campos guardados en sesión durante el registro: `nombre_completo`, `telefono_verificacion`, `zona_trabajo`.
- **Estado**: Pendiente.

### `POST /colaboradores/{id}/documentacion`
- **Cambio**: Los campos ahora se llaman: `identificacion_frontal`, `identificacion_trasera`, `comprobante_domicilio`, `foto_perfil_identificacion`.
- **Estado**: Pendiente.

### `POST /colaboradores/{id}/horarios`
- **Cambio**: Recibir una lista de objetos con `dia_semana` (0-6), `hora_inicio`, `hora_fin` y `activo`.
- **Estado**: Pendiente.

---

## 📋 Historial de Peticiones Completadas
- *(Vacío por ahora)*
