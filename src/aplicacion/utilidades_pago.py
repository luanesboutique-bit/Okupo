from decimal import Decimal
from src.infraestructura.cliente_api import api_post

def calcular_desglose_pago(precio_total, metodo_pago='tarjeta', es_flete=False, token=None):
    """
    DEPRECATED LOCAL LOGIC: Now calls the Finite (Rust) engine to ensure 
    consistency across all platforms (Web, Mobile, Tauri).
    """
    datos = {
        "precio_total": str(precio_total),
        "metodo_pago": metodo_pago,
        "es_flete": es_flete
    }
    
    # Intentar obtener el desglose desde el motor Rust
    respuesta = api_post("/pagos/desglose", datos, token=token)
    
    if respuesta and isinstance(respuesta, dict):
        # Mapear estructura de Rust (plana) a la estructura esperada por los templates de Okupo (anidada)
        return {
            "total": float(respuesta.get('total', 0)),
            "gasto_conekta": float(respuesta.get('gasto_conekta', 0)),
            "base_reparto": float(respuesta.get('base_reparto', 0)),
            "reparto": {
                "tecnico": float(respuesta.get('reparto_tecnico', 0)),
                "empresa": float(respuesta.get('reparto_empresa', 0)),
                "mayoral": float(respuesta.get('reparto_mayoral', 0)),
                "socio": float(respuesta.get('reparto_socio', 0))
            },
            "impuestos": {
                "isr": float(respuesta.get('impuesto_isr', 0)),
                "iva": float(respuesta.get('impuesto_iva', 0)),
                "imss": float(respuesta.get('impuesto_imss', 0)),
                "total_impuestos": float(respuesta.get('impuesto_isr', 0)) + float(respuesta.get('impuesto_iva', 0)) + float(respuesta.get('impuesto_imss', 0))
            }
        }

    # Fallback básico si el motor no responde (no recomendado para producción)
    print("⚠️ ADVERTENCIA: Usando fallback local para desglose de pago. Motor Rust no disponible.")
    total = Decimal(str(precio_total))
    return {
        "total": float(total),
        "gasto_conekta": 0.0,
        "base_reparto": float(total),
        "reparto_tecnico": float(total * Decimal('0.75')),
        "reparto_empresa": float(total * Decimal('0.15')),
        "reparto_mayoral": float(total * Decimal('0.05')),
        "reparto_socio": float(total * Decimal('0.05')),
        "impuesto_isr": 0.0,
        "impuesto_iva": 0.0,
        "impuesto_imss": 0.0
    }
