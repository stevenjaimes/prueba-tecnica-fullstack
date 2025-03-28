from app.infrastructure.database.connection import db

class Movimiento(db.Model):
    __tablename__ = 'movimientos'
    id_movimiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(50), nullable=False)   


