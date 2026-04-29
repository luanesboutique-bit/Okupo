import base64
import json

def obtener_usuario_id_de_token(token):
    try:
        partes = token.split('.')
        if len(partes) < 2: return None
        carga_util_b64 = partes[1]
        relleno_faltante = len(carga_util_b64) % 4
        if relleno_faltante: carga_util_b64 += '=' * (4 - relleno_faltante)
        datos_carga_util = base64.b64decode(carga_util_b64).decode('utf-8')
        return json.loads(datos_carga_util).get('sub')
    except Exception:
        return None
