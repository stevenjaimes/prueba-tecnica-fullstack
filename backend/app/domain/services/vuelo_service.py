from typing import List, Dict, Tuple, Optional, Any
from datetime import date
from app.extensions import cache
from app.domain.repositories.vuelo_repository import VueloRepository
from app.api.schemas.vuelo_schema import VueloSchema
from flask import jsonify
import logging
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

class VueloService:
    def __init__(self, repository: VueloRepository) -> None:
        """Inicializa el servicio de vuelos con el repositorio y esquemas necesarios.
        
        Args:
            repository (VueloRepository): Instancia del repositorio de vuelos
        """
        self.repository = repository
        self.schema = VueloSchema()
        self.schema_list = VueloSchema(many=True)

    def obtener_todos(self) -> List[Dict[str, Any]]:
        """Obtiene todos los vuelos disponibles.
        
        Returns:
            List[Dict[str, Any]]: Lista de vuelos serializados
        """
        return self.schema_list.dump(self.repository.obtener_todos())

    def obtener_por_id(self, id_vuelo: int) -> Optional[Dict[str, Any]]:
        """Obtiene un vuelo específico por su ID con información relacionada.
        
        Args:
            id_vuelo (int): ID del vuelo a buscar
            
        Returns:
            Optional[Dict[str, Any]]: Vuelo serializado con información relacionada o None si no existe
        """
        try:
            vuelo, nombre_aerolinea, nombre_aeropuerto = self.repository.obtener_por_id(id_vuelo)
            return self.schema.dump({
                **vuelo.to_dict(),
                "aerolinea": {"nombre_aerolinea": nombre_aerolinea},
                "aeropuerto": {"nombre_aeropuerto": nombre_aeropuerto}
            })
        except Exception as e:
            logging.error(f"Error al obtener vuelo {id_vuelo}: {str(e)}")
            return None

    def crear_vuelo(self, datos: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Crea un nuevo vuelo con los datos proporcionados.
        
        Args:
            datos (Dict[str, Any]): Datos del vuelo a crear
            
        Returns:
            Tuple[Dict[str, Any], int]: Vuelo creado serializado y código HTTP
        """
        try:
            datos_validados = self.schema.load(datos)
            vuelo = self.repository.crear(datos_validados)
            return self.schema.dump(vuelo), 201
        except ValidationError as err:
            logging.warning(f"Error de validación al crear vuelo: {err.messages}")
            return {"error": "Datos inválidos", "detalles": err.messages}, 400
        except SQLAlchemyError as err:
            logging.error(f"Error de base de datos al crear vuelo: {str(err)}")
            return {"error": "Error al guardar el vuelo"}, 500

    def actualizar_vuelo(self, id_vuelo: int, datos: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        """Actualiza un vuelo existente.
        
        Args:
            id_vuelo (int): ID del vuelo a actualizar
            datos (Dict[str, Any]): Datos a actualizar
            
        Returns:
            Tuple[Dict[str, Any], int]: Vuelo actualizado serializado y código HTTP
        """
        try:
            datos_validados = self.schema.load(datos, partial=True)
            vuelo = self.repository.actualizar(id_vuelo, datos_validados)
            return self.schema.dump(vuelo), 200
        except ValidationError as err:
            logging.warning(f"Error de validación al actualizar vuelo {id_vuelo}: {err.messages}")
            return {"error": "Datos inválidos", "detalles": err.messages}, 400
        except SQLAlchemyError as err:
            logging.error(f"Error de base de datos al actualizar vuelo {id_vuelo}: {str(err)}")
            return {"error": "Error al actualizar el vuelo"}, 500

    def eliminar_vuelo(self, id_vuelo: int) -> Tuple[None, int]:
        """Elimina un vuelo existente.
        
        Args:
            id_vuelo (int): ID del vuelo a eliminar
            
        Returns:
            Tuple[None, int]: Código HTTP de respuesta
        """
        try:
            self.repository.eliminar(id_vuelo)
            return None, 204
        except SQLAlchemyError as err:
            logging.error(f"Error al eliminar vuelo {id_vuelo}: {str(err)}")
            return {"error": f"No se pudo eliminar el vuelo: {str(err)}"}, 500

    @cache.memoize(timeout=3600)
    def obtener_metricas(self) -> Dict[str, Any]:
        """Obtiene métricas de vuelos con caché de 1 hora.
        
        Returns:
            Dict[str, Any]: Métricas de vuelos
        """
        try:
            return self.repository.obtener_metricas()
        except Exception as e:
            logging.error(f"Error al obtener métricas de vuelos: {str(e)}")
            return {"error": "Error al obtener métricas"}

    def obtener_aerolineas_mas_de_dos_vuelos(self) -> Dict[str, Any]:
        """Obtiene aerolíneas con más de 2 vuelos en un mismo día.
        
        Returns:
            Dict[str, Any]: Información de aerolíneas
        """
        try:
            return self.repository._aerolineas_mas_de_dos_vuelos()
        except Exception as e:
            logging.error(f"Error al obtener aerolíneas frecuentes: {str(e)}")
            return {"error": "Error al obtener aerolíneas frecuentes"}