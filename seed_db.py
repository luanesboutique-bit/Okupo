import requests
import json
import time

API_URL = "http://localhost:3000"

def post(endpoint, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.post(f"{API_URL}{endpoint}", json=data, headers=headers)
        if r.status_code in [200, 201]:
            print(f"✅ OK: {endpoint}")
            return r.json() if r.text else True
        else:
            print(f"❌ Error {r.status_code} en {endpoint}: {r.text}")
            return None
    except Exception as e:
        print(f"🔥 Error conectando a {endpoint}: {e}")
        return None

def get_token(correo, contrasenna):
    res = post("/login", {"correo": correo, "contrasenna": contrasenna})
    return res if isinstance(res, str) else None

def seed():
    print("🚀 Iniciando poblado exhaustivo de base de datos...")

    # 1. Categorías y Subcategorías (Ya inicializadas por el motor)
    # categorias = [
    #     {"nombre": "Cerrajería", "icono": "fas fa-key", "subs": ["Apertura de Puerta", "Cambio de Chapa", "Cerrajería Automotriz"]},
    #     {"nombre": "Plomería", "icono": "fas fa-faucet", "subs": ["Fuga de Agua", "Destape de Drenaje", "Instalación de Tinaco"]},
    #     {"nombre": "Electricidad", "icono": "fas fa-bolt", "subs": ["Cortocircuito", "Instalación de Lámpara", "Tablero Eléctrico"]},
    #     {"nombre": "Pintura", "icono": "fas fa-paint-roller", "subs": ["Pintura Interior", "Pintura Exterior", "Impermeabilización"]},
    #     {"nombre": "Albannilería", "icono": "fas fa-hammer", "subs": ["Pegado de Piso", "Reparación de Muro", "Resane de Grietas"]}
    # ]

    # for i, cat in enumerate(categorias, 1):
    #     post("/categorias", {"nombre": cat["nombre"], "icono": cat["icono"]})
    #     for sub_name in cat["subs"]:
    #         post(f"/categorias/{i}/subcategorias", {"nombre": sub_name})

    # 2. Usuarios base
    usuarios = [
        {"nombre": "Ivan Cliente", "correo": "ivan@okupo.com", "contrasenna": "123456"},
        {"nombre": "Admin Okupo", "correo": "admin@okupo.com", "contrasenna": "admin123"},
        {"nombre": "Juan Cerrajería", "correo": "juan@cerrajero.com", "contrasenna": "123456"},
        {"nombre": "Pedro Plomero", "correo": "pedro@plomero.com", "contrasenna": "123456"},
        {"nombre": "Maria Pintora", "correo": "maria@pintora.com", "contrasenna": "123456"},
        {"nombre": "Lucas Electricista", "correo": "lucas@electrico.com", "contrasenna": "123456"}
    ]

    for user in usuarios:
        post("/usuarios", user)

    # 3. Colaboradores (Diferentes estados para AdminOkupo y Okupo)
    
    # --- COLABORADOR 1: Juan (Verificado y con Servicios) ---
    print("\n🔨 Configurando Colaborador 1: Juan (Verificado)")
    token_juan = get_token("juan@cerrajero.com", "123456")
    if token_juan:
        colab_id = post("/colaboradores", {
            "token_usuario": token_juan,
            "telefono": "5512345678",
            "sitio_web": "http://juan-cerrajero.com",
            "servicios": []
        }, token=token_juan)

        if colab_id:
            # Documentación
            post(f"/colaboradores/{colab_id}/documentacion", {
                "ine_frontal": "/archivos/ine_f_juan.jpg",
                "ine_trasera": "/archivos/ine_t_juan.jpg",
                "comprobante_domicilio": "/archivos/comp_juan.jpg",
                "foto_selfie_ine": "/archivos/selfie_juan.jpg"
            }, token=token_juan)

            # Verificación (Simulando Admin)
            post(f"/colaboradores/{colab_id}/verificar", {"estado": "verificado", "comentario": "Documentación completa y validada."})

            # Servicios
            post("/tecnico/servicios", {
                "colaborador_id": colab_id,
                "subcategoria_id": 1, # Apertura de Puerta
                "descripcion": "Apertura experta sin dañar la chapa.",
                "distancia_maxima_kilometros": "20",
                "precio_por_kilometro": "15",
                "latitud": "19.4326",
                "longitud": "-99.1332",
                "precios_urgencia": [
                    {"urgencia": "baja", "precio": "500", "servicio_id": 0},
                    {"urgencia": "media", "precio": "800", "servicio_id": 0},
                    {"urgencia": "alta", "precio": "1200", "servicio_id": 0},
                    {"urgencia": "critica", "precio": "2000", "servicio_id": 0}
                ]
            }, token=token_juan)

            # Horarios
            horarios = []
            for dia in range(1, 6): # Lunes a Viernes
                horarios.append({"colaborador_id": colab_id, "dia_semana": dia, "hora_inicio": "09:00", "hora_fin": "18:00", "activo": True})
            post(f"/colaboradores/{colab_id}/horarios", horarios, token=token_juan)

    # --- COLABORADOR 2: Pedro (Pendiente de Verificación) ---
    print("\n🔨 Configurando Colaborador 2: Pedro (Pendiente)")
    token_pedro = get_token("pedro@plomero.com", "123456")
    if token_pedro:
        colab_id = post("/colaboradores", {
            "token_usuario": token_pedro,
            "telefono": "5598765432",
            "sitio_web": None,
            "servicios": []
        }, token=token_pedro)
        
        if colab_id:
            post(f"/colaboradores/{colab_id}/documentacion", {
                "ine_frontal": "/archivos/ine_pedro.png",
                "ine_trasera": "/archivos/ine_t_pedro.png",
                "comprobante_domicilio": "/archivos/comp_pedro.png",
                "foto_selfie_ine": "/archivos/selfie_pedro.png"
            }, token=token_pedro)

    # --- COLABORADOR 3: Maria (Rechazada) ---
    print("\n🔨 Configurando Colaborador 3: Maria (Rechazada)")
    token_maria = get_token("maria@pintora.com", "123456")
    if token_maria:
        colab_id = post("/colaboradores", {
            "token_usuario": token_maria,
            "telefono": "5511223344",
            "sitio_web": None,
            "servicios": []
        }, token=token_maria)
        
        if colab_id:
            post(f"/colaboradores/{colab_id}/verificar", {"estado": "rechazado", "comentario": "Documentación borrosa, por favor sube fotos claras."})

    # --- COLABORADOR 4: Lucas (Verificado en otra zona) ---
    print("\n🔨 Configurando Colaborador 4: Lucas (Verificado - Santa Fe)")
    token_lucas = get_token("lucas@electrico.com", "123456")
    if token_lucas:
        colab_id = post("/colaboradores", {
            "token_usuario": token_lucas,
            "telefono": "5555555555",
            "sitio_web": None,
            "servicios": []
        }, token=token_lucas)

        if colab_id:
            post(f"/colaboradores/{colab_id}/verificar", {"estado": "verificado", "comentario": "OK"})
            post("/tecnico/servicios", {
                "colaborador_id": colab_id,
                "subcategoria_id": 7, # Cortocircuito
                "descripcion": "Electricista profesional 24/7.",
                "distancia_maxima_kilometros": "15",
                "precio_por_kilometro": "20",
                "latitud": "19.3631", # Santa Fe
                "longitud": "-99.2689",
                "precios_urgencia": [
                    {"urgencia": "baja", "precio": "600", "servicio_id": 0},
                    {"urgencia": "critica", "precio": "2500", "servicio_id": 0}
                ]
            }, token=token_lucas)

    print("\n✨ Base de datos poblada con éxito.")

if __name__ == "__main__":
    seed()
