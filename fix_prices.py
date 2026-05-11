import sqlite3

def fix_prices():
    db_path = 'C:/Users/blanc/Finite/finit/finit.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Obtener todos los servicios que no tienen precios de urgencia
    cur.execute("SELECT id FROM servicio")
    servicios = cur.fetchall()
    
    for (s_id,) in servicios:
        cur.execute("SELECT id FROM precio_servicio_urgencia WHERE servicio_id = ?", (s_id,))
        if not cur.fetchone():
            # Insertar precios base
            for urgencia in ['baja', 'media', 'alta', 'critica']:
                precio = 300 if urgencia == 'baja' else 500 if urgencia == 'media' else 800 if urgencia == 'alta' else 1500
                cur.execute("INSERT INTO precio_servicio_urgencia (servicio_id, urgencia, precio) VALUES (?, ?, ?)", (s_id, urgencia, precio))
            print(f"✅ Precios agregados para servicio {s_id}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_prices()
