from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from src.infraestructura.cliente_api import api_get, api_post
from src.web.decoradores import login_requerido

blueprint = Blueprint('colaboradores', __name__, url_prefix='/colaboradores')

@blueprint.route('/dashboard')
@login_requerido
def dashboard_colaborador():
    return render_template('dashboard_tecnico.html')

@blueprint.route('/centro_suministros')
@login_requerido
def centro_suministros():
    return render_template('centro_suministros.html')

@blueprint.route('/dashboard/datos')
@login_requerido
def dashboard_datos():
    token = session.get('token')
    solicitudes = api_get(f"/solicitudes", token=token)
    return jsonify(solicitudes or [])

# Nuevos endpoints para configurar el técnico
@blueprint.route('/configuracion_guiada')
@login_requerido
def configuracion_guiada():
    return render_template('wizard_configuracion.html')

@blueprint.route('/configuracion/categorias', methods=['POST'])
@login_requerido
def guardar_categorias():
    token = session.get('token')
    colaborador_id = session.get('colaborador_id')
    categorias_ids = request.get_json().get('categorias', [])
    # Aquí iría la lógica para llamar a tu API de Finite y guardar las categorías del colaborador
    # Por ahora, simulamos el éxito
    return jsonify({"status": "ok"})

import json
import os

@blueprint.route('/configuracion/precios', methods=['POST'])
@login_requerido
def guardar_precios():
    token = session.get('token')
    colaborador_id = session.get('colaborador_id')
    precios_data = request.get_json().get('precios', [])
    
    # Ruta aislada para los precios de los técnicos
    archivo_precios_tecnico = 'tecnico_precios.json'
    
    # Cargar datos existentes o crear nuevo dict
    datos_existentes = {}
    if os.path.exists(archivo_precios_tecnico):
        with open(archivo_precios_tecnico, 'r') as f:
            try:
                datos_existentes = json.load(f)
            except:
                datos_existentes = {}
    
    # Actualizar solo para este colaborador
    datos_existentes[str(colaborador_id)] = precios_data
    
    # Guardar de forma aislada
    with open(archivo_precios_tecnico, 'w') as f:
        json.dump(datos_existentes, f, indent=4)
        
    return jsonify({"status": "ok"})

@blueprint.route('/configuracion/perfil', methods=['POST'])
@login_requerido
def guardar_perfil():
    token = session.get('token')
    colaborador_id = session.get('colaborador_id')
    datos = request.get_json()
    
    # Lógica de guardado en archivo aislado o API
    archivo_perfil = 'tecnico_perfil.json'
    datos_existentes = {}
    if os.path.exists(archivo_perfil):
        with open(archivo_perfil, 'r') as f:
            try: datos_existentes = json.load(f)
            except: datos_existentes = {}
    datos_existentes[str(colaborador_id)] = datos
    with open(archivo_perfil, 'w') as f:
        json.dump(datos_existentes, f, indent=4)
        
    return jsonify({"status": "ok"})

@blueprint.route('/configuracion/portafolio', methods=['POST'])
@login_requerido
def guardar_portafolio_wizard():
    token = session.get('token')
    colaborador_id = session.get('colaborador_id')
    datos = request.get_json()
    
    # Lógica de guardado en archivo aislado o API
    archivo_portafolio = 'tecnico_portafolio.json'
    datos_existentes = {}
    if os.path.exists(archivo_portafolio):
        with open(archivo_portafolio, 'r') as f:
            try: datos_existentes = json.load(f)
            except: datos_existentes = {}
    datos_existentes[str(colaborador_id)] = datos
    with open(archivo_portafolio, 'w') as f:
        json.dump(datos_existentes, f, indent=4)
        
    return jsonify({"status": "ok"})

@blueprint.route('/dashboard/estado/<int:id>', methods=['POST'])
@login_requerido
def dashboard_estado(id):
    token = session.get('token')
    datos = request.get_json()
    respuesta = api_post(f"/solicitudes/{id}/estado", datos, token=token)
    return jsonify({"success": respuesta is not None})

