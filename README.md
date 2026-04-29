# 🚀 Okupo

**Okupo** es el marketplace de servicios que dignifica a quienes trabajan y simplifica la vida de quienes necesitan soluciones. Es la interfaz humana y transparente impulsada por el motor [Finite](../../Finite/README.md).

---

## 💎 Filosofía y Visión

Creemos en la transparencia radical y en la dignidad laboral. En Okupo, la tecnología está al servicio de las personas, no al revés.

👉 **Lee nuestro [Manifiesto de Transparencia](documentacion/manifiesto.md)** para entender cómo estamos cambiando las reglas del juego.

---

## ✨ Características Principales

- ⚡ **Solicitud Instantánea**: Emparejamiento automático con colaboradores certificados para soluciones urgentes.
- 🔍 **Marketplace Abierto**: Libertad para explorar perfiles, comparar precios y elegir al colaborador ideal.
- 📅 **Agenda Inteligente**: Sincronización automática de horarios para evitar conflictos y optimizar el tiempo.
- 💰 **Precios Claros**: Distribución del pago totalmente visible para el usuario y el colaborador.

---

## 🛠️ Tecnologías

- **Backend**: Python con [Flask](https://flask.palletsprojects.com/) (Interfaz de Usuario).
- **Motor Central**: [Finite](../../Finite/README.md) (Rust + MySQL).
- **Frontend**: HTML5, Jinja2 Templates, CSS3 (Vanilla).
- **API**: Integración RESTful con motor de proximidad.

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.10+
- Motor **Finite** en ejecución (Puerto 3000).

### Instalación
```bash
# Clonar el repositorio
git clone <url-del-repo>
cd Okupo

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

La plataforma estará disponible en `http://localhost:5000`.

---

## 📂 Estructura del Proyecto

- `main.py`: Lógica de rutas, sesiones y conexión con la API de Finite.
- `templates/`: Vistas de la aplicación (Index, Login, Marketplace, Registro Técnico).
- `static/`: Recursos estáticos (CSS, Imágenes).
- `documentacion/`: Planos técnicos y manifiesto filosófico.

### 📚 Documentación Detallada
Para profundizar en el funcionamiento interno de Okupo:
- [📜 Manifiesto](documentacion/manifiesto.md)
- [🏗️ Estructuras de Datos](documentacion/estructs.md)
- [⚙️ Funciones y Rutas](documentacion/funciones.md)
- [🔌 Integración API](documentacion/api_uso.md)

---

## 📜 Reglas de Desarrollo

Siguiendo el estándar de la casa:
- **Idioma**: Español.
- **Sin 'ñ'**: Se utiliza 'nn' (ej: `contrasenna`, `categoria_id`).
- **Nomenclatura**: Descriptiva y clara, sin abreviaturas innecesarias.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
