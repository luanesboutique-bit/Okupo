# ⚙️ Funciones y Rutas

Este documento describe la lógica de orquestación de **Okupo**, detallando cómo se procesan las solicitudes de los usuarios y cómo se comunica con el motor central.

---

## 🌐 Gestión de Rutas (Flask)

### 🏠 Flujo de Cliente
- `index()`: Punto de entrada. Recupera y muestra las categorías principales disponibles.
- `ver_subcategorias(categoria_id)`: Filtra servicios específicos según la categoría elegida.
- `marketplace(subcategoria_id)`: Muestra colaboradores disponibles cercanos (usa geolocalización por defecto).
- `pedir()`: Gestiona el formulario para crear una nueva solicitud de servicio.
- `mis_pedidos()`: Panel personal del usuario para ver el historial y estado de sus servicios.

### 🛠️ Flujo de Colaborador (Registro Técnico)
Okupo guía a los profesionales a través de un proceso de alta detallado:
1. `registro_tecnico_docs()`: Captura de documentos de identidad (INE, Comprobante).
2. `registro_tecnico_categorias()`: Selección de especialidades.
3. `registro_tecnico_precios()`: Configuración de tarifas dinámicas (km, lluvia, nocturno).
4. `registro_tecnico_horarios()`: Definición de la ventana de servicio semanal.

---

## 🔌 Utilidades del Sistema

### `api_get(endpoint)` / `api_post(endpoint, data)`
Funciones envolventes de la librería `requests` que centralizan la comunicación con el motor Finite.
- Manejan errores de conexión.
- Procesan respuestas JSON.
- Extraen tokens de autenticación.

### `get_user_id_from_token(token)`
Decodifica manualmente el payload de un JWT para obtener el identificador único del usuario (`sub`) sin depender de librerías externas pesadas.

### `login_required(f)`
Decorador de seguridad que asegura que ciertas rutas solo sean accesibles por usuarios autenticados, redirigiendo al login en caso contrario.

---

## 💬 Comunicación en Tiempo Real
- `chat(solicitud_id)`: Orquesta el intercambio de mensajes entre el cliente y el colaborador dentro del contexto de una solicitud activa.
