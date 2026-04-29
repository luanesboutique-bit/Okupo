# 📝 Lista de Pendientes - Proyecto Okupo

Esta lista contiene las tareas necesarias para completar la integración del Frontend `Okupo` con el motor backend `Finite`.

## 🛠️ Integración con la API (Finite)
- [x] **Renderizado Dinámico de Categorías**: Modificar `index.html` para que cargue las categorías principales desde `/categorias` en lugar de tenerlas hardcodeadas.
- [ ] **Manejo de Sesión (JWT)**: Implementar la decodificación del token JWT recibido en `/login` para obtener el `usuario_id` y permisos.
- [ ] **Marketplace de Colaboradores**: Crear una vista de "Marketplace" que consuma `/subcategorias/:id/colaboradores` para que el usuario pueda elegir un profesional antes de crear la solicitud.
- [ ] **Flujo de Solicitudes**: Actualizar la ruta `/pedir` para que esté vinculada a un `colaborador_id` real seleccionado del Marketplace.
- [ ] **Evidencia Multimedia**: Implementar la subida de imágenes (o envío de URLs) para `fotos_evidencia_inicial` en las solicitudes.

## 🎨 Interfaz de Usuario (UI/UX)
- [ ] **Consistencia de Estilos**: Asegurar que todas las vistas usen el mismo redondeo de botones (`btn-categoria`) y paleta de colores.
- [ ] **Dashboard de Usuario**: Crear la vista de "Mis Pedidos" consumiendo `/solicitudes?usuario_id=X`.
- [ ] **Chat en Vivo**: Implementar la interfaz de mensajería usando los endpoints `/solicitudes/:id/mensajes`.

## ⚙️ Infraestructura y Limpieza
- [x] **Renombrar archivo principal**: Cambiado de `app.py` a `main.py` y movido a la raíz.
- [x] **Organización de Carpetas**: Movidos `templates/` y `static/` fuera de `venv/`.
- [ ] **Archivo de Dependencias**: Crear un `requirements.txt` con `flask`, `requests`, etc.
- [ ] **Variables de Entorno**: Mover la `API_URL` y `secret_key` a un archivo `.env`.

## 🧪 Pruebas
- [ ] **Validar Registro**: Probar el flujo completo de registro de usuario y verificar en la DB de Finite.
- [ ] **Test de Conexión**: Asegurar que la ruta `/test` responda correctamente cuando el motor Rust esté encendido.
