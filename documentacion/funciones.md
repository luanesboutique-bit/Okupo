# ⚙️ Funciones y Estructura del Código

Este documento describe la lógica de orquestación de **Okupo** y su nueva arquitectura limpia, detallando cómo se organizan los componentes para mantener un bajo acoplamiento y facilitar el crecimiento del proyecto.

---

## 🏗️ Arquitectura Limpia

El proyecto se ha reestructurado siguiendo los principios de Arquitectura Limpia:

- **`src/infraestructura/`**: Contiene la configuración (`configuracion.py`) y el cliente de la API (`cliente_api.py`). Es la capa que se comunica con el exterior (motor Finite).
- **`src/aplicacion/`**: Contiene la lógica de negocio y utilidades, como el procesamiento de tokens JWT (`utilidades_token.py`).
- **`src/web/`**: Contiene la interfaz de usuario.
    - **`rutas/`**: Blueprints de Flask que organizan las rutas por funcionalidad (`autenticacion.py`, `principal.py`, `pedidos.py`, `colaboradores.py`).
    - **`decoradores.py`**: Lógica de seguridad para las rutas (ej. `login_requerido`).
- **`main.py`**: Punto de entrada que inicializa la aplicación Flask y registra los Blueprints.

---

## 🌐 Gestión de Rutas (Blueprints)

### 🏠 Principal (`rutas/principal.py`)
- `index()`: Punto de entrada. Recupera y muestra las categorías principales.
- `ver_subcategorias(categoria_id)`: Filtra servicios específicos.
- `marketplace(subcategoria_id)`: Muestra colaboradores cercanos.

### 🔑 Autenticación (`rutas/autenticacion.py`)
- `login()`: Gestión de inicio de sesión y almacenamiento de token en sesión.
- `registro()`: Alta de nuevos usuarios (clientes o colaboradores).
- `logout()`: Cierre de sesión y limpieza de datos.

### 📝 Pedidos (`rutas/pedidos.py`)
- `pedir()`: Creación de nuevas solicitudes de servicio.
- `mis_pedidos()`: Panel de historial de servicios del usuario.
- `chat(solicitud_id)`: Interfaz de mensajería para una solicitud activa.

### 🛠️ Colaboradores (`rutas/colaboradores.py`)
Flujo de registro técnico para profesionales:
1. `registro_tecnico_docs()`: Carga de documentos (INE, Comprobante).
2. `registro_tecnico_categorias()`: Selección de especialidades.
3. `registro_tecnico_precios()`: Configuración de tarifas dinámicas.
4. `registro_tecnico_horarios()`: Ventana de disponibilidad.

---

## 🔌 Utilidades del Sistema

### `cliente_api.py`
Funciones genéricas para la comunicación con el motor Finite:
- `api_get(endpoint, token)`: Peticiones GET autorizadas.
- `api_post(endpoint, datos, token)`: Peticiones POST autorizadas.
- Manejo centralizado de errores y respuestas "UNAUTHORIZED".

### `utilidades_token.py`
- `obtener_usuario_id_de_token(token)`: Decodificación segura del payload JWT para extraer el identificador del usuario (`sub`).

### `decoradores.py`
- `login_requerido(f)`: Asegura que el usuario esté autenticado antes de acceder a rutas protegidas.
