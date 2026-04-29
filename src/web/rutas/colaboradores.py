from flask import Blueprint, render_template, request, redirect, url_for, session
from src.infraestructura.cliente_api import api_get, api_post
from src.web.decoradores import login_requerido

blueprint = Blueprint('colaboradores', __name__)

@blueprint.route('/registro/tecnico/docs', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_docs():
    token = session.get('token')
    if request.method == 'POST':
        colaborador_id = session.get('colaborador_id')
        
        if not colaborador_id:
            resp = api_post("/colaboradores", {
                "token_usuario": token,
                "telefono": request.form.get('telefono'),
                "sitio_web": None,
                "servicios": []
            }, token=token)
            if resp and resp != "UNAUTHORIZED":
                colaborador_id = int(resp)
                session['colaborador_id'] = colaborador_id

        datos_docs = {
            "ine_frontal": request.form.get('ine_frontal'),
            "ine_trasera": request.form.get('ine_trasera'),
            "comprobante_domicilio": request.form.get('comprobante_domicilio'),
            "foto_selfie_ine": request.form.get('foto_selfie_ine')
        }
        api_post(f"/colaboradores/{colaborador_id}/documentacion", datos_docs, token=token)
        
        return redirect(url_for('colaboradores.registro_tecnico_categorias'))

    return render_template('registro_tecnico_docs.html')

@blueprint.route('/registro/tecnico/categorias', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_categorias():
    if request.method == 'POST':
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
        datos_precios = {
            "precio_por_kilometro": float(request.form.get('precio_km')),
            "recargo_lluvia": float(request.form.get('recargo_lluvia')),
            "recargo_domingo": float(request.form.get('recargo_domingo')),
            "recargo_nocturno": float(request.form.get('recargo_nocturno'))
        }
        api_post(f"/colaboradores/{colaborador_id}/precios-dinamicos", datos_precios, token=token)
        return redirect(url_for('colaboradores.registro_tecnico_horarios'))
        
    return render_template('registro_tecnico_precios.html')

@blueprint.route('/registro/tecnico/horarios', methods=['GET', 'POST'])
@login_requerido
def registro_tecnico_horarios():
    colaborador_id = session.get('colaborador_id')
    token = session.get('token')
    if request.method == 'POST':
        horarios = []
        for i in range(7):
            if request.form.get(f'dia_{i}_activo'):
                horarios.append({
                    "colaborador_id": colaborador_id,
                    "dia_semana": i,
                    "hora_inicio": request.form.get(f'dia_{i}_inicio'),
                    "hora_fin": request.form.get(f'dia_{i}_fin'),
                    "activo": True
                })
        api_post(f"/colaboradores/{colaborador_id}/horarios", horarios, token=token)
        return redirect(url_for('principal.index', registro_exitoso=True))

    return render_template('registro_tecnico_horarios.html')
