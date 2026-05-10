# Especificaciones de Integración: Pasarela de Pagos (Conekta)

Este documento detalla los requerimientos necesarios en el Backend para completar la integración de pagos y la lógica de negocio acordada.

## 1. Endpoints de Procesamiento y Distribución
Actualmente, el frontend envía el token de Conekta al endpoint `/confirmar/finalizar`. Se requiere que el backend realice lo siguiente:

### A. Endpoint `/confirmar/finalizar` (POST)
*   **Entrada:** JSON `{ "conekta_token": "tok_...", "subcategoria_id": 123 }`
*   **Proceso:**
    1.  **Validación de Precio:** Consultar el precio real del servicio mediante `api_get(f"/subcategorias/{subcat_id}")`. No confiar en montos enviados desde el frontend.
    2.  **Distribución de Fondos (Split Payments):** Implementar la lógica de creación de orden en Conekta utilizando `split_rules` con los siguientes receptores (IDs `rec_...` a configurar en el panel):
        *   **Técnico (75%):** Aplicar deducciones: `monto = (total * 0.75) * (1 - 0.105)` (donde 10.5% = 1% ISR + 8% IVA + 1.5% IMSS).
        *   **Okupo Clic (15%):** `monto = total * 0.15`
        *   **Dueño (5%):** `monto = total * 0.05`
        *   **Socio (5%):** `monto = total * 0.05`
    3.  **Resultado:** Retornar `{ "status": "aprobado", "message": "..." }` o el error correspondiente.

### B. Endpoint de Webhooks (Producción)
*   **Ruta:** `/api/conekta/webhook`
*   **Propósito:** Escuchar eventos asíncronos de Conekta.
*   **Requerimiento:** Procesar eventos de pago:
    *   `order.paid`: Activar la orden en la base de datos automáticamente.
    *   `charge.refunded`: Notificar al usuario y al sistema técnico.

## 2. Gestión de Estados del Pedido
*   **Flujo de Asignación:** Tras el `/confirmar/finalizar` exitoso, el sistema debe transicionar automáticamente el pedido de estado `PENDIENTE_PAGO` a `PAGADO` e iniciar la búsqueda/notificación al técnico más cercano.
*   **Persistencia:** Asegurar que el `conekta_order_id` se guarde en la base de datos vinculado a la solicitud del usuario.

## 3. Seguridad y Configuración
*   **Variables de Entorno:** Se debe incluir obligatoriamente en el servidor:
    *   `CONEKTA_PRIVATE_KEY` (tu llave `key_...`)
    *   `CONEKTA_WEBHOOK_SECRET` (para verificar notificaciones).
*   **Seguridad de Sesión:** El backend debe verificar que el `usuario_id` en la `session` sea el dueño legítimo de la operación.

## 4. Requerimientos de API para el Frontend
1.  `GET /subcategorias/<id>`: Debe devolver siempre el campo `precio_base` actualizado.
2.  `GET /solicitudes?usuario_id=...`: Debe retornar el estado real del pago para que el frontend pueda mostrar al usuario si su pedido está "En camino", "Pagado" o "Pendiente de pago".
