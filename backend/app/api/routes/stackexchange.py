from flask_restx import Namespace, Resource, reqparse
from app.domain.services.stackexchange_service import StackExchangeService

ns = Namespace('stackexchange', 
               description='Consumo de API StackExchange como proxy')

# Initializar el servicio
stackexchange_service = StackExchangeService()

parser = reqparse.RequestParser()
parser.add_argument('etiqueta', 
                   type=str, 
                   default='perl', 
                   help='Etiqueta de búsqueda (default: perl)',
                   location='args')

@ns.route('/stats')
class StackExchangeStats(Resource):
    @ns.doc('get_stackexchange_stats')
    @ns.expect(parser)
    def get(self):
        """
        Obtiene estadísticas de StackExchange:
        1. Número de respuestas contestadas/no contestadas
        2. Respuesta con mayor reputación
        3. Respuesta con menor número de vistas
        4. Respuesta más vieja y más actual
        """
        args = parser.parse_args()
        return stackexchange_service.obtener_estadisticas(args['etiqueta'])