from datetime import datetime, time, date
import pytz

def calcular_tipo_tarifa(es_urgencia_forzada=False):
    """
    Determina el tipo de tarifa ('normal', 'medio', 'urgente') 
    basado en el día y hora actuales (usando hora CDMX).
    """
    # Configurar zona horaria de México
    tz = pytz.timezone('America/Mexico_City')
    ahora = datetime.now(tz)
    fecha_actual = ahora.date()
    dia_semana = ahora.weekday()  # 0=lunes, 6=domingo
    hora_actual = ahora.time()
    
    # Lista de festivos (día, mes)
    festivos = [
        (1, 1), (5, 2), (21, 3), (1, 5), 
        (16, 9), (20, 11), (24, 12), (25, 12), (31, 12)
    ]
    es_festivo = (fecha_actual.day, fecha_actual.month) in festivos
    
    print(f"DEBUG [Tarifas]: Hora: {hora_actual}, Día: {dia_semana}, Festivo: {es_festivo}, Forzada: {es_urgencia_forzada}")
    
    # 1. Tarifa Urgencia
    # Urgencia: Botón manual o entre 23:00 y 07:59
    if es_urgencia_forzada:
        return 'urgente'
    
    if hora_actual >= time(23, 0) or hora_actual < time(8, 0):
        return 'urgente'
    
    # 2. Tarifa Media (Sábados, Domingos, Festivos)
    if dia_semana >= 5 or es_festivo:
        return 'medio'
    
    # Horario tarde para tarifa media (6 PM a 11 PM -> 18:00 a 22:59)
    if time(18, 0) <= hora_actual < time(23, 0):
        return 'medio'
    
    # 3. Tarifa Normal (8 AM a 6 PM -> 08:00 a 17:59)
    return 'normal'
