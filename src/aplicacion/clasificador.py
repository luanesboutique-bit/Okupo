def clasificar_servicio(frase):
    frase = frase.lower()
    
    mapeo = {
        1: ['cerrajeria', 'chapa', 'puerta', 'llave', 'abrir'],
        2: ['plomeria', 'fuga', 'tubería', 'agua', 'faucet', 'lavabo', 'wc'],
        3: ['electricidad', 'luz', 'corto', 'ventilador', 'cable', 'interruptor', 'foco'],
        4: ['limpieza general', 'limpiar', 'casa', 'barrer', 'trapear'],
        5: ['limpieza muebles', 'sillones', 'sala', 'colchon', 'lavado muebles'],
        6: ['armado', 'closet', 'cocina', 'mueble', 'ensamblar'],
        7: ['fletes', 'mudanza', 'mover', 'carga', 'transporte', 'estufa'],
        8: ['albañileria', 'piso', 'ceramica', 'resanar', 'pared', 'cemento'],
        9: ['reparaciones', 'mantenimiento', 'arreglar', 'descompuesto'],
        10: ['paneles', 'solar', 'instalacion solar', 'energia'],
        11: ['autos', 'lavado', 'estetica', 'carro', 'auto'],
        12: ['instalaciones', 'minisplit', 'tv', 'rack', 'soporte'],
    }
    
    for cat_id, palabras in mapeo.items():
        for palabra in palabras:
            if palabra in frase:
                return cat_id
                
    return 13
