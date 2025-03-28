from flask_restx import Namespace, Resource, fields
from app.domain.services.aeropuerto_service import AeropuertoService
from app.domain.repositories.aeropuerto_repository import AeropuertoRepository

ns = Namespace('aeropuertos', description='Operaciones con aeropuertos')

# Inicializar el servicio
aeropuerto_service = AeropuertoService(AeropuertoRepository())

aeropuerto_model = ns.model('Aeropuerto', {
    'id_aeropuerto': fields.Integer(readonly=True),
    'nombre_aeropuerto': fields.String(required=True)
})

@ns.route('/')
class AeropuertoList(Resource):
    @ns.doc('lista_aeropuertos')
    @ns.marshal_list_with(aeropuerto_model)
    def get(self):
        """Lista todos los aeropuertos"""
        return aeropuerto_service.obtener_todos()

    @ns.doc('create_aeropuerto')
    @ns.expect(aeropuerto_model)
    @ns.marshal_with(aeropuerto_model, code=201)
    def post(self):
        """Crea un nuevo aeropuerto"""
        return aeropuerto_service.crear_aeropuerto(ns.payload)

@ns.route('/mas_ocupado')
class AeropuertoMasOcupado(Resource):
    @ns.doc('get_busiest_airport')
    def get(self):
        """Obtiene el aeropuerto con más movimiento"""
        return aeropuerto_service.obtener_mas_ocupado()

@ns.route('/<int:id>')
@ns.response(404, 'Aeropuerto no encontrado')
@ns.param('id', 'ID del aeropuerto')
class AeropuertoDetail(Resource):
    @ns.doc('get_aeropuerto')
    @ns.marshal_with(aeropuerto_model)
    def get(self, id):
        """Obtiene un aeropuerto específico"""
        return aeropuerto_service.obtener_por_id(id)

@ns.route('/<int:id>/estadisticas')
@ns.response(404, 'Aeropuerto no encontrado')
@ns.param('id', 'ID del aeropuerto')
class AeropuertoEstadisticas(Resource):
    @ns.doc('get_airport_stats')
    def get(self, id):
        """Obtiene estadísticas detalladas del aeropuerto"""
        return aeropuerto_service.obtener_estadisticas(id)