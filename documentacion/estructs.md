# 🏗️ Estructuras de Datos

Este documento detalla los objetos de datos principales utilizados en la interfaz de **Okupo** y su correspondencia con el motor **Finite**.

---

## 👤 Usuarios y Colaboradores

### Usuario
Estructura base para cualquier persona registrada en la plataforma.
- `id`: Entero único.
- `nombre`: Nombre completo del usuario.
- `correo`: Dirección de correo electrónico (identificador).
- `contrasenna`: Hash de la clave de acceso.

### Colaborador
Extensión del perfil de usuario para quienes prestan servicios.
- `id`: Identificador de colaborador.
- `usuario_id`: Relación con la tabla base de usuarios.
- `telefono`: Contacto directo.
- `sitio_web`: (Opcional) Portafolio externo.
- `reputacion`: Calificación promedio.

---

## 🛠️ Servicios y Categorización

### Categoria
Grandes grupos de servicios (ej: Hogar, Mecánica).
- `id`: Identificador.
- `nombre`: Etiqueta visible.

### Subcategoria
Servicios específicos dentro de una categoría (ej: Plomería dentro de Hogar).
- `id`: Identificador.
- `categoria_id`: Relación con la categoría padre.
- `nombre`: Nombre del servicio específico.

---

## 💰 Precios y Horarios

### Precios Dinámicos
Configuración de costos variables para el colaborador.
- `precio_por_kilometro`: Costo base por desplazamiento.
- `recargo_lluvia`: Multiplicador por condiciones climáticas.
- `recargo_domingo`: Multiplicador por día festivo.
- `recargo_nocturno`: Multiplicador por horario fuera de oficina.

### Horario de Disponibilidad
- `dia_semana`: 0 (Domingo) a 6 (Sábado).
- `hora_inicio`: Formato HH:MM.
- `hora_fin`: Formato HH:MM.
- `activo`: Booleano para indicar disponibilidad ese día.

---

## 📝 Solicitudes y Chat

### Solicitud de Servicio
El objeto central que representa una tarea contratada.
- `usuario_id`: Quien pide el servicio.
- `colaborador_id`: Quien realiza el servicio.
- `subcategoria_id`: Qué tipo de trabajo es.
- `urgencia`: Nivel de prioridad (baja, media, alta).
- `descripcion_detallada`: Texto explicativo del problema.
- `fotos_evidencia_inicial`: Lista de URLs o rutas a imágenes.
- `latitud / longitud`: Ubicación exacta del servicio.

### Mensaje de Chat
- `solicitud_id`: Contexto de la conversación.
- `emisor_id`: ID del usuario que envía el mensaje.
- `contenido`: Texto del mensaje.
- `timestamp`: Fecha y hora del envío.
