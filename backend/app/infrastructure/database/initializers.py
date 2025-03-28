from flask import Flask
from app.infrastructure.database.connection import db
from .initial_data import DatabaseInitializer

def initialize_database(app: Flask) -> None:
    """Inicializa la base de datos con datos por defecto si es necesario"""
    with app.app_context():
        if DatabaseInitializer.should_initialize(db):
            app.logger.info("⚡ Inicializando base de datos...")
            try:
                DatabaseInitializer.initialize_data(db)
                app.logger.info("✅ Datos iniciales cargados correctamente")
            except Exception as e:
                app.logger.error(f"❌ Error en inicialización: {str(e)}")                
        else:
            app.logger.info("🔍 Base de datos ya inicializada")