from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesaria para las sesiones

# --- CONFIGURACIÓN DE LA API ---
API_BASE_URL = "http://localhost:3000"

def api_get(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        return response.json() if response.status_code == 200 else None
    except:
        return None

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        return response.json() if response.status_code in [200, 201] else None
    except:
        return None

# --- VERIFICACIÓN DE SESIÓN ---
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# --- RUTAS PÚBLICAS ---

@app.route('/')
def index():
    categorias = api_get("/categorias")
    if categorias is None:
        categorias = []
    return render_template('index.html', categorias=categorias)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['contrasenna']
        
        # Buscamos usuario por email
        usuarios = api_get("/usuarios")
        usuario = next((u for u in usuarios if u['correo'] == email), None)
        
        if usuario and usuario['contrasenna'] == password:
            # ✅ GUARDAMOS EN SESIÓN LOS DATOS DEL USUARIO
            session['user_id'] = usuario['id']
            session['nombre'] = usuario['nombre']
            session['correo'] = usuario['correo']
            return redirect(url_for('index'))
        else:
            return "Correo o contraseña incorrectos"
            
    return render_template('login.html')



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        contrasena = request.form.get('password')
        telefono=request.form.get('telefono')

        
        datos_usuario = {
        "nombre": nombre,
        "correo": email,
        "contrasena": password,
        "telefono": telefono, 
    }

        respuesta = api_post("/usuarios", datos_usuario)
        
        if respuesta:
            return redirect(url_for('login'))
        else:
            return "Error al registrar usuario"

    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- RUTAS PROTEGIDAS (Requieren estar logueado) ---

@app.route('/pedir', methods=['GET', 'POST'])
@login_required
def pedir():
    if request.method == 'POST':
        subcategoria_id = request.form.get('subcategoria_id', 1)
        descripcion = request.form.get('descripcion')
        urgencia = request.form.get('urgencia', 'media')
        lat = request.form.get('latitud', 19.4326)
        lon = request.form.get('longitud', -99.1332)

        # 🆕 MANEJO DE ARCHIVO
        foto = request.files.get('foto')
        ruta_foto = ""
        if foto and foto.filename != '':
            # Aquí podrías guardarla físicamente si quieres
            ruta_foto = foto.filename # Por ahora guardamos solo el nombre

        datos_solicitud = {
            "usuario_id": session['user_id'],
            "colaborador_id": request.args.get('colaborador_id', 1),
            "subcategoria_id": int(subcategoria_id),
            "urgencia": urgencia,
            "descripcion_detallada": descripcion,
            "fotos_evidencia_inicial": ruta_foto, # ✅ LA MANDAMOS A LA API
            "latitud": float(lat),
            "longitud": float(lon)
        }

        respuesta = api_post("/solicitudes", datos_solicitud)
        
        if respuesta:
            return f"✅ Solicitud creada con éxito! ID: {respuesta.get('id')}"
        else:
            return "❌ Error al crear la solicitud"

    return render_template('pedir.html')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email = request.form['email']
        return f"Enlace enviado a {email} (simulado)"
    return render_template('recuperar.html')

@app.route('/publicar')
@login_required
def publicar():
    return render_template('publicar.html')

# --- TEST ---

@app.route('/test')
def test():
    respuesta = api_get("/")
    if respuesta:
        return f"🔌 Conectado: {respuesta}"
    return "❌ No conectado"
     # --- MARKETPLACE DE COLABORADORES ---

@app.route('/marketplace/<int:subcategoria_id>')
@login_required
def marketplace(subcategoria_id):
    # Consultamos la API para obtener los trabajadores de esa categoría
    colaboradores = api_get(f"/subcategorias/{subcategoria_id}/colaboradores")
    
    if colaboradores is None:
        colaboradores = []
        
    return render_template('marketplace.html', colaboradores=colaboradores, subcat_id=subcategoria_id)
# --- DASHBOARD DE USUARIO ---

@app.route('/mis_pedidos')
@login_required
def mis_pedidos():
    # Consultamos las solicitudes de ESTE usuario
    usuario_id = session['user_id']
    solicitudes = api_get(f"/solicitudes?usuario_id={usuario_id}")
    
    if solicitudes is None:
        solicitudes = []
        
    return render_template('mis_pedidos.html', solicitudes=solicitudes)
# --- CHAT EN VIVO ---

@app.route('/chat/<int:solicitud_id>')
@login_required
def chat(solicitud_id):
    # Consultamos los mensajes de esta solicitud
    mensajes = api_get(f"/solicitudes/{solicitud_id}/mensajes")
    
    if mensajes is None:
        mensajes = []
        
    return render_template('chat.html', mensajes=mensajes, solicitud_id=solicitud_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

   