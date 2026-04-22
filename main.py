from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'okupo_secret_key' # Debería cambiarse a algo seguro

# URL BASE DE LA API DE FINITE (Motor de búsqueda)
# Asegúrate de que el motor finit esté corriendo en el puerto 3000
API_URL = "http://localhost:3000"

# --- HELPERS PARA CONSUMIR LA API ---

def api_get(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Error en GET {endpoint}: {e}")
        return None

def api_post(endpoint, data):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except:
                return response.text
        return None
    except Exception as e:
        print(f"Error en POST {endpoint}: {e}")
        return None

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
def index():
    # Podríamos obtener las categorías dinámicamente
    # categorias = api_get("/categorias")
    return render_template('index.html')

@app.route('/servicio')
def servicio():
    return render_template('servicio.html')

@app.route('/plomeria')
def plomeria():
    # ID de Plomería en la DB (Asumimos 1 según api_uso.md ejemplo)
    # En un sistema real, buscaríamos el ID por nombre
    categoria_id = 1 
    subcategorias = api_get(f"/categorias/{categoria_id}/subcategorias")
    
    if not subcategorias:
        # Fallback por si la API no responde o no tiene datos
        subcategorias = [
            {"id": 1, "nombre": "Instalación de mezcladora", "descripcion": "Servicio estándar"},
            {"id": 2, "nombre": "Herraje de sanitario", "descripcion": "Cambio de herrajes"},
            {"id": 3, "nombre": "Destape drenaje (Guía)", "descripcion": "Limpieza de tubería"},
            {"id": 4, "nombre": "Kit de regadera", "descripcion": "Instalación completa"}
        ]

    # LÓGICA DE TARIFAS (Simulada para mantener el feeling del front original)
    ahora = datetime.now()
    hora = ahora.hour
    dia = ahora.weekday()
    
    es_noche = hora >= 20 or hora < 6
    es_festivo = dia == 6 

    servicios_con_precio = []
    for sub in subcategorias:
        # Aquí Finite debería darnos el precio, pero como es dinámico por colaborador,
        # mantenemos una lógica base para el front.
        precio_base = 450
        if es_noche:
            precio_final = precio_base + 200
            leyenda = "Tarifa nocturna activa"
            color = "text-red-600"
        elif es_festivo:
            precio_final = precio_base + 400
            leyenda = "Tarifa de día festivo"
            color = "text-red-600"
        else:
            precio_final = precio_base
            leyenda = ""
            color = "text-green-600"
        
        servicios_con_precio.append({
            "id": sub.get("id"),
            "nombre": sub.get("nombre"),
            "precio": precio_final,
            "leyenda": leyenda,
            "color": color
        })

    return render_template('plomeria.html', servicios=servicios_con_precio)

@app.route('/electricidad')
def electricidad():
    categoria_id = 2 # Asumido
    subcategorias = api_get(f"/categorias/{categoria_id}/subcategorias")
    
    if not subcategorias:
        subcategorias = [
            {"id": 5, "nombre": "Instalación Ventilador", "descripcion": ""},
            {"id": 6, "nombre": "Cambio Contactos", "descripcion": ""},
            {"id": 7, "nombre": "Instalación Lámpara", "descripcion": ""},
            {"id": 8, "nombre": "Revisión Centro Carga", "descripcion": ""}
        ]

    # Lógica similar a plomeria...
    return render_template('electricidad.html', servicios=subcategorias)

@app.route('/cerrajeria')
def cerrajeria():
    categoria_id = 3 # Asumido
    subcategorias = api_get(f"/categorias/{categoria_id}/subcategorias")
    return render_template('cerrajeria.html', servicios=subcategorias)

# --- AUTENTICACIÓN (USANDO API FINITE) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Consumimos el endpoint de login de finit
        respuesta = api_post("/login", {
            "correo": email,
            "contrasenna": password
        })

        if respuesta:
            # finit devuelve un token JWT en caso de éxito
            session['token'] = respuesta 
            session['email'] = email
            return redirect(url_for('index'))
        else:
            return "Correo o contraseña incorrectos (API finit)"

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        # Registro en finit
        respuesta = api_post("/usuarios", {
            "nombre": nombre,
            "correo": email,
            "contrasenna": password
        })

        if respuesta:
            return redirect(url_for('login'))
        else:
            return "Error al registrar usuario en la API"

    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- SOLICITUD DE SERVICIOS (USANDO API FINITE) ---

@app.route('/pedir', methods=['GET', 'POST'])
def pedir():
    if request.method == 'POST':
        # Datos del formulario del front
        subcategoria_id = request.form.get('subcategoria_id', 1)
        descripcion = request.form.get('descripcion')
        urgencia = request.form.get('urgencia', 'media')
        lat = request.form.get('latitud', 19.4326) # CDMX default
        lon = request.form.get('longitud', -99.1332)

        # JSON exacto según api_uso.md de finit
        datos_solicitud = {
            "usuario_id": session.get('user_id', 1), # Debería venir del JWT decodificado
            "colaborador_id": 1, # En un flujo real, se elige del Marketplace primero
            "subcategoria_id": int(subcategoria_id),
            "urgencia": urgencia,
            "descripcion_detallada": descripcion,
            "fotos_evidencia_inicial": "",
            "latitud": float(lat),
            "longitud": float(lon)
        }

        respuesta = api_post("/solicitudes", datos_solicitud)
        
        if respuesta:
            return f"✅ Solicitud creada con éxito en finit! ID: {respuesta.get('id')}"
        else:
            return "❌ Error al crear la solicitud en el motor finit."

    return render_template('pedir.html')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email = request.form['email']
        return f"Se ha enviado un enlace de recuperación al correo {email} (Simulado)"
    return render_template('recuperar.html')

@app.route('/publicar')
def publicar():
    return render_template('publicar.html')

# --- TEST DE CONEXIÓN ---

@app.route('/test')
def test():
    respuesta = api_get("/")
    if respuesta:
        return f"🔌 Conectado a Finite: {respuesta}"
    return "❌ No se pudo conectar al motor Finite (Puerto 3000)"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
