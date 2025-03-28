from flask import Flask
from flask_cors import CORS 
from app.infrastructure.database.connection import init_db, db
from app.infrastructure.security.config import SecurityConfig
from .infrastructure.database.initial_data import DatabaseInitializer
from app.infrastructure.database.initializers import initialize_database
from flask_migrate import Migrate

def create_app() -> Flask:
    """Función fábrica para crear y configurar la aplicación Flask.
    
    Responsabilidades:
    1. Inicializa la aplicación Flask con configuraciones básicas
    2. Configura CORS, base de datos, caché y migraciones
    3. Registra los blueprints/rutas de la API
    4. Maneja la inicialización de la base de datos
    
    Retorna:
        Flask: Instancia de la aplicación Flask configurada
    """
    # 1. Creación de la instancia Flask
    app = Flask(__name__)

    # 2. Configuración de Seguridad y CORS
    # Habilita CORS (Cross-Origin Resource Sharing) para todos los dominios
    CORS(app)
    
    # Establece la clave secreta desde la configuración de seguridad
    app.config['SECRET_KEY'] = SecurityConfig.SECRET_KEY

    # 3. Configuración de Extensiones
    # Inicializa el sistema de caché
    from .extensions import cache
    cache.init_app(app)
    
    # Inicializa la conexión a la base de datos
    init_db(app)

    # 4. Inicialización Controlada de la Base de Datos
    # Carga datos iniciales si es necesario
    initialize_database(app)

    # Configura Flask-Migrate para manejar migraciones de la base de datos
    migrate = Migrate(app, db)

    # 5. Registro de Blueprints
    # Importa y registra las rutas de la API
    from .api.routes import bp as api_blueprint
    app.register_blueprint(api_blueprint)
    
    # 6. Creación de Tablas
    # Asegura que todas las tablas estén creadas en el contexto de la aplicación
    with app.app_context():
        db.create_all()

    return app
    

