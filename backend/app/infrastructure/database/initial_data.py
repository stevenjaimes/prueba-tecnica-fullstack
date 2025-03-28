from sqlalchemy import text
from datetime import datetime
from app.domain.entities.aerolinea import Aerolinea
from app.domain.entities.aeropuerto import Aeropuerto
from app.domain.entities.movimiento import Movimiento
from app.domain.entities.vuelo import Vuelo
from app.infrastructure.database.connection import db

class DatabaseInitializer:
    @staticmethod
    def should_initialize(db):
        """Verifica si la base de datos necesita inicialización"""
        return not db.session.execute(
            text("SELECT 1 FROM pg_tables WHERE tablename = 'aerolineas'")
        ).scalar()

    @staticmethod
    def initialize_data(db):
        """Ejecuta la inicialización de datos"""
        try:
            # Crear tablas si no existen
            db.create_all()

            # Datos iniciales (CORRECCIÓN: Añadidas comas después de cada elemento)
            initial_data = {
                'aerolineas': [
                    Aerolinea(id_aerolinea=1, nombre_aerolinea='Volaris'),
                    Aerolinea(id_aerolinea=2, nombre_aerolinea='Aeromar'),
                    Aerolinea(id_aerolinea=3, nombre_aerolinea='Interjet'),
                    Aerolinea(id_aerolinea=4, nombre_aerolinea='Aeromexico')
                ],  # <-- Coma añadida aquí
        
                'aeropuertos': [
                    Aeropuerto(id_aeropuerto=1, nombre_aeropuerto='Benito Juarez'),
                    Aeropuerto(id_aeropuerto=2, nombre_aeropuerto='Guanajuato'),
                    Aeropuerto(id_aeropuerto=3, nombre_aeropuerto='La paz'),
                    Aeropuerto(id_aeropuerto=4, nombre_aeropuerto='Oaxaca')
                ],  # <-- Coma añadida aquí
                
                'movimientos': [
                    Movimiento(id_movimiento=1, descripcion='Salida'),
                    Movimiento(id_movimiento=2, descripcion='Llegada')
                ],  # <-- Coma añadida aquí
                
                'vuelos': [
                    Vuelo(id_aerolinea=1, id_aeropuerto=1, id_movimiento=1, dia=datetime(2021, 5, 2)),
                    Vuelo(id_aerolinea=2, id_aeropuerto=1, id_movimiento=1, dia=datetime(2021, 5, 2)),
                    Vuelo(id_aerolinea=3, id_aeropuerto=2, id_movimiento=2, dia=datetime(2021, 5, 2)),
                    Vuelo(id_aerolinea=4, id_aeropuerto=3, id_movimiento=2, dia=datetime(2021, 5, 2)),
                    Vuelo(id_aerolinea=1, id_aeropuerto=3, id_movimiento=2, dia=datetime(2021, 5, 2)),
                    Vuelo(id_aerolinea=2, id_aeropuerto=1, id_movimiento=1, dia=datetime(2021, 5, 2)),
                    Vuelo(id_aerolinea=2, id_aeropuerto=3, id_movimiento=1, dia=datetime(2021, 5, 4)),
                    Vuelo(id_aerolinea=3, id_aeropuerto=4, id_movimiento=1, dia=datetime(2021, 5, 4)),
                    Vuelo(id_aerolinea=3, id_aeropuerto=4, id_movimiento=1, dia=datetime(2021, 5, 4))
                ]
            }

            for model_data in initial_data.values():
                db.session.add_all(model_data)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e