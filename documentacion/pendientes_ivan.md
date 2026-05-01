 Nota para tu amigo (👨‍💻 Lógica):
  He creado el archivo templates/registro_tecnico_datos.html. Él solo debe añadir esta ruta en src/web/rutas/colaboradores.py para activarlo:

   1 @blueprint.route('/registro/tecnico/datos')
   2 def registro_tecnico_datos():
   3     return render_template('registro_tecnico_datos.html')

Nota para tu amigo (👨‍💻 Lógica):
  He creado el archivo templates/seleccion_rol.html. Para que sea visible, él solo necesita añadir una ruta sencilla en main.py:

   1 @app.route('/bienvenida')
   2 def seleccion_rol():
   3     return render_template('seleccion_rol.html')

Nota para tu amigo (👨‍💻 Lógica):
  He creado el archivo templates/registro_tecnico_documentos.html. Debería estar vinculado a su ruta de colaboradores para procesar los archivos de
  imagen.

He creado el archivo templates/cotizar_especial.html. Para que el botón de "COTIZAR OTRO SERVICIO" del Home funcione, debe apuntar a una nueva
  ruta que él cree en principal.py.

  Nota para tu amigo (👨‍💻 Lógica):
  Para que la pantalla de políticas sea accesible, solo necesita añadir esta ruta en principal.py:

   1 @blueprint.route('/politicas')
   2 def politicas():
   3     return render_template('politicas.html')

  Nota para tu amigo (👨‍💻 Lógica):
  He creado templates/dashboard_tecnico.html. Él debe añadir esta ruta en colaboradores.py:

   1 @blueprint.route('/dashboard')
   2 @login_requerido
   3 def dashboard():
   4     return render_template('dashboard_tecnico.html')

 Nota para tu amigo (👨‍💻 Lógica):
  He creado templates/detalle_trabajo_tecnico.html. Él debe vincular esta pantalla desde el Dashboard para que, al dar clic en una solicitud, se
  abra este detalle con los datos reales del cliente.


