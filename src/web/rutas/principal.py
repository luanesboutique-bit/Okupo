import json
import os
from flask import Blueprint, render_template, redirect, url_for, request, session
from src.infraestructura.cliente_api import api_get
from src.aplicacion.clasificador import clasificar_servicio
from src.web.decoradores import login_requerido

blueprint = Blueprint('principal', __name__)

@blueprint.route('/')
def index():
    categorias = api_get("/categorias", token=session.get('token'))
    if categorias == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada. Inicia sesión de nuevo."))
    return render_template('index.html', categorias=categorias or [])

@blueprint.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('principal.index'))
    
    categoria_id = clasificar_servicio(query)
    return redirect(url_for('principal.ver_subcategorias', categoria_id=categoria_id))

@blueprint.route('/bienvenida')
def bienvenida_seleccion_rol():
    return render_template('seleccion_rol.html')

@blueprint.route('/unete')
def landing_colaborador():
    return render_template('landing_colaborador.html')

@blueprint.route('/categorias/<int:categoria_id>/subcategorias')
def ver_subcategorias(categoria_id):
    subcategorias = api_get(f"/categorias/{categoria_id}/subcategorias", token=session.get('token'))
    if subcategorias == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
    
    # Cargar notas desde precios_config.json
    try:
        with open('precios_config.json', 'r') as f:
            precios_config = json.load(f)
    except:
        precios_config = {}

    # Inyectar nota en cada subcategoría
    for sub in subcategorias:
        sub_id = str(sub.get('id'))
        if sub_id in precios_config:
            sub['nota'] = precios_config[sub_id].get('nota')
            
    return render_template('subcategorias.html', subcategorias=subcategorias or [], categoria_id=categoria_id)

@blueprint.route('/marketplace/<int:subcategoria_id>')
def marketplace(subcategoria_id):
    latitud = request.args.get('latitud', '19.4326')
    longitud = request.args.get('longitud', '-99.1332')
    categoria_id = request.args.get('categoria_id') # Capturar categoria_id
    
    parametros = f"?latitud={latitud}&longitud={longitud}"
    colaboradores = api_get(f"/subcategorias/{subcategoria_id}/colaboradores{parametros}", token=session.get('token'))
    
    if colaboradores == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        
    return render_template('marketplace.html', 
                           colaboradores=colaboradores or [], 
                           subcategoria_id=subcategoria_id,
                           categoria_id=categoria_id) # Pasar al template

@blueprint.route('/cotizar')
def cotizar_especial():
    return render_template('cotizar_especial.html')

@blueprint.route('/politicas')
def politicas():
    return render_template('politicas.html')

@blueprint.route('/perfil')
@login_requerido
def perfil():
    token = session.get('token')
    datos_usuario = api_get(f"/usuarios/{session['user_id']}", token=token)
    
    if datos_usuario == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        
    return render_template('perfil.html', usuario=datos_usuario or {})

@blueprint.route('/direcciones')
@login_requerido
def direcciones():
    # Obtener direcciones registradas del usuario
    token = session.get('token')
    direcciones = api_get(f"/usuarios/{session['user_id']}/direcciones", token=token)
    
    if direcciones == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        
    return render_template('direcciones.html', direcciones=direcciones or [])

@blueprint.route('/direcciones/nueva', methods=['GET', 'POST'])
@login_requerido
def agregar_direccion():
    if request.method == 'POST':
        datos = {
            "alias": request.form.get('alias'),
            "calle": request.form.get('calle'),
            "numero": request.form.get('numero'),
            "colonia": request.form.get('colonia'),
            "codigo_postal": request.form.get('cp')
        }
        token = session.get('token')
        respuesta = api_post(f"/usuarios/{session['user_id']}/direcciones", datos, token=token)
        
        if respuesta:
            return redirect(url_for('principal.direcciones'))
        return render_template('agregar_direccion.html', error="No se pudo guardar la dirección.")
        
    return render_template('agregar_direccion.html')

@blueprint.route('/pagos')
@login_requerido
def pagos():
    # Obtener métodos de pago guardados del usuario
    token = session.get('token')
    metodos = api_get(f"/usuarios/{session['user_id']}/pagos", token=token)
    
    if metodos == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        
    return render_template('pagos.html', metodos=metodos or [])

@blueprint.route('/pagos/nuevo', methods=['GET', 'POST'])
@login_requerido
def agregar_pago():
    if request.method == 'POST':
        # Los datos vendrían del formulario de tarjeta (ej: integración Conekta)
        datos = {
            "token_tarjeta": request.form.get('conekta_token'),
            "tipo": request.form.get('tipo'),
            "ultimos_digitos": request.form.get('ultimos_digitos'),
            "expiracion": request.form.get('expiracion')
        }
        token = session.get('token')
        respuesta = api_post(f"/usuarios/{session['user_id']}/pagos", datos, token=token)
        
        if respuesta:
            return redirect(url_for('principal.pagos'))
        return render_template('agregar_pago.html', error="No se pudo guardar el método de pago.")
        
    return render_template('agregar_pago.html')

@blueprint.route('/facturacion')
def facturacion():
    # Obtener datos de facturación guardados del usuario
    token = session.get('token')
    datos = api_get(f"/usuarios/{session['user_id']}/facturacion", token=token)
    
    if datos == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
        
    return render_template('facturacion.html', datos=datos or {})

@blueprint.route('/soporte')
def soporte():
    return render_template('soporte.html')
