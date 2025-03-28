from typing import Dict, List, Tuple, Any
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.domain.entities.aerolinea import Aerolinea
from app.domain.entities.vuelo import Vuelo
from app.infrastructure.database.connection import db
from app.infrastructure.database.utils import get_or_404, commit_or_rollback

class AerolineaRepository:
    """Repositorio para operaciones de base de datos relacionadas con aerolíneas."""

    @classmethod
    def obtener_todas(cls) -> List[Aerolinea]:
        """Obtiene todas las aerolíneas registradas en el sistema.
        
        Returns:
            List[Aerolinea]: Lista de instancias de Aerolinea
        """
        return Aerolinea.query.all()

    @classmethod
    def obtener_por_id(cls, id_aerolinea: int) -> Aerolinea:
        """Obtiene una aerolínea específica por su ID.
        
        Args:
            id_aerolinea (int): ID de la aerolínea a buscar
            
        Returns:
            Aerolinea: Instancia de la aerolínea encontrada
            
        Raises:
            HTTPException 404: Si la aerolínea no existe
        """
        return get_or_404(Aerolinea, id_aerolinea)

    @classmethod
    def crear(cls, datos: Dict[str, Any]) -> Aerolinea:
        """Crea una nueva aerolínea con los datos proporcionados.
        
        Args:
            datos (Dict[str, Any]): Diccionario con los datos de la aerolínea
            
        Returns:
            Aerolinea: Instancia de la aerolínea creada
            
        Raises:
            SQLAlchemyError: Si ocurre un error al guardar en la base de datos
        """
        aerolinea = Aerolinea(**datos)
        db.session.add(aerolinea)
        commit_or_rollback()
        return aerolinea

    @classmethod
    def actualizar(cls, aerolinea: Aerolinea, datos: Dict[str, Any]) -> Aerolinea:
        """Actualiza una aerolínea existente.
        
        Args:
            aerolinea (Aerolinea): Instancia de la aerolínea a actualizar
            datos (Dict[str, Any]): Diccionario con los datos a actualizar
            
        Returns:
            Aerolinea: Instancia de la aerolínea actualizada
            
        Raises:
            SQLAlchemyError: Si ocurre un error al actualizar
        """
        for key, value in datos.items():
            setattr(aerolinea, key, value)
        commit_or_rollback()
        return aerolinea

    @classmethod
    def eliminar(cls, aerolinea: Aerolinea) -> None:
        """Elimina una aerolínea existente.
        
        Args:
            aerolinea (Aerolinea): Instancia de la aerolínea a eliminar
            
        Raises:
            SQLAlchemyError: Si ocurre un error al eliminar
        """
        db.session.delete(aerolinea)
        commit_or_rollback()

    @classmethod
    def obtener_estadisticas(cls, id_aerolinea: int) -> Dict[str, Any]:
        """Obtiene estadísticas detalladas de una aerolínea.
        
        Args:
            id_aerolinea (int): ID de la aerolínea a consultar
            
        Returns:
            Dict[str, Any]: Diccionario con:
                - aerolinea: Datos de la aerolínea
                - total_vuelos: Número total de vuelos
                - vuelos_por_movimiento: Lista de vuelos agrupados por tipo de movimiento
                - aeropuertos_frecuentes: Top 5 aeropuertos más frecuentados
                
        Raises:
            HTTPException 404: Si la aerolínea no existe
            SQLAlchemyError: Si ocurre un error en la consulta
        """
        aerolinea = cls.obtener_por_id(id_aerolinea)
        
        # Consulta para el total de vuelos
        total_vuelos = db.session.query(func.count(Vuelo.id))\
            .filter(Vuelo.id_aerolinea == id_aerolinea)\
            .scalar()

        # Consulta para vuelos por tipo de movimiento
        vuelos_por_movimiento = db.session.query(
            Vuelo.id_movimiento,
            func.count(Vuelo.id).label('total')
        ).filter(Vuelo.id_aerolinea == id_aerolinea)\
         .group_by(Vuelo.id_movimiento)\
         .all()

        # Consulta para aeropuertos más frecuentados (top 5)
        aeropuertos_frecuentes = db.session.query(
            Vuelo.id_aeropuerto,
            func.count(Vuelo.id).label('total_vuelos')
        ).filter(Vuelo.id_aerolinea == id_aerolinea)\
         .group_by(Vuelo.id_aeropuerto)\
         .order_by(func.count(Vuelo.id).desc())\
         .limit(5)\
         .all()

        return {
            'aerolinea': aerolinea,
            'total_vuelos': total_vuelos,
            'vuelos_por_movimiento': vuelos_por_movimiento,
            'aeropuertos_frecuentes': aeropuertos_frecuentes
        }