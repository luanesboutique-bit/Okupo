from flask import Flask, send_from_directory
from src.infraestructura.configuracion import CLAVE_SECRETA
from src.web.rutas.autenticacion import blueprint as blueprint_autenticacion
from src.web.rutas.principal import blueprint as blueprint_principal
from src.web.rutas.pedidos import blueprint as blueprint_pedidos
from src.web.rutas.colaboradores import blueprint as blueprint_colaboradores

app = Flask(__name__)
app.secret_key = CLAVE_SECRETA

# Registro de Blueprints
app.register_blueprint(blueprint_autenticacion)
app.register_blueprint(blueprint_principal)
app.register_blueprint(blueprint_pedidos)
app.register_blueprint(blueprint_colaboradores)

@app.route('/favicon.ico')
def favicon():
    return "", 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
