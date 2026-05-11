from decimal import Decimal

def calcular_desglose_pago(precio_total, metodo_pago='tarjeta', es_flete=False):
    """
    Calcula el desglose del pago siguiendo la nueva lógica fiscal y financiera:
    1. Total = precio_total
    2. Gasto Conekta = segun metodo (descontado primero)
    3. Impuestos = Total * (ISR + IVA + IMSS)
    4. BaseReparto = Total - Gasto Conekta - Impuestos
    5. Repartos = BaseReparto * porcentajes (75/15/5/5)
    """
    total = Decimal(str(precio_total))
    
    # 1. Calcular Gasto Conekta
    if metodo_pago == 'tarjeta':
        comision_base = (total * Decimal('0.029')) + Decimal('2.50')
        gasto_conekta = comision_base * Decimal('1.16') # + 16% IVA
    elif metodo_pago == 'efectivo' or metodo_pago == 'oxxo':
        gasto_conekta = Decimal('13.92') # 12.00 + 16% IVA
    elif metodo_pago == 'spei':
        gasto_conekta = Decimal('5.80') # 5.00 + 16% IVA
    else:
        gasto_conekta = Decimal('0.00')
    
    # 2. Calcular Impuestos Globales (sobre el total)
    isr_porcentaje = Decimal('0.021') if es_flete else Decimal('0.01')
    iva_porcentaje = Decimal('0.08')
    imss_porcentaje = Decimal('0.015')
    
    isr = total * isr_porcentaje
    iva = total * iva_porcentaje
    imss = total * imss_porcentaje
    total_impuestos = isr + iva + imss
    
    # 3. Base de Reparto
    base_reparto = total - gasto_conekta - total_impuestos
    
    # 4. Aplicar porcentajes sobre la base
    tecnico = base_reparto * Decimal('0.75')
    empresa = base_reparto * Decimal('0.15')
    mayoral = base_reparto * Decimal('0.05')
    socio = base_reparto * Decimal('0.05')
    
    return {
        "total": float(total),
        "gasto_conekta": float(gasto_conekta),
        "base_reparto": float(base_reparto),
        "reparto": {
            "tecnico": float(tecnico),
            "empresa": float(empresa),
            "mayoral": float(mayoral),
            "socio": float(socio)
        },
        "impuestos": {
            "isr": float(isr),
            "iva": float(iva),
            "imss": float(imss),
            "total_impuestos": float(total_impuestos)
        }
    }
