# app/domain/entities/models.py
from app.infrastructure.database.connection import db

class Aeropuerto(db.Model):
    __tablename__ = 'aeropuertos'
    id_aeropuerto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_aeropuerto = db.Column(db.String(50), nullable=False)


