from flask import Blueprint, render_template, request, redirect, url_for, session
from src.infraestructura.cliente_api import api_get, api_post
from src.web.decoradores import login_requerido

blueprint = Blueprint('pedidos', __name__)

@blueprint.route('/pedir', methods=['GET', 'POST'])
@login_requerido
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
        respuesta = api_post("/solicitudes", datos_solicitud, token=session.get('token'))
        if respuesta == "UNAUTHORIZED":
             return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        if respuesta:
            return redirect(url_for('pedidos.mis_pedidos'))
        return "Error al crear la solicitud", 500

    colaborador_id = request.args.get('colaborador_id')
    subcat_id = request.args.get('subcategoria_id')
    return render_template('pedir.html', colaborador_id=colaborador_id, subcat_id=subcat_id)

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
