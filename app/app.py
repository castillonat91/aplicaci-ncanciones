from flask import Flask,  request, render_template, redirect, url_for, flash,session
import bcrypt
import mysql.connector
import base64
from werkzeug.security import generate_password_hash, check_password_hash

#creamos una instancia de la clase flask

app = Flask(__name__)
app.secret_key = '123456'

#configurar la conexion
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AGENDA2024"
)
cursor = db.cursor()

@app.route('/password/<contraencrip>')
def encriptarcontra(contraencrip):

    encriptar = generate_password_hash(contraencrip)
    valor = check_password_hash(encriptar,contraencrip)
    return valor


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method =='POST':
        username= request.form.get('txtusuario')
        password= request.form.get('txtcontrasena')

        sql = 'SELECT usuarioper, contraper FROM Personas where usuarioper = %s'
        cursor.execute(sql,(username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['contraper'], password):
            session['usuario'] = user['usuarioper']
            session['roles'] = user['roles']

            if user['roles'] == 'administrador':
                return redirect(url_for('lista'))
            
        cursor = db.cursor()
        cursor.execute('SELECT usuarioper, contraper FROM Personas where usuarioper = %s', (username,))
        resultado = cursor.fetchone()

        if resultado and check_password_hash (password) == resultado[1]:
            session['usuario'] = username
            return redirect(url_for('lista'))
        else:
            error='Credenciales invalidas. por favor intentarlo de nuevo'
            return render_template('sesion.html', error=error)
    return render_template('sesion.html')
        
#definir rutas
@app.route('/')
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Personas')
    usuario = cursor.fetchall() 
    return render_template('index.html',  personas = usuario)


@app.route('/registrar', methods=['GET','POST'])
def registrar_usuario():

    if request.method == 'POST':
        NOMBRE = request.form.get('nombrePer')
        APELLIDO = request.form.get('apellidoPer')
        EMAIL = request.form.get('correoPer')
        DIRECCION = request.form.get('direccionPer')
        TELEFONO = request.form.get('telefonoPer')
        USUARIO = request.form.get('usuarioPer')
        CONTRASENA = request.form.get('contrasenaPer')
        roles = request.form.get('txtrol')
       
        contrasenaencriptada= generate_password_hash(CONTRASENA)
        
        #insertar datos a la tlaba personas
        
        cursor.execute("INSERT INTO Personas(nombreper,apellidoper,emailper,dirper,telper,usuarioper,contraper,roles)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                       (NOMBRE,APELLIDO,EMAIL,DIRECCION,TELEFONO,USUARIO,contrasenaencriptada,roles))
        db.commit()
        return redirect(url_for('registrar_usuarios'))
    return render_template('registrar.html')

@app.route("/editar/<int:id>", methods=["POST", "GET"])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == "POST":
        nombreper = request.form.get("nombre")
        apelldioper = request.form.get("apellido")
        emailper = request.form.get("email")
        dirreccionper = request.form.get("direccion")
        telefonoper = request.form.get("telefono")
        usuarioper = request.form.get("usuario")
        contraper = request.form.get("contraseña")
         
        sql = "update Personas set nombreper=%s, apellidoper=%s,emailper=%s,dirper=%s, telper=%s,usuarioper=%s, contraper=%s where idper=%s"
        cursor.execute(
            sql,
            (
                nombreper,
                apelldioper,
                emailper,
                dirreccionper,
                telefonoper,
                usuarioper,
                contraper,
                id,
            ),
        )
        db.commit()

        return redirect(url_for("lista"))

    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Personas WHERE idper=%s", (id,))
        data = cursor.fetchall()
        return render_template("editar.html", usuario=data[0])
    
    
@app.route("/eliminar/<int:id>", methods=["GET"])
def eliminar_usuario(id):
    cursor = db.cursor()
    if request.method == "GET":
       cursor.execute('DELETE FROM Personas WHERE idper=%s',(id,))
       db.commit()
       return redirect(url_for("lista"))
    
#------------------------------------------------------------------------------------------------------------------------------------------
#canciones
@app.route('/listaCanciones')
def lista_canciones():
    cursor = db.cursor()
    cursor.execute('SELECT titulo,artista,genero,lanzamiento,precio,duracion,imagen FROM canciones')
    cancion = cursor.fetchall() 

    #crear lista para almacenar canciones

    if cancion:
        cancionlist = []
        for canciones in cancion:
            #convertir la imagen formato base64
            imagen = base64.b64encode(canciones[6]).decode('utf-8')
            #agregar datos cancion a la lista
            cancionlist.append({
                'titulo':canciones[0],
                'artista':canciones[1],
                'genero':canciones[2],
                'lanzamiento':canciones[3],
                'precio':canciones[4],
                'duracion':canciones[5],
                'imagen':imagen
            })
        return render_template('listascanciones.html',  canciones = cancionlist)
    else:
        return print("canciones no encontradas")

@app.route('/registrarCanciones', methods = ['GET','POST'])
def registrar_cancion():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        artista = request.form.get('artista')
        genero = request.form.get('genero')
        lanzamiento = request.form.get('lanzamiento')
        precio = request.form.get('precio')
        Duracion = request.form.get('duracion')
        Imagen = request.files['imagen']
        imagenblog = Imagen.read()

        cursor = db.cursor()
        cursor.execute("INSERT INTO canciones(titulo,artista,genero,lanzamiento, precio, duracion, imagen)VALUES(%s,%s,%s,%s,%s,%s,%s)",(titulo,artista,genero,lanzamiento,precio,Duracion,imagenblog))
        db.commit()
        print("cancion registrada exitosamente")
        return redirect(url_for('registrar_cancion'))
    return render_template('registrocancion.html')

@app.route('/editar_cancion/<int:id>',methods = ['POST','GET'])
def editar_cancion(id):
    cursor = db.cursor()
    if request.method == 'POST':
        #el nombre dentro del get es tomado del formulario editar y debe ser diferente al formulario de registro
        
        tituloCan = request.form.get('tituloCan')
        artistaCan = request.form.get('artistaCan')
        generoCan = request.form.get('generoCan')
        lanzamientoCan = request.form.get('lanzamientoCan')
        precioCan = request.form.get('precioCan')
        DuracionCan = request.form.get('duracionCan')
        ImagenCan= request.files.get('imagenCan')
        #Imagen = request.files['imagenCan']
        #imagenblog = Imagen.read()
    
        sql = "UPDATE canciones SET titulo = %s, artista = %s, genero = %s, lanzamiento= %s, precio = %s, duracion = %s, imagen = %s WHERE id_can = %s"
        cursor.execute(sql, (tituloCan,artistaCan,generoCan,lanzamientoCan, precioCan, DuracionCan, ImagenCan,id))

        db.commit()
        flash('Datos actualizados correctamente', 'success')
        
        return redirect(url_for("lista_canciones"))
        
    else:
        #obtener los datos de la persona que se va editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM canciones WHERE id_can = %s',(id,))
        data = cursor.fetchall()
        cursor.close()

        return render_template('cancioneditar.html', cancion = data[0])

@app.route('/eliminar_cancion/<int:id>',methods = ['GET'])
def eliminar_cancion(id):
    cursor = db.cursor()
    if request.method == "GET":
       cursor.execute('DELETE FROM canciones WHERE id_can=%s',(id,))
       db.commit()
    return redirect(url_for("lista_canciones"))
  
# para ejecutar la aplicacion
if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True,port=5005)