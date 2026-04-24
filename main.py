from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import requests
import os
import base64
import json

app = Flask(__name__)
app.secret_key = 'clave_secreta_okupo_2024'

# --- CONFIGURACIÓN DE LA API ---
API_BASE_URL = "http://localhost:3000"

@app.route('/favicon.ico')
def favicon():
    return "", 204

def api_get(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"DEBUG ERROR: GET {endpoint} -> {e}")
        return None

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        if response.status_code in [200, 201]:
            # Limpiamos comillas del token si vienen como string JSON
            return response.text.strip('"')
        print(f"DEBUG ERROR: POST {endpoint} ({response.status_code}) -> {response.text}")
        return None
    except Exception as e:
        print(f"DEBUG ERROR: POST {endpoint} -> {e}")
        return None

# Función para extraer el ID del Token JWT (sin librerías extras)
def get_user_id_from_token(token):
    try:
        parts = token.split('.')
        if len(parts) < 2: return None
        payload_b64 = parts[1]
        missing_padding = len(payload_b64) % 4
        if missing_padding: payload_b64 += '=' * (4 - missing_padding)
        payload_data = base64.b64decode(payload_b64).decode('utf-8')
        return json.loads(payload_data).get('sub')
    except:
        return None

# --- DECORADOR DE SESIÓN ---
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- RUTAS ---

@app.route('/')
def index():
    categorias = api_get("/categorias") or []
    return render_template('index.html', categorias=categorias)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('contrasenna')
        
        print(f"DEBUG: Intentando login para {email}...")
        token = api_post("/login", {"correo": email, "contrasenna": password})
        
        if token:
            user_id = get_user_id_from_token(token)
            if user_id:
                session.clear()
                session['user_id'] = int(user_id) # Convertimos a int por si viene como str
                session['nombre'] = email.split('@')[0].capitalize() # Usamos el alias del email
                session['correo'] = email
                session['token'] = token
                print(f"DEBUG: Login exitoso para {email} (ID extraído del token: {user_id})")
                return redirect(url_for('index'))
            else:
                print("DEBUG: Token recibido pero no se pudo extraer el ID (sub).")
        
        return render_template('login.html', error="Correo o contraseña incorrectos")
            
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        datos_usuario = {
            "nombre": request.form.get('nombre'),
            "correo": request.form.get('email'),
            "contrasenna": request.form.get('password')
        }
        respuesta = api_post("/usuarios", datos_usuario)
        if respuesta:
            return redirect(url_for('login'))
        return render_template('registro.html', error="Error al registrar. Intenta con otro correo.")
    return render_template('registro.html')

@app.route('/categorias/<int:categoria_id>/subcategorias')
def ver_subcategorias(categoria_id):
    subcategorias = api_get(f"/categorias/{categoria_id}/subcategorias") or []
    colores_cat = {1: "#C69B6F", 2: "#9E8B71", 3: "#ADA391", 4: "#C6B79F"}
    acento = colores_cat.get(categoria_id, "#C69B6F")
    return render_template('subcategorias.html', subcategorias=subcategorias, cat_id=categoria_id, acento=acento)

@app.route('/marketplace/<int:subcategoria_id>')
def marketplace(subcategoria_id):
    params = "?latitud=19.4326&longitud=-99.1332"
    colaboradores = api_get(f"/subcategorias/{subcategoria_id}/colaboradores{params}") or []
    return render_template('marketplace.html', colaboradores=colaboradores, subcat_id=subcategoria_id)

@app.route('/pedir', methods=['GET', 'POST'])
@login_required
def pedir():
    if request.method == 'POST':
        datos_solicitud = {
            "usuario_id": session['user_id'],
            "colaborador_id": int(request.form.get('colaborador_id', 1)),
            "subcategoria_id": int(request.form.get('subcategoria_id', 1)),
            "urgencia": request.form.get('urgencia', 'media'),
            "descripcion_detallada": request.form.get('descripcion'),
            "fotos_evidencia_inicial": "placeholder.jpg",
            "latitud": 19.4326,
            "longitud": -99.1332
        }
        respuesta = api_post("/solicitudes", datos_solicitud)
        if respuesta:
            return redirect(url_for('mis_pedidos'))
        return "Error al crear la solicitud", 500

    colaborador_id = request.args.get('colaborador_id')
    subcat_id = request.args.get('subcategoria_id')
    return render_template('pedir.html', colaborador_id=colaborador_id, subcat_id=subcat_id)

@app.route('/mis_pedidos')
@login_required
def mis_pedidos():
    solicitudes = api_get(f"/solicitudes?usuario_id={session['user_id']}") or []
    return render_template('mis_pedidos.html', solicitudes=solicitudes)

@app.route('/chat/<int:solicitud_id>', methods=['GET', 'POST'])
@login_required
def chat(solicitud_id):
    if request.method == 'POST':
        contenido = request.form.get('texto')
        api_post(f"/solicitudes/{solicitud_id}/mensajes", {
            "emisor_id": session['user_id'],
            "contenido": contenido
        })
        return redirect(url_for('chat', solicitud_id=solicitud_id))
    mensajes = api_get(f"/solicitudes/{solicitud_id}/mensajes") or []
    return render_template('chat.html', mensajes=mensajes, solicitud_id=solicitud_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
