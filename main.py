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

@app.route('/unete')
def landing_colaborador():
    return render_template('landing_colaborador.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    mensaje = request.args.get('mensaje')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('contrasenna')
        
        token = api_post("/login", {"correo": email, "contrasenna": password})
        
        if token:
            user_id = get_user_id_from_token(token)
            if user_id:
                session.clear()
                session['user_id'] = int(user_id)
                session['nombre'] = email.split('@')[0].capitalize()
                session['correo'] = email
                session['token'] = token
                
                # Intentamos ver si ya tiene un perfil de colaborador
                # (Asumiendo que hay un endpoint para buscar por usuario_id o similar)
                # Por ahora, si venia de un flujo de registro tecnico, lo mandamos alla
                return redirect(url_for('index'))
        
        return render_template('login.html', error="Correo o contraseña incorrectos")
            
    return render_template('login.html', mensaje=mensaje)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    rol = request.args.get('rol', 'cliente')
    if request.method == 'POST':
        datos_usuario = {
            "nombre": request.form.get('nombre'),
            "correo": request.form.get('email'),
            "contrasenna": request.form.get('password')
        }
        respuesta = api_post("/usuarios", datos_usuario)
        if respuesta:
            if rol == 'colaborador':
                return redirect(url_for('login', mensaje="¡Cuenta creada! Inicia sesión para configurar tu perfil técnico."))
            return redirect(url_for('login', mensaje="Cuenta creada con éxito. Ya puedes iniciar sesión."))
        return render_template('registro.html', error="Error al registrar. Intenta con otro correo.")
    return render_template('registro.html', rol=rol)

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

# --- FLUJO REGISTRO TÉCNICO ---

@app.route('/registro/tecnico/docs', methods=['GET', 'POST'])
@login_required
def registro_tecnico_docs():
    if request.method == 'POST':
        # Primero necesitamos asegurar que existe el colaborador en la DB de la API
        # Si ya existe, solo actualizamos los documentos.
        # Por ahora intentaremos registrarlo con info basica.
        colaborador_id = session.get('colaborador_id')
        
        if not colaborador_id:
            # Crear entrada basica de colaborador si no existe
            resp = api_post("/colaboradores", {
                "token_usuario": session['token'],
                "telefono": request.form.get('telefono'),
                "sitio_web": None,
                "servicios": []
            })
            if resp:
                colaborador_id = int(resp)
                session['colaborador_id'] = colaborador_id

        # Actualizar Documentacion
        datos_docs = {
            "ine_frontal": request.form.get('ine_frontal'),
            "ine_trasera": request.form.get('ine_trasera'),
            "comprobante_domicilio": request.form.get('comprobante_domicilio'),
            "foto_selfie_ine": request.form.get('foto_selfie_ine')
        }
        api_post(f"/colaboradores/{colaborador_id}/documentacion", datos_docs)
        
        return redirect(url_for('registro_tecnico_categorias'))

    return render_template('registro_tecnico_docs.html')

@app.route('/registro/tecnico/categorias', methods=['GET', 'POST'])
@login_required
def registro_tecnico_categorias():
    if request.method == 'POST':
        # Aqui capturaremos las subcategorias y precios base
        return redirect(url_for('registro_tecnico_precios'))
    
    categorias = api_get("/categorias") or []
    return render_template('registro_tecnico_categorias.html', categorias=categorias)

@app.route('/registro/tecnico/precios', methods=['GET', 'POST'])
@login_required
def registro_tecnico_precios():
    colaborador_id = session.get('colaborador_id')
    if request.method == 'POST':
        datos_precios = {
            "precio_por_kilometro": float(request.form.get('precio_km')),
            "recargo_lluvia": float(request.form.get('recargo_lluvia')),
            "recargo_domingo": float(request.form.get('recargo_domingo')),
            "recargo_nocturno": float(request.form.get('recargo_nocturno'))
        }
        api_post(f"/colaboradores/{colaborador_id}/precios-dinamicos", datos_precios)
        return redirect(url_for('registro_tecnico_horarios'))
        
    return render_template('registro_tecnico_precios.html')

@app.route('/registro/tecnico/horarios', methods=['GET', 'POST'])
@login_required
def registro_tecnico_horarios():
    colaborador_id = session.get('colaborador_id')
    if request.method == 'POST':
        horarios = []
        for i in range(7):
            if request.form.get(f'dia_{i}_activo'):
                horarios.append({
                    "colaborador_id": colaborador_id,
                    "dia_semana": i,
                    "hora_inicio": request.form.get(f'dia_{i}_inicio'),
                    "hora_fin": request.form.get(f'dia_{i}_fin'),
                    "activo": True
                })
        api_post(f"/colaboradores/{colaborador_id}/horarios", horarios)
        return redirect(url_for('index', registro_exitoso=True))

    return render_template('registro_tecnico_horarios.html')

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
