from flask_restx import Namespace, Resource, fields
from app.domain.services.movimiento_service import MovimientoService
from app.domain.repositories.movimiento_repository import MovimientoRepository

ns = Namespace('movimientos', description='Operaciones con movimientos de vuelos')

# Inicializar el servicio
movimiento_service = MovimientoService(MovimientoRepository())

movimiento_model = ns.model('Movimiento', {
    'id_movimiento': fields.Integer(readonly=True),
    'descripcion': fields.String(required=True)
})

vuelo_movimiento_model = ns.model('VueloMovimiento', {
    'id': fields.Integer(),
    'id_aerolinea': fields.Integer(),
    'nombre_aerolinea': fields.String(),
    'id_aeropuerto': fields.Integer(),
    'nombre_aeropuerto': fields.String(),
    'dia': fields.Date(),
    'id_movimiento': fields.Integer()
})

estadisticas_model = ns.model('EstadisticaMovimiento', {
    'id_movimiento': fields.Integer(),
    'descripcion': fields.String(),
    'total_vuelos': fields.Integer(),
    'aerolineas_top': fields.List(fields.Nested(ns.model('AerolineaTop', {
        'id_aerolinea': fields.Integer,
        'nombre_aerolinea': fields.String,
        'total_vuelos': fields.Integer
    }))),
    'aeropuertos_top': fields.List(fields.Nested(ns.model('AeropuertoTop', {
        'id_aeropuerto': fields.Integer,
        'nombre_aeropuerto': fields.String,
        'total_vuelos': fields.Integer
    })))
})

estadisticas_generales_model = ns.model('EstadisticasGeneralesMovimientos', {
    'estadisticas_basicas': fields.List(fields.Nested(estadisticas_model)),
    'total_general': fields.Integer()
})

vuelos_por_movimiento_model = ns.model('VuelosPorMovimiento', {
    'movimiento': fields.Nested(movimiento_model),
    'total_vuelos': fields.Integer(),
    'vuelos': fields.List(fields.Nested(vuelo_movimiento_model))
})

@ns.route('/')
class MovimientoList(Resource):
    @ns.doc('list_movimientos')
    @ns.marshal_list_with(movimiento_model)
    def get(self):
        """Lista todos los tipos de movimiento"""
        return movimiento_service.obtener_todos()

    @ns.doc('create_movimiento')
    @ns.expect(movimiento_model)
    @ns.marshal_with(movimiento_model, code=201)
    def post(self):
        """Crea un nuevo tipo de movimiento"""
        return movimiento_service.crear_movimiento(ns.payload)

@ns.route('/estadisticas')
class MovimientoEstadisticas(Resource):
    @ns.doc('get_movements_stats')
    @ns.marshal_with(estadisticas_generales_model)
    def get(self):
        """Obtiene estadísticas de movimientos"""
        return movimiento_service.obtener_estadisticas()

@ns.route('/<int:id>')
@ns.response(404, 'Movimiento no encontrado')
@ns.param('id', 'ID del movimiento')
class MovimientoDetail(Resource):
    @ns.doc('get_movimiento')
    @ns.marshal_with(movimiento_model)
    def get(self, id):
        """Obtiene un movimiento específico"""
        return movimiento_service.obtener_por_id(id)

@ns.route('/<int:id>/vuelos')
@ns.response(404, 'Movimiento no encontrado')
@ns.param('id', 'ID del movimiento')
class MovimientoVuelos(Resource):
    @ns.doc('get_movement_flights')
    @ns.marshal_with(vuelos_por_movimiento_model)
    def get(self, id):
        """Obtiene vuelos por tipo de movimiento"""
        return movimiento_service.obtener_vuelos_por_movimiento(id)