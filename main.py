from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import requests
import os
import dotenv
from src.infraestructura.configuracion import CLAVE_SECRETA, CONEKTA_PUBLIC_KEY, URL_BASE_API
from src.web.rutas.autenticacion import blueprint as blueprint_autenticacion
from src.web.rutas.principal import blueprint as blueprint_principal
from src.web.rutas.pedidos import blueprint as blueprint_pedidos
from src.web.rutas.colaboradores import blueprint as blueprint_colaboradores

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = CLAVE_SECRETA
app.config['VITE_CONEKTA_PUBLIC_KEY'] = CONEKTA_PUBLIC_KEY

@app.route('/documentos-legales')
def documentos_legales():
    return render_template('documentos_legales.html')

# Ruta para servir los documentos legales
@app.route('/docs/<path:filename>')
def serve_docs(filename):
    # Ruta donde están tus archivos HTML integrados
    return send_from_directory('C:/Users/blanc/documentos_legales_extraidos', filename)

@app.route('/api_proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(path):
    url = f"{URL_BASE_API}/{path}"
    headers = {k: v for k, v in request.headers if k.lower() != 'host'}
    
    if request.method == 'GET':
        resp = requests.get(url, params=request.args, headers=headers)
    elif request.method == 'POST':
        if request.files:
            resp = requests.post(url, files=request.files, headers=headers)
        else:
            resp = requests.post(url, json=request.get_json(), headers=headers)
    else:
        resp = requests.request(request.method, url, json=request.get_json(), headers=headers)
        
    return (resp.content, resp.status_code, resp.headers.items())

import json

# ... (resto de los imports)

# Registro de Blueprints
app.register_blueprint(blueprint_autenticacion)
app.register_blueprint(blueprint_principal)
app.register_blueprint(blueprint_pedidos)
app.register_blueprint(blueprint_colaboradores)

@app.route('/api/precios', methods=['GET', 'POST'])
def gestionar_precios():
    archivo_precios = 'precios_config.json'
    if request.method == 'POST':
        nuevos_datos = request.get_json() # Esperamos formato { "id": { normal, medio, urgente } }
        
        # Cargar datos existentes si existen
        datos_existentes = {}
        if os.path.exists(archivo_precios):
            with open(archivo_precios, 'r') as f:
                try:
                    datos_existentes = json.load(f)
                except:
                    datos_existentes = {}
        
        # Actualizar con los nuevos datos
        datos_existentes.update(nuevos_datos)
        
        # Guardar archivo completo
        with open(archivo_precios, 'w') as f:
            json.dump(datos_existentes, f, indent=4)
        return jsonify({"status": "ok"})
    else:
        if not os.path.exists(archivo_precios):
            return jsonify({})
        with open(archivo_precios, 'r') as f:
            try:
                return jsonify(json.load(f))
            except:
                return jsonify({})



@app.route('/favicon.ico')
def favicon():
    return "", 204

if __name__ == '__main__':
    app.run(debug=True, port=3000)
