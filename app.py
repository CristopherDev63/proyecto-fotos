# --- Importaciones ---
# Importamos las librerías necesarias.
# Flask es el framework web.
# render_template nos ayuda a mostrar páginas HTML.
# request, redirect, url_for, flash, session son para manejar peticiones,
# redirecciones, URLs, mensajes y sesiones de usuario.
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

# --- Configuración de la Aplicación ---
# Creamos la aplicación Flask.
app = Flask(__name__)

# Clave secreta para proteger las sesiones. Es importante que sea segura.
app.secret_key = os.urandom(24)

# Carpeta donde se guardarán las imágenes subidas.
app.config['UPLOAD_FOLDER'] = 'static/images'

# Tamaño máximo de los archivos que se pueden subir (16 MB).
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ruta a la base de datos. Usa la variable de entorno POSTGRES_URL si está disponible (para Vercel),
# si no, usa la base de datos local sqlite.
db_uri = os.environ.get('POSTGRES_URL')
if db_uri and db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')


# Desactiva una función de SQLAlchemy que no necesitamos y que consume recursos.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Inicialización de la Base de Datos ---
# Creamos el objeto de la base de datos.
db = SQLAlchemy(app)

# --- Constantes ---
# Definimos qué extensiones de archivo están permitidas.
EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


# --- Modelos de la Base de Datos ---
# Un modelo es como una "plantilla" para una tabla en la base de datos.

# Modelo para la tabla de Usuarios.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada usuario.
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario, no puede repetirse.
    password_hash = db.Column(db.String(128), nullable=False)  # Contraseña guardada de forma segura.
    role = db.Column(db.String(20), nullable=False, default='user')  # Rol del usuario (user o admin)
    images = db.relationship('Image', backref='author', lazy=True)  # Relación con las imágenes que ha subido.

# Modelo para la tabla de Imágenes.
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada imagen.
    filename = db.Column(db.String(120), nullable=False)  # Nombre del archivo de la imagen.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ID del usuario que subió la imagen.
    status = db.Column(db.String(20), nullable=False, default='pending')  # Estado de la imagen (pending, approved, rejected)


# --- Comando para inicializar la BD ---
# Esto crea un comando que podemos ejecutar desde la terminal para crear las tablas.
# Ejemplo: "flask init-db"
@app.cli.command("init-db")
def init_db_command():
    """Crea las tablas de la base de datos."""
    db.create_all()
    print("Base de datos inicializada.")


# --- Rutas de la Aplicación ---
# Las rutas definen qué pasa cuando un usuario visita una URL.

@app.route('/')
def index():
    """Página principal - muestra todas las imágenes aprobadas."""
    # Obtenemos todas las imágenes aprobadas de la base de datos, ordenadas por la más nueva.
    imagenes = Image.query.filter_by(status='approved').order_by(Image.id.desc()).all()
    # Mostramos la página 'index.html' y le pasamos los datos de las imágenes.
    return render_template('index.html', imagenes=imagenes, total=len(imagenes))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de nuevos usuarios."""
    # Si el usuario envía el formulario (método POST)...
    if request.method == 'POST':
        # Obtenemos el nombre de usuario y la contraseña del formulario.
        username = request.form['username']
        password = request.form['password']
        
        # Definimos el rol por defecto.
        role = 'user'
        
        # Si la contraseña es la maestra, asignamos el rol de admin.
        if password == 'cris6336':
            role = 'admin'

        # Comprobamos si el nombre de usuario ya existe.
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('register'))

        # Creamos un nuevo usuario con la contraseña encriptada y el rol asignado.
        nuevo_usuario = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        # Guardamos el nuevo usuario en la base de datos.
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('¡Registro exitoso! Por favor, inicia sesión.', 'success')
        return redirect(url_for('login'))
    # Si el usuario solo visita la página (método GET), mostramos el formulario.
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Buscamos al usuario en la base de datos.
        usuario = User.query.filter_by(username=username).first()

        # Si el usuario existe y la contraseña es correcta...
        if usuario and check_password_hash(usuario.password_hash, password):
            # Guardamos sus datos en la sesión para que siga conectado.
            session['user_id'] = usuario.id
            session['username'] = usuario.username
            session['role'] = usuario.role  # Guardamos el rol en la sesión.
            flash('¡Has iniciado sesión correctamente!', 'success')
            return redirect(url_for('index'))
        else:
            # Si no, mostramos un error.
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cierra la sesión del usuario."""
    # Eliminamos los datos del usuario de la sesión.
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)  # Eliminamos el rol de la sesión.
    flash('Has cerrado la sesión.', 'info')
    return redirect(url_for('index'))

