from typing import Dict, List, Tuple, Any, Optional
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.domain.entities.aeropuerto import Aeropuerto
from app.domain.entities.vuelo import Vuelo
from app.domain.entities.movimiento import Movimiento
from app.domain.entities.aerolinea import Aerolinea
from app.infrastructure.database.utils import get_or_404, commit_or_rollback
from app.infrastructure.database.connection import db

class AeropuertoRepository:
    """Repositorio para operaciones de base de datos relacionadas con aeropuertos."""

    @classmethod
    def obtener_todos(cls) -> List[Aeropuerto]:
        """Obtiene todos los aeropuertos registrados en el sistema.
        
        Returns:
            List[Aeropuerto]: Lista de instancias de Aeropuerto
        """
        return Aeropuerto.query.all()

    @classmethod
    def obtener_por_id(cls, id_aeropuerto: int) -> Aeropuerto:
        """Obtiene un aeropuerto específico por su ID.
        
        Args:
            id_aeropuerto (int): ID del aeropuerto a buscar
            
        Returns:
            Aeropuerto: Instancia del aeropuerto encontrado
            
        Raises:
            HTTPException 404: Si el aeropuerto no existe
        """
        return get_or_404(Aeropuerto, id_aeropuerto)

    @classmethod
    def crear(cls, datos: Dict[str, Any]) -> Aeropuerto:
        """Crea un nuevo aeropuerto con los datos proporcionados.
        
        Args:
            datos (Dict[str, Any]): Diccionario con los datos del aeropuerto
            
        Returns:
            Aeropuerto: Instancia del aeropuerto creado
            
        Raises:
            SQLAlchemyError: Si ocurre un error al guardar en la base de datos
        """
        aeropuerto = Aeropuerto(**datos)
        db.session.add(aeropuerto)
        commit_or_rollback()
        return aeropuerto

    @classmethod
    def actualizar(cls, aeropuerto: Aeropuerto, datos: Dict[str, Any]) -> Aeropuerto:
        """Actualiza un aeropuerto existente.
        
        Args:
            aeropuerto (Aeropuerto): Instancia del aeropuerto a actualizar
            datos (Dict[str, Any]): Diccionario con los datos a actualizar
            
        Returns:
            Aeropuerto: Instancia del aeropuerto actualizado
            
        Raises:
            SQLAlchemyError: Si ocurre un error al actualizar
        """
        for key, value in datos.items():
            setattr(aeropuerto, key, value)
        commit_or_rollback()
        return aeropuerto

    @classmethod
    def eliminar(cls, aeropuerto: Aeropuerto) -> None:
        """Elimina un aeropuerto existente.
        
        Args:
            aeropuerto (Aeropuerto): Instancia del aeropuerto a eliminar
            
        Raises:
            SQLAlchemyError: Si ocurre un error al eliminar
        """
        db.session.delete(aeropuerto)
        commit_or_rollback()

    @classmethod
    def obtener_mas_ocupado(cls) -> Tuple[List[Aeropuerto], int]:
        """Identifica el/los aeropuerto(s) con mayor número de movimientos.
        
        Returns:
            Tuple[List[Aeropuerto], int]: Tupla con:
                - Lista de aeropuertos más ocupados (puede haber empates)
                - Número total de movimientos del aeropuerto más ocupado
        """
        # Subconsulta para contar movimientos por aeropuerto
        subconsulta = (
            db.session.query(
                Vuelo.id_aeropuerto,
                func.count().label('total_movimientos')
            )
            .group_by(Vuelo.id_aeropuerto)
            .subquery()
        )

        # Obtiene el máximo número de movimientos
        max_movimientos = db.session.query(func.max(subconsulta.c.total_movimientos)).scalar()

        # Consulta para aeropuertos con ese máximo de movimientos
        aeropuertos_ocupados = (
            db.session.query(Aeropuerto)
            .join(subconsulta, Aeropuerto.id_aeropuerto == subconsulta.c.id_aeropuerto)
            .filter(subconsulta.c.total_movimientos == max_movimientos)
            .all()
        )

        return aeropuertos_ocupados, max_movimientos

    @classmethod
    def obtener_estadisticas(cls, id_aeropuerto: int) -> Dict[str, Any]:
        """Obtiene estadísticas detalladas de un aeropuerto específico.
        
        Args:
            id_aeropuerto (int): ID del aeropuerto a consultar
            
        Returns:
            Dict[str, Any]: Diccionario con:
                - aeropuerto: Datos del aeropuerto
                - movimientos: Lista de movimientos con conteo de vuelos
                - aerolineas: Lista de aerolíneas con conteo de vuelos
                
        Raises:
            HTTPException 404: Si el aeropuerto no existe
            SQLAlchemyError: Si ocurre un error en la consulta
        """
        aeropuerto = cls.obtener_por_id(id_aeropuerto)
        
        # Consulta para movimientos y conteo de vuelos
        movimientos = (
            db.session.query(
                Movimiento.descripcion,
                func.count(Vuelo.id).label('total')
            )
            .join(Vuelo, Vuelo.id_movimiento == Movimiento.id_movimiento)
            .filter(Vuelo.id_aeropuerto == id_aeropuerto)
            .group_by(Movimiento.descripcion)
            .all()
        )
        
        # Consulta para aerolíneas y conteo de vuelos
        aerolineas = (
            db.session.query(
                Aerolinea,
                func.count(Vuelo.id).label('total_vuelos')
            )
            .join(Vuelo, Vuelo.id_aerolinea == Aerolinea.id_aerolinea)
            .filter(Vuelo.id_aeropuerto == id_aeropuerto)
            .group_by(Aerolinea.id_aerolinea)
            .order_by(func.count(Vuelo.id).desc())
            .all()
        )
        
        return {
            'aeropuerto': aeropuerto,
            'movimientos': movimientos,
            'aerolineas': aerolineas
        }