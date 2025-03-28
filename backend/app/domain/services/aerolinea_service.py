from app.domain.repositories.aerolinea_repository import AerolineaRepository
from app.extensions import cache
from app.api.schemas.aerolinea_schema import AerolineaSchema
from marshmallow import ValidationError
import logging
from typing import List, Dict

class AerolineaService:
    """Servicio para manejar la lógica de negocio relacionada con aerolíneas."""
    
    def __init__(self, repository: AerolineaRepository):
        """Inicializa el servicio con el repositorio y esquemas necesarios.
        
        Args:
            repository (AerolineaRepository): Repositorio para acceder a datos de aerolíneas
        """
        self.repository = repository
        self.schema = AerolineaSchema()
        self.schema_list = AerolineaSchema(many=True)

    @cache.memoize(timeout=3600)
    def obtener_todas(self) -> List[Dict]:
        """Obtiene todas las aerolíneas con caché de 1 hora.
        
        Returns:
            list: Lista de aerolíneas serializadas
        """
        try:
            aerolineas = self.repository.obtener_todas()
            return self.schema_list.dump(aerolineas)
        except Exception as e:
            logging.error(f"Error al obtener aerolíneas: {str(e)}")
            return []

    def obtener_por_id(self, id_aerolinea: int) -> dict:
        """Obtiene una aerolínea específica por su ID.
        
        Args:
            id_aerolinea (int): ID de la aerolínea a buscar
            
        Returns:
            dict: Aerolínea serializada o None si no existe
        """
        try:
            aerolinea = self.repository.obtener_por_id(id_aerolinea)
            if not aerolinea:
                return None
            return self.schema.dump(aerolinea)
        except Exception as e:
            logging.error(f"Error al obtener aerolínea {id_aerolinea}: {str(e)}")
            return None

    def crear_aerolinea(self, datos: dict) -> tuple:
        """Crea una nueva aerolínea con los datos proporcionados.
        
        Args:
            datos (dict): Datos de la aerolínea a crear
            
        Returns:
            tuple: (dict, int) Datos de la aerolínea creada y código HTTP
        """
        try:
            datos_validados = self.schema.load(datos)
            aerolinea = self.repository.crear(datos_validados)
            return self.schema.dump(aerolinea), 201
        except ValidationError as err:
            logging.warning(f"Validación fallida al crear aerolínea: {err.messages}")
            return {"error": "Datos inválidos", "detalles": err.messages}, 400
        except Exception as e:
            logging.error(f"Error al crear aerolínea: {str(e)}")
            return {"error": "Error interno al crear aerolínea"}, 500

    def actualizar_aerolinea(self, id_aerolinea: int, datos: dict) -> tuple:
        """Actualiza una aerolínea existente.
        
        Args:
            id_aerolinea (int): ID de la aerolínea a actualizar
            datos (dict): Datos a actualizar
            
        Returns:
            tuple: (dict, int) Datos actualizados y código HTTP
        """
        try:
            aerolinea = self.repository.obtener_por_id(id_aerolinea)
            if not aerolinea:
                return {"error": "Aerolínea no encontrada"}, 404
                
            datos_validados = self.schema.load(datos, partial=True)
            aerolinea_actualizada = self.repository.actualizar(aerolinea, datos_validados)
            return self.schema.dump(aerolinea_actualizada), 200
        except ValidationError as err:
            logging.warning(f"Validación fallida al actualizar aerolínea {id_aerolinea}: {err.messages}")
            return {"error": "Datos inválidos", "detalles": err.messages}, 400
        except Exception as e:
            logging.error(f"Error al actualizar aerolínea {id_aerolinea}: {str(e)}")
            return {"error": "Error interno al actualizar aerolínea"}, 500

    def eliminar_aerolinea(self, id_aerolinea: int) -> tuple:
        """Elimina una aerolínea existente.
        
        Args:
            id_aerolinea (int): ID de la aerolínea a eliminar
            
        Returns:
            tuple: (None, int) Código HTTP de respuesta
        """
        try:
            aerolinea = self.repository.obtener_por_id(id_aerolinea)
            if not aerolinea:
                return {"error": "Aerolínea no encontrada"}, 404
                
            self.repository.eliminar(aerolinea)
            return None, 204
        except Exception as e:
            logging.error(f"Error al eliminar aerolínea {id_aerolinea}: {str(e)}")
            return {"error": "Error interno al eliminar aerolínea"}, 500

    @cache.memoize(timeout=3600)
    def obtener_estadisticas(self, id_aerolinea: int) -> dict:
        """Obtiene estadísticas de una aerolínea con caché de 1 hora.
        
        Args:
            id_aerolinea (int): ID de la aerolínea
            
        Returns:
            dict: Estadísticas de la aerolínea
        """
        try:
            aerolinea = self.repository.obtener_por_id(id_aerolinea)
            if not aerolinea:
                return {"error": "Aerolínea no encontrada"}, 404
                
            datos = self.repository.obtener_estadisticas(id_aerolinea)
            return {
                'aerolinea': self.schema.dump(datos['aerolinea']),
                'total_vuelos': datos['total_vuelos'],
                'vuelos_por_movimiento': [
                    {'id_movimiento': m.id_movimiento, 'total': m.total} 
                    for m in datos['vuelos_por_movimiento']
                ],
                'aeropuertos_frecuentes': [
                    {'id_aeropuerto': a.id_aeropuerto, 'total_vuelos': a.total_vuelos}
                    for a in datos['aeropuertos_frecuentes']
                ]
            }
        except Exception as e:
            logging.error(f"Error al obtener estadísticas de aerolínea {id_aerolinea}: {str(e)}")
            return {"error": "Error al obtener estadísticas"}, 500