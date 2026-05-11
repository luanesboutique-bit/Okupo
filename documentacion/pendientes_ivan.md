Nota para tu amigo (👨‍💻 Lógica):
  He creado el archivo templates/seleccion_rol.html. Para que sea visible, él solo necesita añadir una ruta sencilla en main.py:

   1 @app.route('/bienvenida')
   2 def seleccion_rol():
   3     return render_template('seleccion_rol.html')

He creado el archivo templates/cotizar_especial.html. Para que el botón de "COTIZAR OTRO SERVICIO" del Home funcione, debe apuntar a una nueva
  ruta que él cree en principal.py.

  Nota para tu amigo (👨‍💻 Lógica):
  Para que la pantalla de políticas sea accesible, solo necesita añadir esta ruta en principal.py:

   1 @blueprint.route('/politicas')
   2 def politicas():
   3     return render_template('politicas.html')

(Las tareas de lógica de backend y dashboard básico de colaborador han sido completadas)

- ✅ Dashboard de Colaborador con 4 secciones (Configuración, Portafolio, Solicitudes, Próximos).
- ✅ Lógica de redirección basada en rol tras el login.
- ✅ Menú de usuario dinámico en Home (muestra nombre y opciones según login).
- ✅ Ruta de perfil básica (/perfil) para evitar 404.
