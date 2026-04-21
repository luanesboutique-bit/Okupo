from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# URL BASE DE LA API DE TU AMIGO
API_URL = "http://localhost:3000"

# Página de Inicio
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicio')
def servicio():
    return render_template('servicio.html')

@app.route('/plomeria')
def plomeria():
    from datetime import datetime
    
    # PRECIOS EXACTOS DE PLOMERÍA
    servicios = [
        {
            "nombre": "Instalación de mezcladora",
            "precio_base": 450,
            "precio_noche": 650,
            "precio_festivo": 900
        },
        {
            "nombre": "Herraje de sanitario",
            "precio_base": 450,
            "precio_noche": 600,
            "precio_festivo": 850
        },
        {
            "nombre": "Destape drenaje (Guía)",
            "precio_base": 550,
            "precio_noche": 800,
            "precio_festivo": 1100
        },
        {
            "nombre": "Kit de regadera",
            "precio_base": 450,
            "precio_noche": 600,
            "precio_festivo": 850
        }
    ]

    # LÓGICA DE TARIFAS
    ahora = datetime.now()
    hora = ahora.hour
    dia = ahora.weekday()
    
    es_noche = hora >= 20 or hora < 6
    es_festivo = dia == 6 
    hay_lluvia = False 

    # CALCULAR PRECIOS
    servicios_con_precio = []
    for serv in servicios:
        if es_noche:
            precio_final = serv["precio_noche"]
            leyenda = "Tarifa elevada por horario nocturno"
            color = "text-red-600"
        elif es_festivo or hay_lluvia:
            precio_final = serv["precio_festivo"]
            leyenda = "Tarifa elevada por día festivo,Domingo o clima"
            color = "text-red-600"
        else:
            precio_final = serv["precio_base"]
            leyenda = ""
            color = "text-green-600"
        
        servicios_con_precio.append({
            "nombre": serv["nombre"],
            "precio": precio_final,
            "leyenda": leyenda,
            "color": color
        })

    return render_template('plomeria.html', servicios=servicios_con_precio)

@app.route('/electricidad')
def electricidad():
    from datetime import datetime
    
    # PRECIOS EXACTOS DE ELECTRICIDAD
    servicios = [
        {
            "nombre": "Instalacion Ventilador de Techo",
            "precio_base": 550,
            "precio_noche": 800,
            "precio_festivo": 1200
        },
        {
            "nombre": "Cambio Contactos / Apagadores (1-3 piezas)",
            "precio_base": 450,
            "precio_noche": 650,
            "precio_festivo": 900
        },
        {
            "nombre": "Instalacion Lámpara o Candelabro",
            "precio_base": 450,
            "precio_noche": 650,
            "precio_festivo": 950
        },
        {
            "nombre": "Revisión Centro de Carga(Pastillas luz)",
            "precio_base": 500,
            "precio_noche": 750,
            "precio_festivo": 1100
        }
    ]

    # LÓGICA DE TARIFAS
    ahora = datetime.now()
    hora = ahora.hour
    dia = ahora.weekday()
    
    es_noche = hora >= 20 or hora < 6
    es_festivo = dia == 6 
    hay_lluvia = False 

    # CALCULAR PRECIOS
    servicios_con_precio = []
    for serv in servicios:
        if es_noche:
            precio_final = serv["precio_noche"]
            leyenda = "Tarifa elevada por horario nocturno"
            color = "text-red-600"
        elif es_festivo or hay_lluvia:
            precio_final = serv["precio_festivo"]
            leyenda = "Tarifa elevada por día festivo o clima"
            color = "text-red-600"
        else:
            precio_final = serv["precio_base"]
            leyenda = ""
            color = "text-green-600"
        
        servicios_con_precio.append({
            "nombre": serv["nombre"],
            "precio": precio_final,
            "leyenda": leyenda,
            "color": color
        })

    return render_template('electricidad.html', servicios=servicios_con_precio)
