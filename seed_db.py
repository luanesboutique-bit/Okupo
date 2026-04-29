import requests
import json

API_URL = "http://localhost:3000"

def post(endpoint, data):
    try:
        r = requests.post(f"{API_URL}{endpoint}", json=data)
        if r.status_code in [200, 201]:
            print(f"✅ OK: {endpoint}")
            return r.json() if r.text else True
        else:
            print(f"❌ Error {r.status_code} en {endpoint}: {r.text}")
            return None
    except Exception as e:
        print(f"🔥 Error conectando a {endpoint}: {e}")
        return None

def seed():
    print("🚀 Iniciando poblado de base de datos de prueba...")

    # 1. Crear Categorías (Piedras y Maderas)
    categorias = [
        {"nombre": "Cerrajería", "icono": "fas fa-key"},
        {"nombre": "Plomería", "icono": "fas fa-faucet"},
        {"nombre": "Electricidad", "icono": "fas fa-bolt"},
        {"nombre": "Limpieza", "icono": "fas fa-spray-can"},
        {"nombre": "Muebles", "icono": "fas fa-couch"},
        {"nombre": "Fletes", "icono": "fas fa-truck"},
        {"nombre": "Jardinería", "icono": "fas fa-leaf"},
        {"nombre": "Pintura", "icono": "fas fa-paint-roller"},
        {"nombre": "Albannilería", "icono": "fas fa-hammer"},
        {"nombre": "Computación", "icono": "fas fa-laptop"}
    ]

    for cat in categorias:
        post("/categorias", cat)

    # 2. Crear Subcategorías (Ejemplos)
    subcategorias = [
        {"categoria_id": 1, "nombre": "Apertura de Puerta"},
        {"categoria_id": 1, "nombre": "Cambio de Chapa"},
        {"categoria_id": 2, "nombre": "Fuga de Agua"},
        {"categoria_id": 2, "nombre": "Destape de Drenaje"},
        {"categoria_id": 3, "nombre": "Cortocircuito"},
        {"categoria_id": 3, "nombre": "Instalación de Lámpara"}
    ]
    for sub in subcategorias:
        post(f"/categorias/{sub['categoria_id']}/subcategorias", {"nombre": sub['nombre']})

    # 3. Crear Usuarios de Prueba (Técnicos y Clientes)
    usuarios = [
        {"nombre": "Ivan Cliente", "correo": "ivan@okupo.com", "contrasenna": "123456"},
        {"nombre": "Pedro Tecnico", "correo": "pedro@tecnico.com", "contrasenna": "123456"},
        {"nombre": "Maria Expert", "correo": "maria@expert.com", "contrasenna": "123456"}
    ]
    
    user_ids = []
    for user in usuarios:
        res = post("/usuarios", user)
        # Nota: La API actual parece devolver el token o algo similar segun main.py
        # Pero para seed nos interesaría que devuelva el ID o usar el login para obtenerlo.
        # Asumiremos que se crearon correctamente.

    print("\n💡 Datos de prueba básicos enviados.")
    print("Nota: Asegúrate de que el motor Finite (Rust) esté corriendo en el puerto 3000.")

if __name__ == "__main__":
    seed()
