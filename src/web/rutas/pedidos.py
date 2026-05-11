from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from src.infraestructura.cliente_api import api_get, api_post
from src.web.decoradores import login_requerido
from src.aplicacion.utilidades_pago import calcular_desglose_pago
from decimal import Decimal
import json

blueprint = Blueprint('pedidos', __name__)

@blueprint.route('/solicitar_clic', methods=['POST'])
@login_requerido
def solicitar_clic():
    """
    Crea una solicitud directa (Okupo Clic) desde el index.
    Aplica las reglas financieras de D'Mayoral automáticamente.
    """
    token = session.get('token')
    datos_post = request.get_json()
    
    servicio_nombre = datos_post.get('servicio_nombre', 'Servicio General')
    subcategoria_id = datos_post.get('subcategoria_id', 1)
    latitud = datos_post.get('latitud', 20.6736)
    longitud = datos_post.get('longitud', -103.3444)
    
    # Precio base para "Okupo Clic" (ejemplo: 450 MXN)
    precio_base = 450 
    es_flete = "FLETES" in servicio_nombre.upper()
    
    # Calcular desglose financiero según reglas de D'Mayoral
    desglose = calcular_desglose_pago(precio_base, es_flete=es_flete)
    
    # Buscar colaboradores para esta subcategoría
    colaboradores = api_get(f"/subcategorias/{subcategoria_id}/colaboradores?latitud={latitud}&longitud={longitud}", token=token)
    
    colaborador_id = 1 # Fallback
    if colaboradores and isinstance(colaboradores, list) and len(colaboradores) > 0:
        colaborador_id = colaboradores[0].get('colaborador_id', 1)
    
    datos_solicitud = {
        "usuario_id": session['user_id'],
        "colaborador_id": colaborador_id,
        "subcategoria_id": subcategoria_id,
        "urgencia": "alta", # Clic es por definición urgente
        "descripcion_detallada": f"Solicitud directa desde Okupo Clic para: {servicio_nombre}",
        "fotos_evidencia_inicial": None,
        "latitud": float(latitud),
        "longitud": float(longitud),
        "detalles_adicionales": json.dumps({
            "tipo_flujo": "okupo_clic",
            "desglose_financiero": desglose,
            "version_reglas": "v1_mayoral"
        })
    }
    
    respuesta = api_post("/solicitudes", datos_solicitud, token=token)
    
    if respuesta:
        return jsonify({"status": "success", "solicitud_id": respuesta.get('id')})
    
    return jsonify({"status": "error", "message": "No se pudo crear la solicitud"}), 500

@blueprint.route('/pedir', methods=['GET', 'POST'])
@login_requerido
def pedir():
    if request.method == 'POST':
        subcategoria_id = request.form.get('subcategoria_id')
        token = session.get('token')
        
        # Obtener detalles de la subcategoría para el resumen
        subcategoria = api_get(f"/subcategorias/{subcategoria_id}", token=token)
        
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
            
        # Capturar TODOS los campos específicos por categoría
        campos_ignorar = ['subcategoria_id', 'colaborador_id', 'descripcion', 'latitud', 'longitud', 
                          'calle', 'numero', 'colonia', 'referencias', 'fecha_servicio', 'hora_servicio']
        detalles_adicionales = {k: v for k, v in request.form.items() if k not in campos_ignorar and v}
        
        import json
        datos = {
            "subcategoria_id": subcategoria_id,
            "colaborador_id": request.form.get('colaborador_id'),
            "descripcion": request.form.get('descripcion'),
            "latitud": request.form.get('latitud'),
            "longitud": request.form.get('longitud'),
            "calle": request.form.get('calle'),
            "numero": request.form.get('numero'),
            "colonia": request.form.get('colonia'),
            "referencias": request.form.get('referencias'),
            "detalles_adicionales": json.dumps(detalles_adicionales),
            "nombre_servicio": subcategoria.get('nombre', 'Servicio') if subcategoria else "Servicio",
            "tarifa_tipo": tarifa_tipo,
            "precio": precio,
            "nombre_colaborador": "Experto Asignado"
        }
        return render_template('confirmacion.html', **datos)

    colaborador_id = request.args.get('colaborador_id')
    subcategoria_id = request.args.get('subcategoria_id')
    
    # Obtener detalles de la subcategoría para el resumen de pago inicial
    subcategoria = api_get(f"/subcategorias/{subcategoria_id}", token=session.get('token'))
    
    return render_template('pedir.html', 
                           colaborador_id=colaborador_id, 
                           subcategoria_id=subcategoria_id,
                           subcategoria=subcategoria or {})

