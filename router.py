from flask import Flask,  send_from_directory, render_template, redirect, url_for, request, session 
from flask_session import Session
from flask_cors import CORS 
from database import get_user_role
from permissions import PERMISOS
import auth  # Importa el archivo auth.py
import dashboard
import expedientes 
import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__, template_folder='./templates/')
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de la sesión
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Usaremos el sistema de archivos para almacenar las sesiones por simplicidad
Session(app)

# Definir las rutas de este archivo
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/signin')
def sign_in_route():
    print("La función sign_in_route ha sido ejecutada!")
    return render_template('signin.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if auth.check_password(email, password):  
            # Redirige al usuario a la página principal si las credenciales son correctas.
            session['user_email'] = email            
            return redirect(url_for('dashboard_route'))
        else:
            # Si las credenciales son incorrectas, puedes enviar un mensaje de error.
            return "Credenciales incorrectas", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard_route():
    user_email = session.get('user_email')
    if not user_email:
        return redirect(url_for('login'))
    
    user_role = get_user_role(user_email)

    if not user_role:
        return "Usuario no encontrado o sin rol definido.", 404

    # Determinar permisos del usuario
    enlaces_permitidos = {key: value for key, value in PERMISOS.items() if user_role in value}

    return render_template('dashboard.html', enlaces=enlaces_permitidos)


# Adjuntar las rutas de autenticación desde auth.py
auth.setup_routes(app)

# Adjuntar las rutas del dashboard desde dashboard.py
dashboard.setup_dashboard_routes(app)

# Adjuntar las rutas de expedientes desde expedientes.py
expedientes.setup_expedientes_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
