from flask import Blueprint, render_template, redirect, url_for, request, session
from src.infraestructura.cliente_api import api_get

blueprint = Blueprint('principal', __name__)

@blueprint.route('/')
def index():
    categorias = api_get("/categorias", token=session.get('token'))
    if categorias == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada. Inicia sesión de nuevo."))
    return render_template('index.html', categorias=categorias or [])

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
def perfil():
    return f"<h1>Perfil de {session.get('nombre', 'Usuario')}</h1><p>Rol: {session.get('rol')}</p><a href='/'>Volver</a>"

@blueprint.route('/soporte')
def soporte():
    return render_template('soporte.html')
