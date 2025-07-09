import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)
app.secret_key = '12345.abcd.' # ¡CAMBIA ESTO! Debe ser una cadena aleatoria y segura

DATABASE = 'users.db'
PORT = 7500

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_user_to_db(username, password):
    password_hashed = generate_password_hash(password)
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                           (username, password_hashed))
            conn.commit()
        print(f"Usuario '{username}' agregado exitosamente.")
        return True
    except sqlite3.IntegrityError:
        print(f"Error: El usuario '{username}' ya existe.")
        return False

def get_user_from_db(username):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

def setup_initial_users():
    print("Configurando usuarios iniciales del examen...")
    # Nombres de los integrantes del examen (Carlos Montiel, Alexis Suarez)
    # ¡CAMBIA ESTAS CONTRASEÑAS POR LAS QUE QUIERAS USAR!
    users_to_add = {
        "CarlosMontiel": "cisco123",
        "AlexisSuarez": "cisco321"
    }

    for username, password in users_to_add.items():
        add_user_to_db(username, password) # Esta función ya maneja si existe o no

LOGIN_PAGE_HTML = """
<!doctype html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Examen DRY7122</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba[rgba](0, 0, 0, 0.1); width: 300px; text-align: center; }
        h2 { color: #333; margin-bottom: 20px; }
        .message { color: red; margin-bottom: 15px; }
        label { display: block; text-align: left; margin-bottom: 5px; color: #555; }
        input[type="text"], input[type="password"] { width: calc(100% - 22px); padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px; }
        input[type="submit"] { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        input[type="submit"]:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Acceso al Sistema</h2>
        {% if message %}
        <p class="message">{{ message }}</p>
        {% endif %}
        <form method="post">
            <label for="username">Usuario:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Contraseña:</label>
            <input type="password" id="password" name="password" required><br>
            <input type="submit" value="Iniciar Sesión">
        </form>
    </div>
</body>
</html>
"""

SUCCESS_PAGE_HTML = """
<!doctype html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bienvenido</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba[rgba](0, 0, 0, 0.1); width: 400px; text-align: center; }
        h2 { color: #333; margin-bottom: 20px; }
        p { color: #555; margin-bottom: 20px; }
        a { background-color: #28a745; color: white; padding: 10px 15px; border: none; border-radius: 4px; text-decoration: none; font-size: 16px; }
        a:hover { background-color: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h2>¡Bienvenido, {{ username }}!</h2>
        <p>Has iniciado sesión exitosamente.</p>
        <a href="/">Volver a Login</a>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_from_db(username)

        if user and check_password_hash(user[2], password):
            return render_template_string(SUCCESS_PAGE_HTML, username=username)
        else:
            message = "Usuario o contraseña incorrectos."
    return render_template_string(LOGIN_PAGE_HTML, message=message)

if __name__ == '__main__':
    init_db()
    setup_initial_users()

    print(f"\nServidor web Flask iniciado en http://127.0.0.1:{PORT}")
    print(f"Accede a la base de datos '{DATABASE}' con DB Browser for SQLite para verificar los usuarios y sus hashes.")
    app.run(host='0.0.0.0', port=PORT, debug=False)