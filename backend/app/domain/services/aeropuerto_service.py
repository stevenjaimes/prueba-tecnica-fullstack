from app.extensions import cache
from app.domain.repositories.aeropuerto_repository import AeropuertoRepository
from app.api.schemas.aeropuerto_schema import AeropuertoSchema
from marshmallow import ValidationError
import logging
from typing import Dict, List, Tuple, Optional, Union

class AeropuertoService:
    """Servicio para manejar operaciones relacionadas con aeropuertos."""
    
    def __init__(self, repository: AeropuertoRepository):
        """Inicializa el servicio con el repositorio inyectado.
        
        Args:
            repository (AeropuertoRepository): Repositorio para acceso a datos
        """
        self.repository = repository
        self.schema = AeropuertoSchema()
        self.schema_list = AeropuertoSchema(many=True)

    @cache.memoize(timeout=3600)
    def obtener_todos(self) -> List[Dict]:
        """Obtiene todos los aeropuertos con caché de 1 hora.
        
        Returns:
            List[Dict]: Lista de aeropuertos serializados
        """
        try:
            aeropuertos = self.repository.obtener_todos()
            return self.schema_list.dump(aeropuertos)
        except Exception as e:
            logging.error(f"Error al obtener aeropuertos: {str(e)}")
            return []

    def obtener_por_id(self, id_aeropuerto: int) -> Optional[Dict]:
        """Obtiene un aeropuerto por su ID.
        
        Args:
            id_aeropuerto (int): ID del aeropuerto
            
        Returns:
            Optional[Dict]: Datos del aeropuerto o None si no existe
        """
        try:
            aeropuerto = self.repository.obtener_por_id(id_aeropuerto)
            if not aeropuerto:
                return None
            return self.schema.dump(aeropuerto)
        except Exception as e:
            logging.error(f"Error al obtener aeropuerto {id_aeropuerto}: {str(e)}")
            return None

    def crear_aeropuerto(self, datos: Dict) -> Tuple[Union[Dict, str], int]:
        """Crea un nuevo aeropuerto.
        
        Args:
            datos (Dict): Datos del aeropuerto a crear
            
        Returns:
            Tuple: (Datos del aeropuerto o mensaje de error, código HTTP)
        """
        try:
            datos_validados = self.schema.load(datos)
            aeropuerto = self.repository.crear(datos_validados)
            return self.schema.dump(aeropuerto), 201
        except ValidationError as err:
            logging.warning(f"Validación fallida: {err.messages}")
            return {"error": "Datos inválidos", "detalles": err.messages}, 400
        except Exception as e:
            logging.error(f"Error al crear aeropuerto: {str(e)}")
            return {"error": "Error interno del servidor"}, 500

    def actualizar_aeropuerto(self, id_aeropuerto: int, datos: Dict) -> Tuple[Union[Dict, str], int]:
        """Actualiza un aeropuerto existente.
        
        Args:
            id_aeropuerto (int): ID del aeropuerto a actualizar
            datos (Dict): Datos a actualizar
            
        Returns:
            Tuple: (Datos actualizados o mensaje de error, código HTTP)
        """
        try:
            aeropuerto = self.repository.obtener_por_id(id_aeropuerto)
            if not aeropuerto:
                return {"error": "Aeropuerto no encontrado"}, 404
                
            datos_validados = self.schema.load(datos, partial=True)
            aeropuerto = self.repository.actualizar(aeropuerto, datos_validados)
            return self.schema.dump(aeropuerto), 200
        except ValidationError as err:
            logging.warning(f"Validación fallida: {err.messages}")
            return {"error": "Datos inválidos", "detalles": err.messages}, 400
        except Exception as e:
            logging.error(f"Error al actualizar aeropuerto {id_aeropuerto}: {str(e)}")
            return {"error": "Error interno del servidor"}, 500

    def eliminar_aeropuerto(self, id_aeropuerto: int) -> Tuple[None, int]:
        """Elimina un aeropuerto.
        
        Args:
            id_aeropuerto (int): ID del aeropuerto a eliminar
            
        Returns:
            Tuple: (None, código HTTP)
        """
        try:
            aeropuerto = self.repository.obtener_por_id(id_aeropuerto)
            if not aeropuerto:
                return {"error": "Aeropuerto no encontrado"}, 404
                
            self.repository.eliminar(aeropuerto)
            return None, 204
        except Exception as e:
            logging.error(f"Error al eliminar aeropuerto {id_aeropuerto}: {str(e)}")
            return {"error": "Error interno del servidor"}, 500

    @cache.memoize(timeout=3600)
    def obtener_mas_ocupado(self) -> Dict:
        """Obtiene el/los aeropuerto(s) más ocupado(s) con caché de 1 hora.
        
        Returns:
            Dict: Datos de aeropuertos más ocupados
        """
        try:
            aeropuertos, total = self.repository.obtener_mas_ocupado()
            return {
                'aeropuertos': [self.schema.dump(a) for a in aeropuertos],
                'hay_empate': len(aeropuertos) > 1,
                'total_movimientos': total
            }
        except Exception as e:
            logging.error(f"Error al obtener aeropuertos más ocupados: {str(e)}")
            return {"error": "Error al obtener estadísticas"}

    def obtener_estadisticas(self, id_aeropuerto: int) -> Dict:
        """Obtiene estadísticas detalladas de un aeropuerto.
        
        Args:
            id_aeropuerto (int): ID del aeropuerto
            
        Returns:
            Dict: Estadísticas del aeropuerto
        """
        try:
            aeropuerto = self.repository.obtener_por_id(id_aeropuerto)
            if not aeropuerto:
                return {"error": "Aeropuerto no encontrado"}, 404
                
            datos = self.repository.obtener_estadisticas(id_aeropuerto)
            return {
                'aeropuerto': self.schema.dump(datos['aeropuerto']),
                'movimientos': {m.descripcion: m.total for m in datos['movimientos']},
                'aerolineas': [
                    {
                        'aerolinea': self.schema.dump(a),
                        'total_vuelos': total
                    } 
                    for a, total in datos['aerolineas']
                ]
            }
        except Exception as e:
            logging.error(f"Error al obtener estadísticas del aeropuerto {id_aeropuerto}: {str(e)}")
            return {"error": "Error al obtener estadísticas"}, 500