from functools import wraps
from flask import session, redirect, url_for

def login_requerido(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('autenticacion.login'))
        return f(*args, **kwargs)
    return funcion_decorada
