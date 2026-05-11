import sqlite3

def fix_services():
    db_path = 'C:/Users/blanc/Finite/finit/finit.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Colaborador 6 es Juan Experto
    colab_id = 6
    servicios_a_asegurar = [61, 52, 1, 4, 7, 10, 49, 53, 56, 109, 122, 123, 166]
    
    for sub_id in servicios_a_asegurar:
        cur.execute("SELECT id FROM servicio WHERE colaborador_id = ? AND subcategoria_id = ?", (colab_id, sub_id))
        if not cur.fetchone():
            cur.execute("INSERT INTO servicio (colaborador_id, subcategoria_id, descripcion, precio_por_kilometro, latitud, longitud) VALUES (?, ?, 'Servicio verificado', 10, 20.6736, -103.3444)", (colab_id, sub_id))
            print(f"✅ Servicio {sub_id} agregado para colab {colab_id}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_services()
