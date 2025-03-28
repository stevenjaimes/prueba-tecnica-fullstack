from app.infrastructure.database.connection import db

class Aerolinea(db.Model):
    __tablename__ = 'aerolineas'
    id_aerolinea = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_aerolinea = db.Column(db.String(50), nullable=False)