@blueprint.route('/registro/tecnico/datos', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_datos():
    if request.method == 'POST':
        session['registro_telefono_verificacion'] = request.form.get('telefono_verificacion')
        session['registro_zona_trabajo'] = request.form.get('zona_trabajo')
        session['registro_latitud'] = request.form.get('latitud')
        session['registro_longitud'] = request.form.get('longitud')
        session['registro_especialidad_resumen'] = request.form.get('especialidad_resumen')
        session['registro_medio_transporte'] = request.form.get('medio_transporte')
        session['registro_sitio_web'] = request.form.get('sitio_web')
        return redirect(url_for('colaboradores.registro_tecnico_documentos'))
    return render_template('registro_tecnico_datos.html')

@blueprint.route('/registro/tecnico/documentos', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_documentos():
    token = session.get('token')
    if request.method == 'POST':
        # 1. Crear el perfil base del colaborador
        # Nombre completo se saca de la sesión (guardado en login)
        nombre_completo = session.get('usuario_nombre', 'Usuario Okupo')
        
        # Procesar foto de perfil primero para mandarla en la creación
        import base64
        foto_perfil_b64 = None
        archivo_foto = request.files.get('foto_perfil')
        if archivo_foto and archivo_foto.filename != '':
            contenido = archivo_foto.read()
            base64_data = base64.b64encode(contenido).decode('utf-8')
            mime = archivo_foto.content_type or 'image/jpeg'
            foto_perfil_b64 = f"data:{mime};base64,{base64_data}"

        respuesta_colaborador = api_post("/colaboradores", {
            "token_usuario": token,
            "nombre_completo": nombre_completo,
            "telefono": session.get('registro_telefono_verificacion'),
            "zona_trabajo": session.get('registro_zona_trabajo'),
            "sitio_web": session.get('registro_sitio_web'),
            "foto_perfil": foto_perfil_b64,
            "medio_transporte": session.get('registro_medio_transporte'),
            "especialidad_resumen": session.get('registro_especialidad_resumen'),
            "servicios": []
        }, token=token)

        if respuesta_colaborador and respuesta_colaborador != "UNAUTHORIZED":
            try:
                colaborador_id = int(respuesta_colaborador)
            except (ValueError, TypeError):
                colaborador_id = respuesta_colaborador.get('id') if isinstance(respuesta_colaborador, dict) else None
            
            if not colaborador_id:
                return render_template('registro_tecnico_documentos.html', error="Error al crear el perfil de colaborador en el sistema.")

            session['colaborador_id'] = colaborador_id
            datos_documentacion = {}

            # Mapeo de campos del form a campos esperados por la API de Finite
            mapeo_campos = {
                'ine_frontal': 'ine_frontal', 
                'carta_policia': 'ine_trasera', # Reutilizamos ine_trasera para carta_policia por ahora en Finite
                'comprobante_domicilio': 'comprobante_domicilio', 
            }


            for campo_form, campo_api in mapeo_campos.items():
                archivo = request.files.get(campo_form)
                if archivo and archivo.filename != '':
                    contenido = archivo.read()
                    base64_data = base64.b64encode(contenido).decode('utf-8')
                    mime = archivo.content_type or 'image/jpeg'
                    datos_documentacion[campo_api] = f"data:{mime};base64,{base64_data}"
                else:
                    datos_documentacion[campo_api] = "" # Enviar vacío para evitar error de validación 400

            # Añadir foto de perfil si no se envió en el primer post (o para actualizar)
            if foto_perfil_b64:
                datos_documentacion['foto_selfie_ine'] = foto_perfil_b64 # Reutilizamos este campo para foto_perfil en Finite por ahora
            else:
                datos_documentacion['foto_selfie_ine'] = ""

            respuesta_doc = api_post(f"/colaboradores/{colaborador_id}/documentacion", datos_documentacion, token=token)
            
            if respuesta_doc is None or respuesta_doc == "UNAUTHORIZED":
                return render_template('registro_tecnico_documentos.html', error="Error al subir la documentación. Verifica que los archivos no sean demasiado pesados.")

            return redirect(url_for('colaboradores.registro_tecnico_categorias'))
        else:
            error_msg = "Error de conexión con el servidor de Finite."
            if respuesta_colaborador == "UNAUTHORIZED":
                error_msg = "Sesión no autorizada. Por favor, inicia sesión de nuevo."
            return render_template('registro_tecnico_documentos.html', error=error_msg)

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
@blueprint.route('/registro/tecnico/precios/<int:cat_index>', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_precios(cat_index=0):
    categorias_ids = session.get('categorias_seleccionadas', [])
    if not categorias_ids:
        return redirect(url_for('colaboradores.registro_tecnico_categorias'))
    
    if cat_index >= len(categorias_ids):
        return redirect(url_for('colaboradores.registro_tecnico_horarios'))
    
    cat_id = categorias_ids[cat_index]
    token = session.get('token')

    if request.method == 'POST':
        # Aquí se guardarían los precios en la sesión o se enviarían a la API
        # Por ahora, avanzamos a la siguiente categoría o al siguiente paso
        if cat_index + 1 < len(categorias_ids):
            return redirect(url_for('colaboradores.registro_tecnico_precios', cat_index=cat_index + 1))
        return redirect(url_for('colaboradores.registro_tecnico_horarios'))
    
    # Obtener info de la categoría y sus subcategorías
    categorias_todas = api_get("/categorias", token=token)
    categoria_actual = next((c for c in categorias_todas if str(c['id']) == str(cat_id)), {"nombre": "Categoría"})
    
    subcategorias = api_get(f"/categorias/{cat_id}/subcategorias", token=token)
    
    return render_template('registro_tecnico_precios.html', 
                           categoria=categoria_actual, 
                           subcategorias=subcategorias or [],
                           cat_index=cat_index,
                           total_cats=len(categorias_ids))

@blueprint.route('/registro/tecnico/horarios', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_horarios():
    return render_template('registro_tecnico_horarios.html')

@blueprint.route('/registro/tecnico/finalizar', methods=['POST'])
@login_requerido
def finalizar_registro():
    colaborador_id = session.get('colaborador_id')
    token = session.get('token')
    
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
    # Actualizar el rol en la sesión para que aparezca el dashboard inmediatamente
    session['rol'] = 'colaborador'
    
    # Limpiar datos temporales de sesión


    claves_a_limpiar = ['registro_nombre_completo', 'registro_telefono_verificacion', 'registro_zona_trabajo']
    for clave in claves_a_limpiar: session.pop(clave, None)
    return redirect(url_for('principal.index', registro_exitoso=True))


@blueprint.route('/dashboard/tecnico')
@login_requerido
def dashboard_tecnico():
    # En un entorno real, aquí buscaríamos los trabajos asignados al colaborador
    return render_template('dashboard_tecnico.html')

@blueprint.route('/portafolio')
@login_requerido
def portafolio():
    token = session.get('token')
    colaborador_id = session.get('colaborador_id')
    
    # Si no tenemos el colaborador_id en sesion, intentamos obtenerlo del perfil
    if not colaborador_id:
        # Esto es un fallback, en realidad deberia estar siempre si es colaborador
        pass

    perfil = api_get(f"/colaboradores/{colaborador_id}", token=token)
    trabajos = perfil.get('portafolio', []) if perfil and isinstance(perfil, dict) else []
    
    return render_template('portafolio.html', trabajos=trabajos)

@blueprint.route('/portafolio/agregar', methods=['POST'])
@login_requerido
def agregar_portafolio():
    token = session.get('token')
    colaborador_id = session.get('colaborador_id')
    datos = request.get_json()
    # datos: { titulo, imagen (b64), descripcion }
    respuesta = api_post(f"/colaboradores/{colaborador_id}/portafolio", datos, token=token)
    return jsonify({"success": respuesta is not None})

@blueprint.route('/evidencia/<int:solicitud_id>')
@login_requerido
def evidencia_fotografica(solicitud_id):
    return render_template('evidencia_fotografica.html', solicitud_id=solicitud_id)

@blueprint.route('/evidencia/<int:solicitud_id>/subir', methods=['POST'])
@login_requerido
def subir_evidencia(solicitud_id):
    token = session.get('token')
    datos = request.get_json()
    # datos debe tener { inicial: bool, fotos: string_base64_array }
    respuesta = api_post(f"/solicitudes/{solicitud_id}/evidencia", datos, token=token)
    return jsonify({"success": respuesta is not None})

@blueprint.route('/soporte/reportar', methods=['POST'])
@login_requerido
def reportar_soporte():
    token = session.get('token')
    datos = request.get_json()
    # datos debe tener { descripcion: string, fotos: optional_string_base64_array }
    respuesta = api_post("/soporte/reportar", datos, token=token)
    return jsonify({"success": respuesta is not None})

@blueprint.route('/trabajo/<int:solicitud_id>')
@login_requerido
def ver_trabajo(solicitud_id):
    return render_template('ver_trabajo_tecnico.html', solicitud_id=solicitud_id)

@blueprint.route('/expertos_favoritos')
@login_requerido
def expertos_favoritos():
    # Obtener lista de expertos favoritos desde la API Finite
    token = session.get('token')
    favoritos = api_get(f"/usuarios/{session['user_id']}/favoritos", token=token)
    
    if favoritos == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        
    return render_template('expertos_favoritos.html', favoritos=favoritos or [])