@app.route('/cerrajeria')
def cerrajeria():
    from datetime import datetime
    
    # SERVICIOS DE CERRAJERÍA CON SUS 3 TARIFAS
    servicios = [
        {
            "nombre": "🔓 Apertura de emergencia",
            "descripcion": "Me quedé fuera",
            "detalle": "Abrimos tu puerta sin daños en minutos.",
            "nota": "⚠️ Precio por apertura no destructiva. Si requiere romper la chapa, el cambio de pieza tiene costo extra.\n📎 Se requiere identificación oficial para acreditar propiedad.",
            "precio_base": 600,
            "precio_noche": 950,
            "precio_festivo": 1500
        },
        {
            "nombre": "🚪 Cambio de chapa de pomo",
            "descripcion": "Recámaras / Baños",
            "detalle": "Precio fijo por mano de obra (quitar vieja y poner nueva).",
            "nota": "El costo NO incluye el material. El cliente trae la chapa o se cotiza aparte.",
            "precio_base": 500,
            "precio_noche": 750,
            "precio_festivo": 1000
        },
        {
            "nombre": "🛡️ Instalación chapa de Alta seguridad",
            "descripcion": "Entrada principal",
            "detalle": "Para puertas de calle, barras o digitales.",
            "nota": "Precio por instalación y ajuste fino. Incluye perforaciones necesarias.",
            "precio_base": 700,
            "precio_noche": 1000,
            "precio_festivo": 1400
        }
    ]

    # LÓGICA PARA ELEGIR LA TARIFA CORRECTA
    ahora = datetime.now()
    hora = ahora.hour
    dia = ahora.weekday()
    
    es_noche = hora >= 20 or hora < 6
    es_festivo = dia == 6  # Domingo
    hay_lluvia = False 

    # CALCULAR PRECIO FINAL
    servicios_con_precio = []
    for serv in servicios:
        if es_noche:
            precio_final = serv["precio_noche"]
            leyenda = "Tarifa elevada por horario nocturno"
            color = "text-red-600"
        elif es_festivo or hay_lluvia:
            precio_final = serv["precio_festivo"]
            leyenda = "Tarifa elevada por día festivo,Domingo o clima"
            color = "text-red-600"
        else:
            precio_final = serv["precio_base"]
            leyenda = ""
            color = "text-green-600"
        
        servicios_con_precio.append({
            "nombre": serv["nombre"],
            "descripcion": serv["descripcion"],
            "detalle": serv["detalle"],
            "nota": serv["nota"],
            "precio": precio_final,
            "leyenda": leyenda,
            "color": color
        })

    return render_template('cerrajeria.html', servicios=servicios_con_precio)
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password'].encode('utf-8')

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, password, tipo_usuario FROM usuarios WHERE email = %s", [email])
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
        session['user_id'] = user[0]
        session['nombre'] = user[1]
        session['tipo'] = user[3]
        return redirect(url_for('index'))
    else:
        return "Correo o contraseña incorrectos"

@app.route('/registro')
def registro_page():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['confirmar_password']
    tipo = request.form['tipo_usuario']

    # VERIFICAR QUE SEAN IGUALES
    if password != password2:
        return "Las contraseñas no coinciden. Intenta de nuevo."

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (nombre, email, password, tipo_usuario) VALUES (%s, %s, %s, %s)", 
                (nombre, email, hashed.decode('utf-8'), tipo))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('login_page'))

@app.route('/recuperar')
def recuperar_page():
    return render_template('recuperar.html')

@app.route('/recuperar', methods=['POST'])
def recuperar():
    email = request.form['email']
    return f"Se ha enviado un enlace de recuperación al correo {email}"
    
    # AQUÍ IRÍA EL CÓDIGO PARA ENVIAR EL CORREO
    # Por ahora solo mostramos mensaje
    return f"Se ha enviado un enlace de recuperación al correo {email} (Funcionalidad de envío de email pendiente)"
# Página para SOLICITAR SERVICIO (Cliente)
@app.route('/pedir', methods=['GET', 'POST'])
def pedir():
    if request.method == 'POST':
        # 1. Tomamos datos del formulario
        titulo = request.form.get('titulo')
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        ubicacion = request.form.get('ubicacion')

        # 2. Preparamos el JSON exacto como pide la API
        datos = {
            "nombre": "Cliente OKUPO",
            "correo": "cliente@okupo.com",
            "telefono": "000000000",
            "sitio_web": "",
            "servicios": [
                [
                    {
                        "colaborador_id": 0,
                        "categoria_id": 1,
                        "descripcion": descripcion,
                        "distancia_maxima_kilometros": 10.0,
                        "precio_por_kilometro": 0.0,
                        "latitud": 0.0,
                        "longitud": 0.0
                    }
                ],
                [
                    {
                        "servicio_id": 0,
                        "urgencia": "media",
                        "precio": float(precio)
                    }
                ]
            ]
        }

        # 3. Enviamos a la API
        try:
            respuesta = requests.post(
                f"{API_URL}/colaboradores", 
                data=json.dumps(datos),
                headers={'Content-Type': 'application/json'}
            )
            return f"✅ Enviado! Respuesta Backend: {respuesta.text}"
        except Exception as e:
            return f"❌ Error de conexión: {str(e)}"

    return render_template('pedir.html')

# Página para OFRECER SERVICIOS (Trabajador)
@app.route('/publicar')
def publicar():
    return render_template('publicar.html')

# PRUEBA RÁPIDA: Ver si la API está viva
@app.route('/test')
def test():
    try:
        r = requests.get(f"{API_URL}/")
        return f"🔌 Conexión exitosa! Servidor responde: {r.text}"
    except:
        return "❌ No se pudo conectar a la API. ¿Está encendida?"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt

# ... TU CÓDIGO DE CONEXIÓN A LA DB ...

