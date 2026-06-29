from flask import Flask, request, jsonify, send_from_directory, render_template, session
from flask_cors import CORS
import requests
import os
import dotenv
import json
from datetime import datetime
from src.infraestructura.configuracion import CLAVE_SECRETA, CONEKTA_PUBLIC_KEY, URL_BASE_API
from src.web.rutas.autenticacion import blueprint as blueprint_autenticacion
from src.web.rutas.principal import blueprint as blueprint_principal
from src.web.rutas.pedidos import blueprint as blueprint_pedidos
from src.web.rutas.colaboradores import blueprint as blueprint_colaboradores
from calculo_tarifas import calcular_tipo_tarifa

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

# Registro de Blueprints
app.register_blueprint(blueprint_autenticacion)
app.register_blueprint(blueprint_principal)
app.register_blueprint(blueprint_pedidos)
app.register_blueprint(blueprint_colaboradores)

@app.route('/api/precios', methods=['GET', 'POST'])
def gestionar_precios():
    archivo_precios = 'precios_config.json'
    if request.method == 'POST':
        nuevos_datos = request.get_json() 
        datos_existentes = {}
        if os.path.exists(archivo_precios):
            with open(archivo_precios, 'r') as f:
                try:
                    datos_existentes = json.load(f)
                except:
                    datos_existentes = {}
        
        datos_existentes.update(nuevos_datos)
        with open(archivo_precios, 'w') as f:
            json.dump(datos_existentes, f, indent=4)
        return jsonify({"status": "ok"})
    else:
        if not os.path.exists(archivo_precios):
            return jsonify({})
        
        # Obtener tarifa activa según horario para referencia interna
        es_urgencia_forzada = request.args.get('urgencia', 'false').lower() == 'true'
        tipo_tarifa = calcular_tipo_tarifa(es_urgencia_forzada)
        
        with open(archivo_precios, 'r') as f:
            try:
                todos_precios = json.load(f)
                # Mantener la estructura original para el frontend
                return jsonify(todos_precios)
            except:
                return jsonify({})


@app.route('/api/pedido_suministros', methods=['POST'])
def generar_pedido_suministros():
    try:
        datos = request.get_json()
        print(f"DEBUG: Datos recibidos: {datos}")
        
        # Guardar en archivo para que el admin lo lea
        archivo_pedidos = 'pedidos_suministros.json'
        pedidos = []
        if os.path.exists(archivo_pedidos):
            with open(archivo_pedidos, 'r') as f:
                try: pedidos = json.load(f)
                except: pedidos = []
        
        pedido = {
            "id": len(pedidos) + 1,
            "tecnico": session.get('nombre', 'Técnico'),
            "items": datos['items'],
            "total": datos['total'],
            "fecha": datetime.now().isoformat(),
            "estado": "pendiente"
        }
        pedidos.append(pedido)
        with open(archivo_pedidos, 'w') as f:
            json.dump(pedidos, f, indent=4)
            
        return jsonify({"status": "ok", "pedido_id": pedido['id']})
    except Exception as e:
        print(f"ERROR al generar pedido: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/suministros', methods=['GET', 'POST'])
def gestionar_suministros():
    archivo_suministros = 'suministros_config.json'
    if request.method == 'POST':
        datos = request.get_json()
        with open(archivo_suministros, 'w') as f:
            json.dump(datos, f, indent=4)
        return jsonify({"status": "ok"})
    else:
        if not os.path.exists(archivo_suministros):
            return jsonify({})
        with open(archivo_suministros, 'r') as f:
            return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
