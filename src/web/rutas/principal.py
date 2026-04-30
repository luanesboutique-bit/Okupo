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
    colores_cat = {1: "#C69B6F", 2: "#9E8B71", 3: "#ADA391", 4: "#C6B79F"}
    acento = colores_cat.get(categoria_id, "#C69B6F")
    return render_template('subcategorias.html', subcategorias=subcategorias or [], cat_id=categoria_id, acento=acento)

@blueprint.route('/marketplace/<int:subcategoria_id>')
def marketplace(subcategoria_id):
    params = "?latitud=19.4326&longitud=-99.1332"
    colaboradores = api_get(f"/subcategorias/{subcategoria_id}/colaboradores{params}", token=session.get('token'))
    if colaboradores == "UNAUTHORIZED":
        return redirect(url_for('autenticacion.login', mensaje="Sesión expirada."))
    return render_template('marketplace.html', colaboradores=colaboradores or [], subcat_id=subcategoria_id)
