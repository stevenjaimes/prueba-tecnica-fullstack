from typing import Dict, List, Optional, Any
from sqlalchemy import func
from app.domain.entities.vuelo import Vuelo
from app.domain.entities.aerolinea import Aerolinea
from app.domain.entities.aeropuerto import Aeropuerto
from app.infrastructure.database.utils import get_or_404, commit_or_rollback
from app.infrastructure.database.connection import db
from datetime import date

class VueloRepository:
    """Repositorio para operaciones de base de datos relacionadas con vuelos."""

    @classmethod
    def obtener_todos(cls) -> List[Vuelo]:
        """Obtiene todos los vuelos registrados en el sistema.
        
        Returns:
            List[Vuelo]: Lista de instancias de Vuelo
        """
        return Vuelo.query.all()

    @classmethod
    def obtener_por_id(cls, id_vuelo: int) -> Vuelo:
        """Obtiene un vuelo específico por su ID.
        
        Args:
            id_vuelo (int): ID del vuelo a buscar
            
        Returns:
            Vuelo: Instancia del vuelo encontrado
            
        Raises:
            NotFoundError: Si el vuelo no existe
        """
        return get_or_404(Vuelo, id_vuelo)

    @classmethod
    def crear(cls, datos: Dict[str, Any]) -> Vuelo:
        """Crea un nuevo vuelo con los datos proporcionados.
        
        Args:
            datos (Dict[str, Any]): Diccionario con los datos del vuelo
            
        Returns:
            Vuelo: Instancia del vuelo creado
            
        Raises:
            SQLAlchemyError: Si ocurre un error al guardar en la base de datos
        """
        vuelo = Vuelo(**datos)
        db.session.add(vuelo)
        commit_or_rollback()
        return vuelo

    @classmethod
    def actualizar(cls, id_vuelo: int, datos: Dict[str, Any]) -> Vuelo:
        """Actualiza un vuelo existente.
        
        Args:
            id_vuelo (int): ID del vuelo a actualizar
            datos (Dict[str, Any]): Diccionario con los datos a actualizar
            
        Returns:
            Vuelo: Instancia del vuelo actualizado
            
        Raises:
            NotFoundError: Si el vuelo no existe
            SQLAlchemyError: Si ocurre un error al actualizar
        """
        vuelo = cls.obtener_por_id(id_vuelo)
        for key, value in datos.items():
            setattr(vuelo, key, value)
        commit_or_rollback()
        return vuelo

    @classmethod
    def eliminar(cls, id_vuelo: int) -> None:
        """Elimina un vuelo existente.
        
        Args:
            id_vuelo (int): ID del vuelo a eliminar
            
        Raises:
            NotFoundError: Si el vuelo no existe
            SQLAlchemyError: Si ocurre un error al eliminar
        """
        vuelo = cls.obtener_por_id(id_vuelo)
        db.session.delete(vuelo)
        commit_or_rollback()

    @classmethod
    def obtener_metricas(cls) -> Dict[str, Any]:
        """Obtiene métricas consolidados sobre los vuelos.
        
        Returns:
            Dict[str, Any]: Diccionario con:
                - aeropuerto_mas_ocupado: Lista de aeropuertos con más movimiento
                - aerolinea_mas_ocupada: Lista de aerolíneas con más vuelos
                - dia_mas_ocupado: Lista de días con más vuelos
                - aerolineas_mas_de_dos_vuelos: Aerolíneas con >2 vuelos en un día
        """
        return {
            'aeropuerto_mas_ocupado': cls._aeropuerto_mas_ocupado(),
            'aerolinea_mas_ocupada': cls._aerolinea_mas_ocupada(),
            'dia_mas_ocupado': cls._dia_mas_ocupado(),
            'aerolineas_mas_de_dos_vuelos': cls._aerolineas_mas_de_dos_vuelos()
        }

    @classmethod
    def _aeropuerto_mas_ocupado(cls) -> List[Dict[str, Any]]:
        """Obtiene los aeropuertos con mayor número de movimientos.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con:
                - id_aeropuerto: ID del aeropuerto
                - nombre_aeropuerto: Nombre del aeropuerto
                - total_movimientos: Número total de movimientos
        """
        max_movimientos = db.session.query(
            func.count(Vuelo.id).label('total')
        ).group_by(Vuelo.id_aeropuerto).order_by(
            func.count(Vuelo.id).desc()
        ).first()

        if not max_movimientos:
            return []

        resultados = (
            db.session.query(
                Vuelo.id_aeropuerto,
                Aeropuerto.nombre_aeropuerto,
                func.count(Vuelo.id).label('total_movimientos')
            )
            .join(Aeropuerto, Aeropuerto.id_aeropuerto == Vuelo.id_aeropuerto)
            .group_by(Vuelo.id_aeropuerto, Aeropuerto.nombre_aeropuerto)
            .having(func.count(Vuelo.id) == max_movimientos[0])
            .all()
        )

        return [{
            'id_aeropuerto': r.id_aeropuerto,
            'nombre_aeropuerto': r.nombre_aeropuerto,
            'total_movimientos': r.total_movimientos
        } for r in resultados]

    @classmethod
    def _aerolinea_mas_ocupada(cls) -> List[Dict[str, Any]]:
        """Obtiene las aerolíneas con mayor número de vuelos.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con:
                - id_aerolinea: ID de la aerolínea
                - nombre_aerolinea: Nombre de la aerolínea
                - total_vuelos: Número total de vuelos
        """
        max_vuelos = db.session.query(
            func.count(Vuelo.id).label('total')
        ).group_by(Vuelo.id_aerolinea).order_by(
            func.count(Vuelo.id).desc()
        ).first()

        if not max_vuelos:
            return []

        resultados = (
            db.session.query(
                Vuelo.id_aerolinea,
                Aerolinea.nombre_aerolinea,
                func.count(Vuelo.id).label('total_vuelos')
            )
            .join(Aerolinea, Aerolinea.id_aerolinea == Vuelo.id_aerolinea)
            .group_by(Vuelo.id_aerolinea, Aerolinea.nombre_aerolinea)
            .having(func.count(Vuelo.id) == max_vuelos[0])
            .all()
        )

        return [{
            'id_aerolinea': r.id_aerolinea,
            'nombre_aerolinea': r.nombre_aerolinea,
            'total_vuelos': r.total_vuelos
        } for r in resultados]

    @classmethod
    def _dia_mas_ocupado(cls) -> List[Dict[str, Any]]:
        """Obtiene los días con mayor número de vuelos.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con:
                - dia: Fecha en formato YYYY-MM-DD
                - total_vuelos: Número total de vuelos
        """
        max_vuelos = db.session.query(
            func.count(Vuelo.id).label('total')
        ).group_by(Vuelo.dia).order_by(
            func.count(Vuelo.id).desc()
        ).first()

        if not max_vuelos:
            return []

        resultados = (
            db.session.query(
                Vuelo.dia,
                func.count(Vuelo.id).label('total_vuelos')
            )
            .group_by(Vuelo.dia)
            .having(func.count(Vuelo.id) == max_vuelos[0])
            .all()
        )

        return [{
            'dia': r.dia.strftime('%Y-%m-%d'),
            'total_vuelos': r.total_vuelos
        } for r in resultados]

    @classmethod
    def _aerolineas_mas_de_dos_vuelos(cls) -> List[Dict[str, Any]]:
        """Obtiene aerolíneas con más de 2 vuelos en un mismo día.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con:
                - id_aerolinea: ID de la aerolínea
                - nombre_aerolinea: Nombre de la aerolínea
                - dia: Fecha en formato YYYY-MM-DD
                - total_vuelos: Número total de vuelos
        """
        vuelos_por_dia = (
            db.session.query(
                Vuelo.id_aerolinea,
                Aerolinea.nombre_aerolinea,
                Vuelo.dia,
                func.count().label('total')
            )
            .join(Aerolinea, Aerolinea.id_aerolinea == Vuelo.id_aerolinea)
            .group_by(Vuelo.id_aerolinea, Aerolinea.nombre_aerolinea, Vuelo.dia)
            .subquery()
        )

        resultados = (
            db.session.query(
                vuelos_por_dia.c.id_aerolinea,
                vuelos_por_dia.c.nombre_aerolinea,
                vuelos_por_dia.c.dia,
                vuelos_por_dia.c.total
            )
            .filter(vuelos_por_dia.c.total > 2)
            .all()
        )

        return [{
            'id_aerolinea': r.id_aerolinea,
            'nombre_aerolinea': r.nombre_aerolinea,
            'dia': r.dia.strftime('%Y-%m-%d'),
            'total_vuelos': r.total
        } for r in resultados]