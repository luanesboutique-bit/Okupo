from functools import wraps
from flask import session, redirect, url_for, request

def login_requerido(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('autenticacion.login', proximo=request.url))
        return f(*args, **kwargs)
    return funcion_decorada
