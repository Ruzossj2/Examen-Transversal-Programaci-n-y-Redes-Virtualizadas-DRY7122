from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import os

# --- Base de datos ---
DB_NAME = 'usuarios.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Inicializa base de datos y usuario por defecto ---
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Crear tabla
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

        # Crear usuario Benjamin Castillo si no existe
        usuario = "Benjamin Castillo"
        contraseña = "12345"
        password_hash = hash_password(contraseña)

        cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (usuario,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (usuario, password_hash))
            conn.commit()
            print(f"Usuario '{usuario}' creado con contraseña '12345'.")

# --- Agrega nuevos usuarios ---
def agregar_usuario(nombre, password):
    password_hash = hash_password(password)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nombre, password_hash))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

# --- Valida login ---
def validar_usuario(nombre, password):
    password_hash = hash_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND password_hash=?", (nombre, password_hash))
        return cursor.fetchone() is not None

# --- Ejecutar creación de tabla y usuario base ---
init_db()

# --- Web app ---
app = Flask(__name__)

html = '''
<!DOCTYPE html>
<html>
<head><title>Gestión de Usuarios</title></head>
<body>
    <h2>Registrar Usuario</h2>
    <form method="POST" action="/registrar">
        Nombre: <input name="nombre"><br>
        Contraseña: <input type="password" name="password"><br>
        <button type="submit">Registrar</button>
    </form>
    <h2>Validar Usuario</h2>
    <form method="POST" action="/validar">
        Nombre: <input name="nombre"><br>
        Contraseña: <input type="password" name="password"><br>
        <button type="submit">Validar</button>
    </form>
    <p>{{ mensaje }}</p>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    return render_template_string(html, mensaje='')

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    password = request.form['password']
    if agregar_usuario(nombre, password):
        mensaje = 'Usuario registrado correctamente.'
    else:
        mensaje = 'El usuario ya existe.'
    return render_template_string(html, mensaje=mensaje)

@app.route('/validar', methods=['POST'])
def validar():
    nombre = request.form['nombre']
    password = request.form['password']
    if validar_usuario(nombre, password):
        mensaje = 'Usuario válido. Acceso permitido.'
    else:
        mensaje = 'Nombre o contraseña incorrecta.'
    return render_template_string(html, mensaje=mensaje)

# --- Iniciar aplicación en puerto 5800 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800)

