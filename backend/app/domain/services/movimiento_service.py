from typing import Dict, List, Any, Tuple
from app.extensions import cache
from app.domain.repositories.movimiento_repository import MovimientoRepository
from app.api.schemas.movimiento_schema import MovimientoSchema
from app.api.schemas.vuelo_schema import VueloSchema
from marshmallow import ValidationError
import logging

class MovimientoService:
    """Servicio para manejar la lógica de negocio relacionada con movimientos de vuelos."""

    def __init__(self, repository: MovimientoRepository):
        """Inicializa el servicio con las dependencias necesarias.
        
        Args:
            repository (MovimientoRepository): Repositorio para acceso a datos de movimientos
        """
        self.repository = repository
        self.schema = MovimientoSchema()  # Schema para un solo movimiento
        self.schema_list = MovimientoSchema(many=True)  # Schema para listas de movimientos
        self.vuelo_schema = VueloSchema()  # Schema para vuelos

    @cache.memoize(timeout=3600)
    def obtener_todos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los movimientos con caché de 1 hora.
        
        Returns:
            List[Dict[str, Any]]: Lista de movimientos serializados
        """
        try:
            movimientos = self.repository.obtener_todos()
            return self.schema_list.dump(movimientos)
        except Exception as e:
            logging.error(f"Error al obtener movimientos: {str(e)}")
            return []

    def obtener_por_id(self, id_movimiento: int) -> Dict[str, Any]:
        """Obtiene un movimiento específico por su ID.
        
        Args:
            id_movimiento (int): ID del movimiento a buscar
            
        Returns:
            Dict[str, Any]: Movimiento serializado
            
        Raises:
            NotFoundError: Si el movimiento no existe
        """
        try:
            movimiento = self.repository.obtener_por_id(id_movimiento)
            return self.schema.dump(movimiento)
        except Exception as e:
            logging.error(f"Error al obtener movimiento {id_movimiento}: {str(e)}")
            raise

    def crear_movimiento(self, datos: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Crea un nuevo movimiento con los datos proporcionados.
        
        Args:
            datos (Dict[str, Any]): Datos del movimiento a crear
            
        Returns:
            Tuple[Dict[str, Any], int]: Tupla con:
                - Dict: Movimiento creado serializado
                - int: Código HTTP (201 para creación exitosa)
                
        Raises:
            ValidationError: Si los datos no pasan la validación del schema
        """
        try:
            datos_validados = self.schema.load(datos)
            movimiento = self.repository.crear(datos_validados)
            return self.schema.dump(movimiento), 201
        except ValidationError as err:
            logging.warning(f"Error de validación al crear movimiento: {err.messages}")
            return {"error": "Datos inválidos", "detalles": err.messages}, 400
        except Exception as e:
            logging.error(f"Error al crear movimiento: {str(e)}")
            return {"error": "Error interno del servidor"}, 500

    @cache.memoize(timeout=3600)
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas detalladas de movimientos con caché de 1 hora.
        
        Returns:
            Dict[str, Any]: Diccionario con:
                - estadisticas_basicas: Lista de estadísticas por movimiento
                - total_general: Suma total de todos los vuelos
                
        Estructura de estadisticas_basicas:
            - id_movimiento: ID del movimiento
            - descripcion: Descripción del movimiento
            - total_vuelos: Total de vuelos para este movimiento
            - aerolineas_top: Top aerolíneas para este movimiento
            - aeropuertos_top: Top aeropuertos para este movimiento
        """
        try:
            datos = self.repository.obtener_estadisticas()
            return {
                'estadisticas_basicas': [
                    {
                        'id_movimiento': m.id_movimiento,
                        'descripcion': m.descripcion,
                        'total_vuelos': m.total_vuelos,
                        'aerolineas_top': [
                            {
                                'id_aerolinea': a.id_aerolinea,
                                'nombre_aerolinea': a.nombre_aerolinea,
                                'total_vuelos': a.total_vuelos
                            } for a in datos['aerolineas'].get(m.id_movimiento, [])
                        ],
                        'aeropuertos_top': [
                            {
                                'id_aeropuerto': a.id_aeropuerto,
                                'nombre_aeropuerto': a.nombre_aeropuerto,
                                'total_vuelos': a.total_vuelos
                            } for a in datos['aeropuertos'].get(m.id_movimiento, [])
                        ]
                    } for m in datos['estadisticas']
                ],
                'total_general': sum(m.total_vuelos for m in datos['estadisticas'])
            }
        except Exception as e:
            logging.error(f"Error al obtener estadísticas de movimientos: {str(e)}")
            return {"error": "Error al obtener estadísticas"}, 500

    def obtener_vuelos_por_movimiento(self, id_movimiento: int) -> Dict[str, Any]:
        """Obtiene todos los vuelos asociados a un movimiento específico.
        
        Args:
            id_movimiento (int): ID del movimiento a consultar
            
        Returns:
            Dict[str, Any]: Diccionario con:
                - movimiento: Datos del movimiento
                - total_vuelos: Cantidad total de vuelos
                - vuelos: Lista de vuelos con información extendida
                
        Estructura de cada vuelo:
            - Todos los campos del schema de vuelo
            - nombre_aerolinea: Nombre de la aerolínea
            - nombre_aeropuerto: Nombre del aeropuerto
        """
        try:
            datos = self.repository.obtener_vuelos_por_movimiento(id_movimiento)
            vuelos_procesados = []
            
            for vuelo, nombre_aerolinea, nombre_aeropuerto in datos['vuelos']:
                vuelo_data = self.vuelo_schema.dump(vuelo)
                vuelo_data.update({
                    'nombre_aerolinea': nombre_aerolinea,
                    'nombre_aeropuerto': nombre_aeropuerto
                })
                vuelos_procesados.append(vuelo_data)
            
            return {
                'movimiento': self.schema.dump(datos['movimiento']),
                'total_vuelos': len(vuelos_procesados),
                'vuelos': vuelos_procesados
            }
        except Exception as e:
            logging.error(f"Error al obtener vuelos por movimiento {id_movimiento}: {str(e)}")
            return {"error": "Error al obtener vuelos por movimiento"}, 500