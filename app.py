from flask import Flask, render_template, redirect, request, session
from flask_mysqldb import MySQL


app = Flask(__name__, template_folder='template')

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia si tienes una contraseña
app.config['MYSQL_DB'] = 'cine'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')
 
@app.route('/index')
def index():
    if 'logueado' in session and session['logueado']:
        return render_template('index.html')
    else:
        return redirect('/')  # Redirige al login si no está logueado

# Función de login
@app.route('/acceso-login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'txtcorreo' in request.form and 'txtcontraseña' in request.form:
        _correo = request.form['txtcorreo']
        _contraseña = request.form['txtcontraseña']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo=%s AND contraseña=%s', (_correo, _contraseña,))
        account = cur.fetchone()
        cur.close()  # Cierra el cursor

        if account:
            session['logueado'] = True
            return redirect('/index')  # Redirige a index después de iniciar sesión
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')

@app.route('/logout')
def logout():
    session.pop('logueado', None)  # Elimina el estado de sesión
    return redirect('/')  # Redirige al login


# Función de registro


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        
        correo = request.form['txtcorreo']
        contraseña = request.form['txtcontraseña']
        
        
        if not correo or not contraseña:
            error = "Todos los campos son obligatorios"
            return render_template('registro.html', error=error)


        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s', [correo])
        user = cur.fetchone()

        if user:
            error = "El usuario ya existe"
            return render_template('registro.html', error=error)
        else:
        
            cur.execute('INSERT INTO usuarios (correo, contraseña) VALUES (%s, %s)', (correo, contraseña))
            mysql.connection.commit()
            cur.close()

            return render_template(('login.html'))

    return render_template('registro.html')

if __name__ == '__main__':
    app.secret_key = "proyecto_cine"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
