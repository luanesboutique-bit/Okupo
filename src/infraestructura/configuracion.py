import os

CLAVE_SECRETA = os.environ.get('CLAVE_SECRETA', 'clave_secreta_okupo_2024')
URL_BASE_API = os.environ.get('URL_BASE_API', "http://localhost:3000")
MODO_MOCK = True # Cambiar a False para usar la API real de Finite
