from flask import Blueprint, render_template, request, redirect, url_for, session
from src.infraestructura.cliente_api import api_get, api_post
from src.web.decoradores import login_requerido

blueprint = Blueprint('pedidos', __name__)

@blueprint.route('/pedir', methods=['GET', 'POST'])
@login_requerido
def pedir():
    if request.method == 'POST':
        subcat_id = request.form.get('subcategoria_id')
        token = session.get('token')
        
        # Obtener detalles de la subcategoría para el resumen
        subcategoria = api_get(f"/subcategorias/{subcat_id}", token=token)
        
        # Simular cálculo de tarifa (en producción vendría de la API o lógica compartida)
        import datetime
        ahora = datetime.datetime.now()
        tarifa_tipo = "Normal"
        precio = subcategoria.get('precio_normal', 0) if subcategoria else 0
        
        if ahora.hour >= 20 or ahora.hour < 6:
            tarifa_tipo = "Noche"
            precio = subcategoria.get('precio_noche', precio)
        if ahora.weekday() == 6: # Domingo
            tarifa_tipo = "Urgente"
            precio = subcategoria.get('precio_urgente', precio)
            
        datos = {
            "subcat_id": subcat_id,
            "colaborador_id": request.form.get('colaborador_id'),
            "descripcion": request.form.get('descripcion'),
            "latitud": request.form.get('latitud'),
            "longitud": request.form.get('longitud'),
            "nombre_servicio": subcategoria.get('nombre', 'Servicio') if subcategoria else "Servicio",
            "tarifa_tipo": tarifa_tipo,
            "precio": precio,
            "nombre_colaborador": "Experto Asignado" # Placeholder o buscar si colaborador_id != None
        }
        return render_template('confirmacion.html', **datos)

    colaborador_id = request.args.get('colaborador_id')
    subcat_id = request.args.get('subcategoria_id')
    return render_template('pedir.html', colaborador_id=colaborador_id, subcat_id=subcat_id)

@blueprint.route('/confirmar/finalizar', methods=['POST'])
@login_requerido
def finalizar_pedido():
    token = session.get('token')
    
    # Obtener valores del formulario con fallbacks seguros para evitar ValueError
    subcat_id_raw = request.form.get('subcat_id')
    colab_id_raw = request.form.get('colaborador_id')
    
    # Convertir a int solo si el valor existe y no es la cadena 'None'
    try:
        subcat_id = int(subcat_id_raw) if subcat_id_raw and subcat_id_raw != 'None' else 1
    except (ValueError, TypeError):
        subcat_id = 1

    try:
        colab_id = int(colab_id_raw) if colab_id_raw and colab_id_raw != 'None' else 1
    except (ValueError, TypeError):
        colab_id = 1

    datos_solicitud = {
        "usuario_id": session['user_id'],
        "colaborador_id": colab_id,
        "subcategoria_id": subcat_id,
        "urgencia": "media",
        "descripcion_detallada": request.form.get('descripcion', 'Sin descripción'),
        "fotos_evidencia_inicial": "placeholder.jpg",
        "latitud": float(request.form.get('latitud', 19.4326)),
        "longitud": float(request.form.get('longitud', -99.1332))
    }
    
    respuesta = api_post("/solicitudes", datos_solicitud, token=token)
    
    if respuesta == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
    
    if respuesta:
        return redirect(url_for('pedidos.mostrar_asignacion'))
        
    return "Error al procesar la solicitud", 500

@blueprint.route('/asignacion')
@login_requerido
def mostrar_asignacion():
    return render_template('asignacion.html')

@blueprint.route('/mis_pedidos')
@login_requerido
def mis_pedidos():
    solicitudes = api_get(f"/solicitudes?usuario_id={session['user_id']}", token=session.get('token'))
    if solicitudes == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
    return render_template('mis_pedidos.html', solicitudes=solicitudes or [])

@blueprint.route('/chat/<int:solicitud_id>', methods=['GET', 'POST'])
@login_requerido
def chat(solicitud_id):
    if request.method == 'POST':
        contenido = request.form.get('texto')
        api_post(f"/solicitudes/{solicitud_id}/mensajes", {
            "emisor_id": session['user_id'],
            "contenido": contenido
        }, token=session.get('token'))
        return redirect(url_for('pedidos.chat', solicitud_id=solicitud_id))
    
    mensajes = api_get(f"/solicitudes/{solicitud_id}/mensajes", token=session.get('token'))
    if mensajes == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
    return render_template('chat.html', mensajes=mensajes or [], solicitud_id=solicitud_id)

@blueprint.route('/cotizacion/enviar', methods=['POST'])
@login_requerido
def enviar_cotizacion():
    # En un entorno real, enviaríamos esto a la API Finite
    datos = {
        "descripcion": request.form.get('descripcion_trabajo'),
        "presupuesto": request.form.get('presupuesto_estimado'),
        "fecha": request.form.get('fecha_servicio'),
        "hora": request.form.get('hora_servicio')
    }
    # Por ahora simulamos el éxito y mostramos la pantalla de espera
    return render_template('esperando_ofertas.html', **datos)

@blueprint.route('/visita/aviso')
@login_requerido
def aviso_visita():
    return render_template('aviso_visita.html')

@blueprint.route('/visita/agendar')
@login_requerido
def agendar_visita():
    return render_template('agenda_visita.html')
