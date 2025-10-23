from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, logout_user
from extensions import db
import controlador_juegos
from models import Juego, User
from werkzeug.security import generate_password_hash, check_password_hash

# --- Importar el blueprint de autenticación ---
from app.auth import auth

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave secreta obligatoria para sesiones y formularios
app.config['SECRET_KEY'] = 'keyri2025'

# Inicializar base de datos
db.init_app(app)

# Configurar LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # redirige al login si no hay sesión
login_manager.session_protection = 'strong'
login_manager.remember_cookie_duration = 0  

# Registrar blueprint de autenticación (solo una vez)
app.register_blueprint(auth)

# Callback para cargar usuario por ID (Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ---------------- RUTAS ---------------- #

# Índice: redirige siempre al login y cierra cualquier sesión activa
@app.route("/")
def index():
    logout_user()
    print(app.url_map) 
    return redirect(url_for('auth.login'))

# Listar juegos
@app.route("/juegos")
@login_required
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

# Formulario para agregar juego
@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

# Guardar nuevo juego
@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    return redirect("/juegos")

# Eliminar juego
@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    id = request.form["id"]
    controlador_juegos.eliminar_juego(id)
    return redirect("/juegos")

# Formulario para editar juego
@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

# Actualizar juego
@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")

# ---------------- EJECUTAR APP ---------------- #
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # crea tablas 'juegos' y 'users' si no existen
    app.run(port=8000, debug=True)