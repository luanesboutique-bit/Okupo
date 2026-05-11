# 🔌 Integración API

Okupo utiliza el motor **Finite** como núcleo de procesamiento. A continuación se listan los endpoints principales y su propósito dentro de la interfaz.

---

## 🔑 Autenticación y Usuarios

### `POST /login`
- **Uso**: Iniciar sesión.
- **Retorno**: Token JWT.

### `POST /usuarios`
- **Uso**: Registro de nuevos usuarios (clientes o colaboradores).

### `POST /auth/google` y `POST /auth/facebook`
- **Uso**: Social Login mediante tokens OAuth2. Valida el token con el proveedor y devuelve un JWT. Registra automáticamente al usuario si no existe.

---

## 📂 Catálogo y Marketplace

### `POST /cotizaciones-especiales`
- **Uso**: Enviar una solicitud de servicio para algo que no está en el catálogo estándar.
- **Campos**: `usuario_id`, `descripcion_trabajo`, `fotos_evidencia`, `presupuesto_estimado`, `nivel_urgencia`.

### `GET /categorias`
- **Uso**: Listar los sectores de servicios principales.

### `GET /categorias/{id}/subcategorias`
- **Uso**: Obtener los servicios específicos de una categoría.

### `GET /subcategorias/{id}`
- **Uso**: Obtener detalles de una subcategoría específica (nombre, descripción, precios base).

### `GET /subcategorias/{id}/colaboradores`
- **Uso**: Búsqueda de profesionales mediante filtros de geolocalización.
- **Parámetros**: `latitud`, `longitud`.

---

## 🛠️ Perfil de Colaborador (Configuración)

### `POST /colaboradores`
- **Uso**: Inicializar perfil profesional.

### `POST /colaboradores/{id}/documentacion`
- **Uso**: Carga de documentos legales para certificación.

### `POST /colaboradores/{id}/precios-dinamicos`
- **Uso**: Configuración de reglas de cobro variables.

### `POST /colaboradores/{id}/horarios`
- **Uso**: Establecer ventanas de disponibilidad semanal.

---

## 📝 Operativa de Servicios

### `POST /solicitudes`
- **Uso**: Crear un nuevo contrato de servicio.

### `GET /solicitudes?usuario_id={id}`
- **Uso**: Listar pedidos de un usuario específico.

### `GET /solicitudes/{id}/mensajes`
- **Uso**: Recuperar historial de chat de una orden.

### `POST /solicitudes/{id}/mensajes`
- **Uso**: Enviar un nuevo mensaje dentro del chat de servicio.

### `POST /calificaciones`
- **Uso**: Evaluar un servicio terminado.
- **Campos**: `solicitud_id`, `puntuacion`, `aspectos` (lista: puntualidad, limpieza, calidad), `comentario`.
