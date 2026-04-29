from flask import Blueprint, render_template, request, redirect, url_for, session
from src.infraestructura.cliente_api import api_post
from src.aplicacion.utilidades_token import obtener_usuario_id_de_token

blueprint = Blueprint('autenticacion', __name__)

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('principal.index'))
        
    mensaje = request.args.get('mensaje')
    if request.method == 'POST':
        email = request.form.get('email')
        contrasenna = request.form.get('contrasenna')
        
        token = api_post("/login", {"correo": email, "contrasenna": contrasenna})
        
        if token and token != "UNAUTHORIZED":
            usuario_id = obtener_usuario_id_de_token(token)
            if usuario_id:
                session.clear()
                session['user_id'] = int(usuario_id)
                session['nombre'] = email.split('@')[0].capitalize()
                session['correo'] = email
                session['token'] = token
                return redirect(url_for('principal.index'))
        
        return render_template('login.html', error="Correo o contrasenna incorrectos")
            
    return render_template('login.html', mensaje=mensaje)

@blueprint.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'user_id' in session:
        return redirect(url_for('principal.index'))
        
    rol = request.args.get('rol', 'cliente')
    if request.method == 'POST':
        datos_usuario = {
            "nombre": request.form.get('nombre'),
            "correo": request.form.get('email'),
            "contrasenna": request.form.get('password')
        }
        respuesta = api_post("/usuarios", datos_usuario)
        if respuesta and respuesta != "UNAUTHORIZED":
            if rol == 'colaborador':
                return redirect(url_for('autenticacion.login', mensaje="¡Cuenta creada! Inicia sesión para configurar tu perfil técnico."))
            return redirect(url_for('autenticacion.login', mensaje="Cuenta creada con éxito. Ya puedes iniciar sesión."))
        return render_template('registro.html', error="Error al registrar. Intenta con otro correo.")
    return render_template('registro.html', rol=rol)

@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('principal.index'))
