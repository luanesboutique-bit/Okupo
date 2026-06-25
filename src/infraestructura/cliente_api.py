import requests
from .configuracion import URL_BASE_API

def obtener_cabeceras(token=None):
    cabeceras = {'Content-Type': 'application/json'}
    if token:
        cabeceras['Authorization'] = f"Bearer {token}"
    return cabeceras

def api_get(endpoint, token=None):
    try:
        url_completa = f"{URL_BASE_API}{endpoint}"
        print(f"DEBUG: Llamando a API en: {url_completa}")
        respuesta = requests.get(url_completa, headers=obtener_cabeceras(token))
        if respuesta.status_code == 200:
            return respuesta.json()
        if respuesta.status_code == 401:
            return "UNAUTHORIZED"
        return None
    except Exception as e:
        print(f'🔥 ERROR EN API_GET: {e}')
        return None

def api_post(endpoint, datos, token=None):
    try:
        respuesta = requests.post(f"{URL_BASE_API}{endpoint}", json=datos, headers=obtener_cabeceras(token))
        if respuesta.status_code in [200, 201]:
            try:
                return respuesta.json()
            except:
                return respuesta.text.strip('"')
        print(f"❌ API POST Error {respuesta.status_code}: {respuesta.text}")
        if respuesta.status_code == 401:
            return "UNAUTHORIZED"
        return None
    except Exception as e:
        print(f"❌ API POST Exception: {e}")
        return None
