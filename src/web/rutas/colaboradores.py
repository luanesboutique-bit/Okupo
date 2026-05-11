from flask import Blueprint, render_template, request, redirect, url_for, session
from src.infraestructura.cliente_api import api_get, api_post
from src.web.decoradores import login_requerido

blueprint = Blueprint('colaboradores', __name__)

@blueprint.route('/registro/tecnico/datos', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_datos():
    if request.method == 'POST':
        # Guardamos datos en sesión temporalmente
        session['registro_nombre_completo'] = request.form.get('nombre_completo')
        session['registro_telefono_verificacion'] = request.form.get('telefono_verificacion')
        session['registro_correo_electronico'] = request.form.get('correo_electronico')
        session['registro_zona_trabajo'] = request.form.get('zona_trabajo')
        return redirect(url_for('colaboradores.registro_tecnico_documentos'))
    
    return render_template('registro_tecnico_datos.html')

@blueprint.route('/registro/tecnico/documentos', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_documentos():
    token = session.get('token')
    if request.method == 'POST':
        # Crear la entrada del colaborador en el motor Finite
        respuesta_colaborador = api_post("/colaboradores", {
            "token_usuario": token,
            "telefono": session.get('registro_telefono_verificacion'),
            "zona_trabajo": session.get('registro_zona_trabajo'),
            "servicios": []
        }, token=token)

        if respuesta_colaborador and respuesta_colaborador != "UNAUTHORIZED":
            try:
                colaborador_id = int(respuesta_colaborador)
            except (ValueError, TypeError):
                # Si la respuesta es un objeto JSON con el ID
                colaborador_id = respuesta_colaborador.get('id') if isinstance(respuesta_colaborador, dict) else None
            
            if not colaborador_id:
                return render_template('registro_tecnico_documentos.html', error="Error al crear el perfil de colaborador.")

            session['colaborador_id'] = colaborador_id

            # Procesar archivos y convertirlos a base64 (o enviarlos como multipart si la API lo soporta)
            import base64
            
            datos_documentacion = {}
            campos_archivos = [
                'identificacion_frontal', 
                'identificacion_trasera', 
                'comprobante_domicilio', 
                'foto_perfil_identificacion'
            ]

            for campo in campos_archivos:
                archivo = request.files.get(campo)
                if archivo and archivo.filename != '':
                    contenido = archivo.read()
                    base64_data = base64.b64encode(contenido).decode('utf-8')
                    # Formato data:image/...;base64,...
                    mime = archivo.content_type or 'image/jpeg'
                    datos_documentacion[campo] = f"data:{mime};base64,{base64_data}"
                else:
                    # Fallback si se envió como string (por si acaso hay algún JS de por medio)
                    datos_documentacion[campo] = request.form.get(campo)

            api_post(f"/colaboradores/{colaborador_id}/documentacion", datos_documentacion, token=token)
            
            return redirect(url_for('colaboradores.registro_tecnico_categorias'))

    return render_template('registro_tecnico_documentos.html')

@blueprint.route('/registro/tecnico/categorias', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_categorias():
    if request.method == 'POST':
        session['categorias_seleccionadas'] = request.form.getlist('categorias_seleccionadas')
        return redirect(url_for('colaboradores.registro_tecnico_precios'))
    
    categorias = api_get("/categorias", token=session.get('token'))
    if categorias == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
    return render_template('registro_tecnico_categorias.html', categorias=categorias or [])

@blueprint.route('/registro/tecnico/precios', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_precios():
    colaborador_id = session.get('colaborador_id')
    token = session.get('token')
    if request.method == 'POST':
        # Aquí se procesarían los precios por cada categoría
        # Por ahora redirigimos al último paso
        return redirect(url_for('colaboradores.registro_tecnico_horarios'))
        
    return render_template('registro_tecnico_precios.html')

@blueprint.route('/registro/tecnico/horarios', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_horarios():
    return render_template('registro_tecnico_horarios.html')

@blueprint.route('/registro/tecnico/finalizar', methods=['POST'])
@login_requerido
def finalizar_registro():
    colaborador_id = session.get('colaborador_id')
    token = session.get('token')
    
    # Procesar horarios del formulario
    lista_horarios = []
    for i in range(7):
        if request.form.get(f'dia_{i}_activo'):
            lista_horarios.append({
                "colaborador_id": colaborador_id,
                "dia_semana": i,
                "hora_inicio": request.form.get(f'dia_{i}_inicio'),
                "hora_fin": request.form.get(f'dia_{i}_fin'),
                "activo": True
            })
    
    api_post(f"/colaboradores/{colaborador_id}/horarios", lista_horarios, token=token)
    
    # Limpiar datos temporales de sesión
    claves_a_limpiar = ['registro_nombre_completo', 'registro_telefono_verificacion', 'registro_zona_trabajo']
    for clave in claves_a_limpiar: session.pop(clave, None)

    return redirect(url_for('principal.index', registro_exitoso=True))

@blueprint.route('/dashboard')
@login_requerido
def dashboard():
    return render_template('dashboard_colaborador.html')

@blueprint.route('/dashboard/tecnico')
@login_requerido
def dashboard_tecnico():
    # En un entorno real, aquí buscaríamos los trabajos asignados al colaborador
    return render_template('dashboard_tecnico.html')

@blueprint.route('/evidencia/<int:solicitud_id>')
@login_requerido
def evidencia_fotografica(solicitud_id):
    return render_template('evidencia_fotografica.html', solicitud_id=solicitud_id)

@blueprint.route('/trabajo/<int:solicitud_id>')
@login_requerido
def ver_trabajo(solicitud_id):
    # Simula la vista de un trabajo para cotizar (Oferta económica)
    return render_template('ver_trabajo_tecnico.html', solicitud_id=solicitud_id)

@blueprint.route('/trabajo/<int:solicitud_id>/detalle')
@login_requerido
def detalle_trabajo(solicitud_id):
    # Vista detallada del trabajo con botones de Aceptar/Visita
    return render_template('detalle_trabajo_tecnico.html', solicitud_id=solicitud_id)
