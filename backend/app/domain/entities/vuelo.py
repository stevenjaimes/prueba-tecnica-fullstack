from app.infrastructure.database.connection import db
class Vuelo(db.Model):
    __tablename__ = 'vuelos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aerolinea = db.Column(db.Integer, db.ForeignKey('aerolineas.id_aerolinea'))
    id_aeropuerto = db.Column(db.Integer, db.ForeignKey('aeropuertos.id_aeropuerto'))
    id_movimiento = db.Column(db.Integer, db.ForeignKey('movimientos.id_movimiento'))
    dia = db.Column(db.Date, nullable=False)


