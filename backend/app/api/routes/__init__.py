from flask_restx import Api
from flask import Blueprint
from flask_restx import Namespace, Resource

# Crear blueprint principal
bp = Blueprint('api', __name__, url_prefix='/api')

# Crear instancia API principal
api = Api(
    bp,
    title='Flight API',
    version='1.0',
    description='API para gestión de vuelos y Consulta de Stack Exchange',
    doc='/docs'
)

# Importar namespaces después de crear la instancia api

from .aerolineas import ns as aerolineas_ns
from .aeropuertos import ns as aeropuertos_ns
from .movimientos import ns as movimientos_ns
from .vuelos import ns as vuelos_ns
from .stackexchange import ns as stackexchange_ns

# Registrar namespaces

api.add_namespace(aerolineas_ns)
api.add_namespace(aeropuertos_ns)
api.add_namespace(movimientos_ns)
api.add_namespace(vuelos_ns)
api.add_namespace(stackexchange_ns)

