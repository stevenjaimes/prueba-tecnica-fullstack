from flask_sqlalchemy import SQLAlchemy
from .config import DBConfig

db = SQLAlchemy()

def init_db(app):
    """Inicializa la conexión a la base de datos"""
    app.config.from_object(DBConfig)
    db.init_app(app)