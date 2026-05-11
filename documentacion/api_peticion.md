# 📥 Peticiones al Back-end (D'Maria)

Este archivo sirve como canal de comunicación para que **D'Mayoral** (Front-end) solicite formalmente nuevos endpoints o cambios en la API a **D'Maria** (Back-end).

---

## 🚀 Nuevos Endpoints Solicitados
- *(Todos completados)*

---

## 🛠️ Modificaciones de Endpoints Existentes
- *(Todos completados)*

---

## 📋 Historial de Peticiones Completadas
### `POST /auth/google` y `POST /auth/facebook`
- **Motivo**: Implementación de Social Login (OAuth2).
- **Estado**: Completado. Soporta registro automático y validación de tokens.

### `POST /colaboradores` (Actualización)
- **Cambio**: Acepta `nombre_completo` (actualiza usuario), `telefono_verificacion` y `zona_trabajo`.
- **Estado**: Completado.

### `POST /cotizaciones-especiales`
- **Motivo**: Para procesar el formulario de "¿No encuentras lo que buscas?" donde el usuario describe un problema libre y sube fotos.
- **Estado**: Completado en motor Finit (Rust).

### `POST /calificaciones`
- **Motivo**: Para enviar la puntuación final (estrellas y aspectos) al terminar un servicio.
- **Datos añadidos**: `aspectos` (lista de strings).
- **Estado**: Completado en motor Finit (Rust).

### `POST /colaboradores/{id}/documentacion`
- **Cambio**: Los campos ahora se llaman: `identificacion_frontal`, `identificacion_trasera`, `comprobante_domicilio`, `foto_perfil_identificacion`.
- **Estado**: Completado en motor Finit (Rust).

### `POST /colaboradores/{id}/horarios`
- **Cambio**: Recibir una lista de objetos con `dia_semana` (0-6), `hora_inicio`, `hora_fin` y `activo`.
- **Estado**: Completado en motor Finit (Rust).