@app.route('/acerca')
def acerca():
    """Página 'Acerca de' con información del proyecto."""
    return render_template('acerca.html')

# --- Funciones Auxiliares ---

def archivo_permitido(nombre_archivo):
    """Comprueba si un archivo tiene una extensión permitida."""
    return '.' in nombre_archivo and \
           nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

@app.route('/subir', methods=['GET', 'POST'])
def subir():
    """Página para subir imágenes (solo para usuarios conectados)."""
    # Si el usuario no ha iniciado sesión, lo redirigimos al login.
    if 'user_id' not in session:
        flash('Debes iniciar sesión para subir una imagen.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Comprobamos si se envió un archivo.
        if 'archivo' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        archivo = request.files['archivo']

        # Si no se seleccionó un archivo, el navegador envía un archivo "vacío".
        if archivo.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        # Si el archivo existe y tiene una extensión permitida...
        if archivo and archivo_permitido(archivo.filename):
            # Hacemos el nombre del archivo seguro para evitar problemas.
            nombre_seguro = secure_filename(archivo.filename)
            
            # Creamos la carpeta de subidas si no existe.
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Guardamos el archivo en el servidor.
            ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)
            archivo.save(ruta_completa)

            # Creamos un registro de la imagen en la base de datos.
            nueva_imagen = Image(filename=nombre_seguro, user_id=session['user_id'])
            db.session.add(nueva_imagen)
            db.session.commit()

            flash(f'¡Imagen "{nombre_seguro}" subida exitosamente!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Tipo de archivo no permitido.', 'error')
            return redirect(request.url)

    return render_template('subir.html')


# --- Rutas de Administrador ---

@app.route('/admin')
def admin_dashboard():
    """Panel de administración para aprobar o rechazar imágenes."""
    # Verificamos si el usuario es administrador.
    if 'role' not in session or session['role'] != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('index'))

    # Obtenemos todas las imágenes pendientes de aprobación.
    imagenes_pendientes = Image.query.filter_by(status='pending').order_by(Image.id.desc()).all()
    return render_template('admin.html', imagenes=imagenes_pendientes)

@app.route('/admin/approve/<int:image_id>')
def approve_image(image_id):
    """Ruta para aprobar una imagen."""
    if 'role' not in session or session['role'] != 'admin':
        flash('Acción no permitida.', 'danger')
        return redirect(url_for('index'))

    imagen = Image.query.get_or_404(image_id)
    imagen.status = 'approved'
    db.session.commit()
    flash(f'La imagen "{imagen.filename}" ha sido aprobada.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject/<int:image_id>')
def reject_image(image_id):
    """Ruta para rechazar una imagen."""
    if 'role' not in session or session['role'] != 'admin':
        flash('Acción no permitida.', 'danger')
        return redirect(url_for('index'))

    imagen = Image.query.get_or_404(image_id)
    imagen.status = 'rejected'
    db.session.commit()
    flash(f'La imagen "{imagen.filename}" ha sido rechazada.', 'warning')
    return redirect(url_for('admin_dashboard'))


# --- Bloque de Ejecución Principal ---
# Este código solo se ejecuta si corremos el archivo directamente (ej: python app.py).
if __name__ == '__main__':
    # El modo de depuración se activa solo si la variable de entorno FLASK_ENV es 'development'
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, port=5001)

