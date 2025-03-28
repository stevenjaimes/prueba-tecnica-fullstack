from flask_restx import Namespace, Resource, fields
from app.domain.services.aerolinea_service import AerolineaService
from app.domain.repositories.aerolinea_repository import AerolineaRepository

ns = Namespace('aerolineas', description='Operaciones con aerolíneas')
# Inicializar el servicio
aerolinea_service = AerolineaService(AerolineaRepository())

aerolinea_model = ns.model('Aerolinea', {
    'id_aerolinea': fields.Integer(readonly=True),
    'nombre_aerolinea': fields.String(required=True)
})

estadisticas_model = ns.model('EstadisticasAerolinea', {
    'aerolinea': fields.Nested(aerolinea_model),
    'total_vuelos': fields.Integer,
    'vuelos_por_movimiento': fields.List(fields.Nested(ns.model('VuelosPorMovimiento', {
        'id_movimiento': fields.Integer,
        'total': fields.Integer
    }))),
    'aeropuertos_frecuentes': fields.List(fields.Nested(ns.model('AeropuertoFrecuente', {
        'id_aeropuerto': fields.Integer,
        'total_vuelos': fields.Integer
    })))
})

@ns.route('/')
class AerolineaList(Resource):
    @ns.doc('list_aerolineas')
    @ns.marshal_list_with(aerolinea_model)
    def get(self):
        """Lista todas las aerolíneas"""
        return aerolinea_service.obtener_todas()

    @ns.doc('create_aerolinea')
    @ns.expect(aerolinea_model)
    @ns.marshal_with(aerolinea_model, code=201)
    def post(self):
        """Crea una nueva aerolínea"""
        return aerolinea_service.crear_aerolinea(ns.payload)

@ns.route('/<int:id>')
@ns.response(404, 'Aerolínea no encontrada')
@ns.param('id', 'ID de la aerolínea')
class AerolineaResource(Resource):
    @ns.doc('get_aerolinea')
    @ns.marshal_with(aerolinea_model)
    def get(self, id):
        """Obtiene una aerolínea específica"""
        return aerolinea_service.obtener_por_id(id)

    @ns.doc('update_aerolinea')
    @ns.expect(aerolinea_model)
    @ns.marshal_with(aerolinea_model)
    def put(self, id):
        """Actualiza una aerolínea existente"""
        return aerolinea_service.actualizar_aerolinea(id, ns.payload)

    @ns.doc('delete_aerolinea')
    @ns.response(204, 'Aerolínea eliminada')
    def delete(self, id):
        """Elimina una aerolínea"""
        return aerolinea_service.eliminar_aerolinea(id)

@ns.route('/<int:id>/estadisticas')
@ns.response(404, 'Aerolínea no encontrada')
@ns.param('id', 'ID de la aerolínea')
class AerolineaEstadisticas(Resource):
    @ns.doc('get_airline_stats')
    @ns.marshal_with(estadisticas_model)
    def get(self, id):
        """Obtiene estadísticas de una aerolínea"""
        return aerolinea_service.obtener_estadisticas(id)