@blueprint.route('/confirmar/finalizar', methods=['POST'])
@login_requerido
def finalizar_pedido():
    print("DEBUG: Entered finalizar_pedido route")
    try:
        token = session.get('token')
        print(f"DEBUG: Form data: {request.form.to_dict()}")
        
        def safe_int(valor, default=1):
            if not valor or valor == 'None': return default
            try: return int(valor)
            except (ValueError, TypeError): return default

        subcategoria_id = safe_int(request.form.get('subcategoria_id'))
        colaborador_id = safe_int(request.form.get('colaborador_id'))
        
        precio_raw = request.form.get('precio', '450')
        print(f"DEBUG: Precio raw: {precio_raw}")
        precio_total = Decimal(str(precio_raw))
        
        es_flete = "FLETES" in request.form.get('nombre_servicio', '').upper()
        metodo_pago = request.form.get('metodo_pago', 'tarjeta')
        
        desglose = calcular_desglose_pago(precio_total, metodo_pago=metodo_pago, es_flete=es_flete)
        print(f"DEBUG: Desglose: {desglose}")
        
        detalles_adicionales = {}
        try:
            raw = request.form.get('detalles_adicionales', '{}')
            detalles_adicionales = json.loads(raw)
        except:
            pass
            
        detalles_adicionales['desglose_financiero'] = desglose
        detalles_adicionales['metodo_pago'] = metodo_pago
        detalles_adicionales['version_reglas'] = 'v2_mayoral_conekta'

        datos_solicitud = {
            "usuario_id": session['user_id'],
            "colaborador_id": colaborador_id,
            "subcategoria_id": subcategoria_id,
            "urgencia": "media",
            "descripcion_detallada": request.form.get('descripcion', 'Sin descripción'),
            "fotos_evidencia_inicial": "placeholder.jpg",
            "latitud": float(request.form.get('latitud', 19.4326)),
            "longitud": float(request.form.get('longitud', -99.1332)),
            "calle": request.form.get('calle'),
            "numero": request.form.get('numero'),
            "colonia": request.form.get('colonia'),
            "referencias": request.form.get('referencias'),
            "detalles_adicionales": json.dumps(detalles_adicionales)
        }
        
        print(f"DEBUG: Payload final: {datos_solicitud}")
        
        respuesta = api_post("/solicitudes", datos_solicitud, token=token)
        
        print(f"DEBUG: API POST response: {respuesta}")
        if respuesta == "UNAUTHORIZED":
            return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        
        if respuesta:
            return redirect(url_for('pedidos.mostrar_asignacion'))
            
        current_app.logger.error(f"❌ API POST failed. Response: {respuesta}")
        return f"Error al procesar la solicitud. API returned: {respuesta}", 500
    except Exception as e:
        print(f"❌ CRITICAL ERROR in finalizar_pedido: {e}")
        return f"Error crítico: {str(e)}", 500

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
    
    import json
    if solicitudes:
        for sol in solicitudes:
            if sol.get('detalles_adicionales'):
                try:
                    sol['campos_extra'] = json.loads(sol['detalles_adicionales'])
                except:
                    sol['campos_extra'] = {}
            else:
                sol['campos_extra'] = {}
                
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
