import sqlite3
import hashlib
from flask import Flask, request

app = Flask(__name__)

db_name = 'usuarios.db'

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

@app.route('/')
def index():
    return 'Sitio web de gestión de claves'

@app.route('/registro', methods=['POST'])
def registro():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                (nombre TEXT PRIMARY KEY NOT NULL,
                contraseña TEXT NOT NULL)''')
    conn.commit()

    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_password(password)

    try:
        c.execute("INSERT INTO usuarios (nombre, contraseña) VALUES (?, ?)",
                  (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El nombre de usuario ya ha sido registrado."

    return "Registro exitoso"

def verificar_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT contraseña FROM usuarios WHERE nombre = ?", (username,))
    records = c.fetchone()
    conn.close()

    if not records:
        return False

    hashed_password = hash_password(password)
    return records[0] == hashed_password

@app.route('/inicio-sesion', methods=['POST'])
def inicio_sesion():
    username = request.form['username']
    password = request.form['password']

    if verificar_hash(username, password):
        return 'Inicio de sesión exitoso'
    else:
        return 'Nombre de usuario o contraseña inválidos'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4850)
