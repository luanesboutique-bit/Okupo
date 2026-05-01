import requests
from .configuracion import URL_BASE_API, MODO_MOCK

def obtener_cabeceras(token=None):
    cabeceras = {'Content-Type': 'application/json'}
    if token:
        cabeceras['Authorization'] = f"Bearer {token}"
    return cabeceras

def obtener_mock(endpoint, metodo="GET", datos=None):
    """Devuelve datos simulados para el desarrollo del Front-end."""
    print(f"🛠️ MOCK: {metodo} {endpoint}")
    
    if "/login" in endpoint:
        return {"token": "mock.eyJzdWIiOiIxIn0.token"} # Simula usuario_id = 1
    
    if "/categorias" in endpoint and "subcategorias" not in endpoint:
        return [
            {"id": 1, "nombre": "Cerrajería", "icono": "key"},
            {"id": 2, "nombre": "Plomería", "icono": "faucet"},
            {"id": 3, "nombre": "Electricidad", "icono": "bolt"},
            {"id": 4, "nombre": "Limpieza", "icono": "spray-can-sparkles"},
            {"id": 5, "nombre": "Muebles", "icono": "couch"},
            {"id": 8, "nombre": "Albañilería", "icono": "hard-hat"}
        ]
        
    if "/subcategorias" in endpoint:
        lista = [
            {"id": 1, "nombre": "Chapa de Pomo", "precio_normal": 720, "precio_noche": 1080, "precio_urgente": 1450},
            {"id": 2, "nombre": "Apertura de Puerta", "precio_normal": 870, "precio_noche": 1370, "precio_urgente": 2170}
        ]
        # Si el endpoint termina en un número, es una búsqueda por ID
        partes = endpoint.split('/')
        ultimo = partes[-1]
        if ultimo.isdigit():
            id_buscado = int(ultimo)
            for item in lista:
                if item['id'] == id_buscado:
                    return item
            return lista[0] # Fallback
        return lista
    
    return {}

def api_get(endpoint, token=None):
    if MODO_MOCK:
        return obtener_mock(endpoint, "GET")
    try:
        respuesta = requests.get(f"{URL_BASE_API}{endpoint}", headers=obtener_cabeceras(token))
        if respuesta.status_code == 200:
            return respuesta.json()
        if respuesta.status_code == 401:
            return "UNAUTHORIZED"
        return None
    except Exception:
        return None

def api_post(endpoint, datos, token=None):
    if MODO_MOCK:
        return obtener_mock(endpoint, "POST", datos)
    try:
        respuesta = requests.post(f"{URL_BASE_API}{endpoint}", json=datos, headers=obtener_cabeceras(token))
        if respuesta.status_code in [200, 201]:
            try:
                return respuesta.json()
            except:
                return respuesta.text.strip('"')
        if respuesta.status_code == 401:
            return "UNAUTHORIZED"
        return None
    except Exception:
        return None
