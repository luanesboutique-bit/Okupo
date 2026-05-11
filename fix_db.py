import sqlite3

def fix_db():
    db_path = 'C:/Users/blanc/Finite/finit/finit.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Actualizar roles
    cur.execute("UPDATE usuario SET rol = 'admin' WHERE correo = 'admin@okupo.com'")
    cur.execute("UPDATE usuario SET rol = 'usuario' WHERE correo = 'ivan@okupo.com'")
    cur.execute("UPDATE usuario SET rol = 'colaborador' WHERE correo = 'juan@experto.com'")
    
    # Asegurar que Juan Experto (ID 8) es un colaborador verificado
    # Primero buscamos el ID de usuario de Juan
    cur.execute("SELECT id FROM usuario WHERE correo = 'juan@experto.com'")
    juan_user_id = cur.fetchone()
    
    if juan_user_id:
        juan_user_id = juan_user_id[0]
        # Ver si ya es colaborador
        cur.execute("SELECT id FROM colaborador WHERE usuario_id = ?", (juan_user_id,))
        colab = cur.fetchone()
        if colab:
            cur.execute("UPDATE colaborador SET es_verificado = 1, estado_verificacion = 'verificado' WHERE usuario_id = ?", (juan_user_id,))
        else:
            # Crear registro de colaborador si no existe (aunque seed_db ya lo hace)
            cur.execute("INSERT INTO colaborador (usuario_id, telefono, es_verificado, estado_verificacion) VALUES (?, '3312345678', 1, 'verificado')", (juan_user_id,))
            
    conn.commit()
    print("Base de datos corregida.")
    conn.close()

if __name__ == "__main__":
    fix_db()
