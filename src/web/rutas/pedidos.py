from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from src.infraestructura.cliente_api import api_get, api_post
from src.web.decoradores import login_requerido
from src.aplicacion.utilidades_pago import calcular_desglose_pago
from decimal import Decimal
import json
import os
from calculo_tarifas import calcular_tipo_tarifa

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
    desglose = calcular_desglose_pago(precio_base, es_flete=es_flete, token=token)
    
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
        subcategoria = api_get(f"/subcategorias/{subcategoria_id}", token=token) or {}
        
        # Cargar precios usando ruta relativa al proyecto
        try:
            with open('precios_config.json', 'r') as f:
                precios_locales = json.load(f)
        except:
            precios_locales = {}
            
        precios = precios_locales.get(str(subcategoria_id), {})
        
        # Usar la función centralizada
        tarifa_tipo = calcular_tipo_tarifa()
        precio = precios.get(tarifa_tipo, precios.get('normal', 0))
            
        # Capturar TODOS los campos específicos por categoría
        campos_ignorar = ['subcategoria_id', 'colaborador_id', 'descripcion', 'latitud', 'longitud', 
                          'calle', 'numero', 'colonia', 'referencias', 'fecha_servicio', 'hora_servicio']
        detalles_adicionales = {k: v for k, v in request.form.items() if k not in campos_ignorar and v}
        
        datos = {
            "subcategoria_id": subcategoria_id,
            "colaborador_id": request.form.get('colaborador_id'),
            "descripcion": request.form.get('descripcion'),
            "latitud": request.form.get('latitud'),
            "longitud": request.form.get('longitud'),
            "fotos_evidencia_inicial": request.form.get('fotos_evidencia_inicial'),
            "calle": request.form.get('calle'),
            "numero": request.form.get('numero'),
            "colonia": request.form.get('colonia'),
            "referencias": request.form.get('referencias'),
            "detalles_adicionales": json.dumps(detalles_adicionales),
            "nombre_servicio": subcategoria.get('nombre', 'Servicio'),
            "tarifa_tipo": tarifa_tipo,
            "precio": precio,
            "nombre_colaborador": "Experto Asignado"
        }
        return render_template('confirmacion.html', **datos)

    colaborador_id = request.args.get('colaborador_id')
    subcategoria_id = request.args.get('subcategoria_id')
    
    # Obtener detalles de la subcategoría desde API
    subcategoria = api_get(f"/subcategorias/{subcategoria_id}", token=session.get('token')) or {}
    
    # Cargar precios usando ruta relativa
    precios_locales = {}
    try:
        with open('precios_config.json', 'r') as f:
            precios_locales = json.load(f)
    except Exception as e:
        print(f"DEBUG: Failed to load precios_config.json: {e}")
    
    key = str(subcategoria_id)
    precios = precios_locales.get(key, {})
    
    # Usar la función centralizada
    tarifa_tipo = calcular_tipo_tarifa()
    precio_activo = precios.get(tarifa_tipo, precios.get('normal', 0))
    
    print(f"DEBUG [Pedidos]: Tarifa tipo calculada: {tarifa_tipo}")
    print(f"DEBUG [Pedidos]: Precio activo seleccionado: {precio_activo}")
        
    subcategoria['precio_activo'] = float(precio_activo)
    subcategoria['tarifa_tipo'] = tarifa_tipo
    subcategoria['nota'] = precios.get('nota')
    
    print(f"DEBUG [Pedidos]: Objeto subcategoria enviado al template: {subcategoria}")
    
    return render_template('pedir.html', 
                           colaborador_id=colaborador_id, 
                           subcategoria_id=subcategoria_id,
                           subcategoria=subcategoria)


@blueprint.route('/carrito/agregar', methods=['POST'])
@login_requerido
def agregar_al_carrito():
    datos = request.get_json()
    if 'carrito' not in session:
        session['carrito'] = []
    
    carrito = session['carrito']
    
    # Validar que todos los items sean de la misma categoría
    if carrito:
        if carrito[0].get('categoria_id') != datos.get('categoria_id'):
            return jsonify({"status": "error", "message": "Solo puedes agrupar servicios de la misma categoría."}), 400
    
    carrito.append(datos)
    session['carrito'] = carrito
    return jsonify({"status": "success", "carrito_count": len(carrito)})

@blueprint.route('/carrito/eliminar', methods=['POST'])
@login_requerido
def eliminar_del_carrito():
    datos = request.get_json()
    index = datos.get('index')
    carrito = session.get('carrito', [])
    if 0 <= index < len(carrito):
        carrito.pop(index)
        session['carrito'] = carrito
    return jsonify({"status": "success"})

