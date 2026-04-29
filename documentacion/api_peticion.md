# 📥 Peticiones al Back-end (D'Maria)

Este archivo sirve como canal de comunicación para que **D'Mayoral** (Front-end) solicite formalmente nuevos endpoints o cambios en la API a **D'Maria** (Back-end).

---

## 🚀 Nuevos Endpoints Solicitados

*(Ejemplo de formato)*
### `GET /solicitudes/pendientes`
- **Motivo**: Necesario para el dashboard del colaborador para ver trabajos que no han sido aceptados.
- **Datos requeridos en respuesta**: Lista de objetos Solicitud con `id`, `urgencia` y `distancia`.
- **Estado**: Pendiente.

---

## 🛠️ Modificaciones de Endpoints Existentes

### `POST /usuarios`
- **Cambio**: Permitir el campo `telefono` opcional durante el registro inicial.
- **Motivo**: Mejorar la tasa de conversión en el registro rápido.
- **Estado**: Pendiente.

---

## 📋 Historial de Peticiones Completadas
- *(Vacío por ahora)*
