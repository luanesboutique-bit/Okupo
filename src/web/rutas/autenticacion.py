from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from src.infraestructura.cliente_api import api_post
from src.aplicacion.utilidades_token import obtener_usuario_id_de_token, obtener_rol_de_token

blueprint = Blueprint('autenticacion', __name__)

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('principal.index'))
        
    mensaje = request.args.get('mensaje')
    proximo = request.args.get('proximo')

    if request.method == 'POST':
        email = request.form.get('email')
        contrasenna = request.form.get('contrasenna')
        proximo = request.form.get('proximo')
        
        print(f"DEBUG: Intentando login con correo: {email}")
        respuesta = api_post("/login", {"correo": email, "contrasenna": contrasenna})
        print(f"DEBUG: Respuesta API Login: {respuesta}")
        
        if respuesta and respuesta != "UNAUTHORIZED":
            # Si respuesta es un string (el token mismo), úsalo directamente.
            # Si es un dict, intenta buscar la clave 'token'.
            if isinstance(respuesta, str):
                token = respuesta
            elif isinstance(respuesta, dict):
                token = respuesta.get('token', '')
            else:
                token = str(respuesta)
                
            print(f"DEBUG: Token extraido: {token}")
            
            usuario_id = obtener_usuario_id_de_token(token)
            rol = obtener_rol_de_token(token)
            print(f"DEBUG: Usuario ID decodificado: {usuario_id}, Rol: {rol}")

            if usuario_id:
                # Mantener la bandera de registro como colaborador si existe
                es_registro_colaborador = session.get('registro_como_colaborador')
                
                session.clear()
                session['user_id'] = int(usuario_id)
                session['nombre'] = email.split('@')[0].capitalize()
                session['correo'] = email
                session['token'] = token
                session['rol'] = rol
                print(f"DEBUG: Sesion guardada: {dict(session)}")
                
                if proximo:
                    return redirect(proximo)

                if es_registro_colaborador:
                    return redirect(url_for('colaboradores.registro_tecnico_datos'))
                
                if rol == 'colaborador':
                    return redirect(url_for('colaboradores.dashboard_colaborador'))
                return redirect(url_for('principal.index'))
            else:
                print("DEBUG: Fallo al decodificar ID del token")
        
        return render_template('login.html', error="Correo o contrasenna incorrectos", proximo=proximo)
            
    return render_template('login.html', mensaje=mensaje, proximo=proximo)

@blueprint.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'user_id' in session:
        return redirect(url_for('principal.index'))
        
    rol = request.args.get('rol', 'cliente')
    if request.method == 'POST':
        datos_usuario = {
            "nombre": request.form.get('nombre'),
            "correo": request.form.get('correo'),
            "contrasenna": request.form.get('contrasenna')
        }
        print(f"DEBUG: Intentando registrar: {datos_usuario}")
        respuesta = api_post("/usuarios", datos_usuario)
        print(f"DEBUG: Respuesta registro: {respuesta}")
        if respuesta and respuesta != "UNAUTHORIZED":
            if rol == 'colaborador':
                session['registro_como_colaborador'] = True
                return redirect(url_for('autenticacion.login', mensaje="¡Cuenta creada! Inicia sesión para configurar tu perfil técnico."))
            return redirect(url_for('autenticacion.login', mensaje="Cuenta creada con éxito. Ya puedes iniciar sesión."))
        return render_template('registro.html', error="Error al registrar. Intenta con otro correo.")
    return render_template('registro.html', rol=rol)

@blueprint.route('/login/social/<red_social>', methods=['GET', 'POST'])
def login_social(red_social):
    if request.method == 'GET':
        return f"Proceso de autenticación con {red_social} en curso. Asegúrate de enviar un POST con tu token."
        
    token_social = request.json.get('token')
    if not token_social:
        return jsonify({"status": "error", "message": "Token social no proporcionado"}), 400
    
    endpoint = f"/auth/{red_social}"
    respuesta = api_post(endpoint, {"token": token_social})
    
    if respuesta and respuesta != "UNAUTHORIZED" and isinstance(respuesta, dict):
        token_jwt = respuesta.get('token')
        usuario_id = obtener_usuario_id_de_token(token_jwt)
        rol = obtener_rol_de_token(token_jwt)
        
        session.clear()
        session['user_id'] = int(usuario_id)
        session['token'] = token_jwt
        session['rol'] = rol
        
        return jsonify({"status": "success", "redirect": url_for('principal.index')})
        
    return jsonify({"status": "error", "message": "Autenticación fallida con el proveedor"}), 401

@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('principal.index'))