@blueprint.route('/carrito/resumen', methods=['GET'])
@login_requerido
def resumen_carrito():
    carrito = session.get('carrito', [])
    if not carrito:
        return jsonify({"mensaje": "Carrito vacío", "total": 0})
        
    # Agrupar por categoría
    categorias = {}
    for item in carrito:
        cat_id = item.get('categoria_id')
        if cat_id not in categorias:
            categorias[cat_id] = []
        categorias[cat_id].append(item)
    
    total_final = 0
    desglose = []
    
    # Aplicar regla: 100% precio más alto, 80% precio resto
    for cat_id, items in categorias.items():
        items_ordenados = sorted(items, key=lambda x: x['precio'], reverse=True)
        
        for i, item in enumerate(items_ordenados):
            precio_a_cobrar = item['precio']
            if i > 0: # Descuento del 20% a partir del segundo
                precio_a_cobrar = item['precio'] * 0.8
            
            total_final += precio_a_cobrar
            desglose.append({**item, "precio_cobrado": precio_a_cobrar})
            
    return jsonify({
        "desglose": desglose,
        "total_final": total_final,
        "ahorro_total": sum(i['precio'] for i in carrito) - total_final
    })

@blueprint.route('/confirmar_paquete', methods=['GET'])
@login_requerido
def confirmar_paquete_form():
    return render_template('confirmacion_paquete.html')

@blueprint.route('/confirmar_paquete', methods=['POST'])
@login_requerido
def confirmar_paquete_submit():
    carrito = session.get('carrito', [])
    token = session.get('token')
    descripcion = request.form.get('descripcion')
    direccion = request.form.get('direccion')
    referencias = request.form.get('referencias')

    # Enviar cada servicio como solicitud individual (o agrupar si la API lo permite)
    for item in carrito:
        datos_solicitud = {
            "usuario_id": session['user_id'],
            "subcategoria_id": item['id'],
            "descripcion_detallada": f"{descripcion} - Paquete: {item['nombre']}",
            "calle": direccion,
            "detalles_adicionales": json.dumps({"referencias": referencias})
        }
        api_post("/solicitudes", datos_solicitud, token=token)

    session.pop('carrito', None) # Limpiar carrito
    return redirect(url_for('pedidos.confirmacion_pedido'))

@blueprint.route('/confirmacion_pedido', methods=['GET'])
@login_requerido
def confirmacion_pedido():
    return render_template('confirmacion_pedido.html')

@blueprint.route('/resumen_paquete', methods=['GET'])
@login_requerido
def resumen_paquete():
    return render_template('resumen_paquete.html')

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

@blueprint.route('/chat')
@login_requerido
def listar_chats():
    token = session.get('token')
    solicitudes = api_get(f"/solicitudes?usuario_id={session['user_id']}", token=token)
    
    if solicitudes == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        
    return render_template('lista_chats.html', solicitudes=solicitudes or [])

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
    return render_template('esperando_ofertas.html')

@blueprint.route('/visita/aviso')
@login_requerido
def aviso_visita():
    return render_template('aviso_visita.html')

@blueprint.route('/pagar/<int:solicitud_id>')
@login_requerido
def iniciar_pago(solicitud_id):
    token = session.get('token')
    solicitud = api_get(f"/solicitudes?usuario_id={session['user_id']}", token=token)
    pedido = next((s for s in (solicitud or []) if s['id'] == solicitud_id), None)
    
    if not pedido:
        return "Pedido no encontrado", 404
        
    return render_template('pago.html', pedido=pedido)

@blueprint.route('/pagar/finalizar', methods=['POST'])
@login_requerido
def finalizar_pago():
    return "OK"

@blueprint.route('/urgencia_final')
@login_requerido
def mostrar_urgencia_final():
    return render_template('urgencia_final.html')

@blueprint.route('/historial_pagos')
@login_requerido
def historial_pagos():
    pagos = api_get(f"/pagos?usuario_id={session['user_id']}", token=session.get('token'))
    if pagos == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
    return render_template('historial_pagos.html', pagos=pagos or [])


@blueprint.route('/solicitar_urgencia_final', methods=['POST'])
@login_requerido
def finalizar_urgencia():
    datos_solicitud = {
        "usuario_id": session['user_id'],
        "colaborador_id": 1,
        "subcategoria_id": 9,
        "urgencia": "media",
        "descripcion_detallada": request.form.get('descripcion'),
        "fotos_evidencia_inicial": None,
        "latitud": 20.6736,
        "longitud": -103.3444,
        "calle": request.form.get('direccion', 'Ubicación GPS'),
        "detalles_adicionales": json.dumps({"referencias": request.form.get('referencias'), "urgencia_247": True})
    }
    
    respuesta = api_post("/solicitudes", datos_solicitud, token=session.get('token'))
    
    if respuesta and isinstance(respuesta, dict) and 'id' in respuesta:
        return redirect(url_for('pedidos.iniciar_pago', solicitud_id=respuesta['id']))
    
    return "Error al enviar la emergencia", 500
