import requests
import json
import time

API_URL = "http://localhost:5001"

def post(endpoint, data, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = requests.post(f"{API_URL}{endpoint}", json=data, headers=headers)
        if r.status_code in [200, 201]:
            # print(f"✅ OK: {endpoint}")
            return r.json() if r.text else True
        else:
            # print(f"❌ Error {r.status_code} en {endpoint}: {r.text}")
            return None
    except Exception as e:
        print(f"🔥 Error conectando a {endpoint}: {e}")
        return None

def get_token(correo, contrasenna):
    res = post("/login", {"correo": correo, "contrasenna": contrasenna})
    return res if isinstance(res, str) else None

def seed():
    print("🚀 Iniciando poblado de base de datos para D'Mayoral...")

    # 1. Usuarios base con ROLES
    usuarios = [
        {"nombre": "D'Mayoral Admin", "correo": "admin@okupo.com", "contrasenna": "admin", "rol": "admin"},
        {"nombre": "Ivan Cliente", "correo": "ivan@okupo.com", "contrasenna": "123456", "rol": "usuario"},
        {"nombre": "Juan Experto", "correo": "juan@experto.com", "contrasenna": "123456", "rol": "colaborador"},
    ]

    for user in usuarios:
        res = post("/usuarios", user)
        if res:
            print(f"👤 Usuario creado: {user['nombre']} ({user['rol']})")

    # 2. Registrar a Juan como Colaborador con los 13 servicios
    print("\n🔨 Configurando Colaborador: Juan (Con todos los servicios)")
    token_juan = get_token("juan@experto.com", "123456")
    if not token_juan:
        print("❌ No se pudo obtener token para Juan")
        return

    # Mapeo de subcategorías para los 13 servicios
    # Basado en la consulta previa de finit.db
    servicios_mapeo = [
        {"nombre": "CERRAJERÍA", "sub_id": 1},
        {"nombre": "PLOMERÍA", "sub_id": 4},
        {"nombre": "ELECTRICIDAD", "sub_id": 7},
        {"nombre": "LIMPIEZA GENERAL", "sub_id": 10},
        {"nombre": "LIMPIEZA MUEBLES", "sub_id": 49},
        {"nombre": "ARMADO", "sub_id": 53},
        {"nombre": "FLETES", "sub_id": 61},
        {"nombre": "ALBAÑILERÍA", "sub_id": 56},
        {"nombre": "REPARACIONES", "sub_id": 109},
        {"nombre": "PANELES", "sub_id": 122}, # Cortocircuitos (fallback)
        {"nombre": "AUTOS", "sub_id": 52},
        {"nombre": "INSTALACIONES", "sub_id": 123}, # Instalacion de Lamparas
        {"nombre": "SERVICIOS EXTRA", "sub_id": 166}, # Volado de muebles
    ]

    servicios_para_registro = []
    for s in servicios_mapeo:
        servicio_data = {
            "colaborador_id": 0, # Se asignará en el back
            "subcategoria_id": s["sub_id"],
            "descripcion": f"Experto en {s['nombre']}",
            "distancia_maxima_kilometros": "50",
            "precio_por_kilometro": "10",
            "latitud": "20.6736",
            "longitud": "-103.3444"
        }
        precios_urgencia = [
            {"urgencia": "baja", "precio": "300", "servicio_id": 0},
            {"urgencia": "media", "precio": "500", "servicio_id": 0},
            {"urgencia": "alta", "precio": "800", "servicio_id": 0},
            {"urgencia": "critica", "precio": "1500", "servicio_id": 0}
        ]
        servicios_para_registro.append([servicio_data, precios_urgencia])

    colab_id = post("/colaboradores", {
        "token_usuario": token_juan,
        "telefono": "3312345678",
        "sitio_web": "http://juan-experto.com",
        "servicios": servicios_para_registro
    }, token=token_juan)

    if colab_id:
        print(f"✅ Colaborador Juan registrado con ID: {colab_id}")
        
        # Subir "Documentación" para que aparezca en el panel de admin
        post(f"/colaboradores/{colab_id}/documentacion", {
            "ine_frontal": "/static/images/ine_ejemplo.jpg",
            "ine_trasera": "/static/images/ine_ejemplo.jpg",
            "comprobante_domicilio": "/static/images/comp_ejemplo.jpg",
            "foto_selfie_ine": "/static/images/selfie_ejemplo.jpg"
        }, token=token_juan)
        print("📄 Documentación subida para Juan (Estado: Pendiente)")

    print("\n✨ Base de datos lista para pruebas.")
    print("Admin: admin@okupo.com / admin")
    print("Cliente: ivan@okupo.com / 123456")

if __name__ == "__main__":
    seed()
