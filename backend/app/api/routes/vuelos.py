from flask_restx import Namespace, Resource, fields
from app.domain.services.vuelo_service import VueloService
from app.domain.repositories.vuelo_repository import VueloRepository

ns = Namespace('vuelos', description='Operaciones relacionadas con vuelos')

# Inicializar el servicio
vuelo_service = VueloService(VueloRepository())

vuelo_model = ns.model('Vuelo', {
    'id': fields.Integer(readonly=True, description='ID del vuelo'),
    'id_aerolinea': fields.Integer(required=True, description='ID de la aerolínea'),
    'id_aeropuerto': fields.Integer(required=True, description='ID del aeropuerto'),
    'id_movimiento': fields.Integer(required=True, description='ID del movimiento (1: Salida, 2: Llegada)'),
    'dia': fields.Date(required=True, description='Fecha del vuelo (YYYY-MM-DD)')
})

metricas_model = ns.model('MetricasVuelos', {
    'aeropuerto_mas_ocupado': fields.Raw(description='Aeropuerto con más movimiento'),
    'aerolinea_mas_ocupada': fields.Raw(description='Aerolínea con más vuelos'),
    'dia_mas_ocupado': fields.Raw(description='Día con mayor número de vuelos'),
    'aerolineas_mas_de_dos_vuelos': fields.List(fields.Raw, description='Aerolíneas con más de 2 vuelos en un día')
})

@ns.route('/')
class VueloList(Resource):
    @ns.doc('list_vuelos')
    @ns.marshal_list_with(vuelo_model)
    def get(self):
        """Lista todos los vuelos"""
        return vuelo_service.obtener_todos()

    @ns.doc('create_vuelo')
    @ns.expect(vuelo_model)
    @ns.marshal_with(vuelo_model, code=201)
    def post(self):
        """Crea un nuevo registro de vuelo"""
        return vuelo_service.crear_vuelo(ns.payload)

@ns.route('/metricas')
class MetricasVuelos(Resource):
    @ns.doc('get_flight_metrics')
    @ns.marshal_with(metricas_model)
    def get(self):
        """Obtiene todas las métricas de vuelos"""
        return vuelo_service.obtener_metricas()

@ns.route('/<int:id>')
@ns.response(404, 'Vuelo no encontrado')
@ns.param('id', 'ID del vuelo')
class VueloResource(Resource):
    @ns.doc('get_vuelo')
    @ns.marshal_with(vuelo_model)
    def get(self, id):
        """Obtiene un vuelo específico"""
        return vuelo_service.obtener_por_id(id)

    @ns.doc('update_vuelo')
    @ns.expect(vuelo_model)
    @ns.marshal_with(vuelo_model)
    def put(self, id):
        """Actualiza un vuelo existente"""
        return vuelo_service.actualizar_vuelo(id, ns.payload)

    @ns.doc('delete_vuelo')
    @ns.response(204, 'Vuelo eliminado')
    def delete(self, id):
        """Elimina un vuelo"""
        return vuelo_service.eliminar_vuelo(id)

@ns.route('/aerolineas-mas-de-dos')
class AerolineasMasDeDosVuelos(Resource):
    @ns.doc('get_airlines_more_than_two_flights')
    def get(self):
        """Obtiene aerolíneas con más de 2 vuelos en un día"""
        return vuelo_service.obtener_aerolineas_mas_de_dos_vuelos()