from typing import Dict, List, Tuple, Any
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.domain.entities.movimiento import Movimiento
from app.domain.entities.vuelo import Vuelo
from app.domain.entities.aerolinea import Aerolinea
from app.domain.entities.aeropuerto import Aeropuerto
from app.infrastructure.database.utils import get_or_404, commit_or_rollback
from app.infrastructure.database.connection import db

class MovimientoRepository:
    """Repositorio para operaciones de base de datos relacionadas con movimientos de vuelos."""

    @classmethod
    def obtener_todos(cls) -> List[Movimiento]:
        """Obtiene todos los movimientos registrados en el sistema.
        
        Returns:
            List[Movimiento]: Lista de todos los movimientos disponibles
        """
        return Movimiento.query.all()

    @classmethod
    def obtener_por_id(cls, id_movimiento: int) -> Movimiento:
        """Obtiene un movimiento específico por su ID.
        
        Args:
            id_movimiento (int): ID del movimiento a buscar
            
        Returns:
            Movimiento: Instancia del movimiento encontrado
            
        Raises:
            HTTPException 404: Si el movimiento no existe
        """
        return get_or_404(Movimiento, id_movimiento)

    @classmethod
    def crear(cls, datos: Dict[str, Any]) -> Movimiento:
        """Crea un nuevo movimiento con los datos proporcionados.
        
        Args:
            datos (Dict[str, Any]): Diccionario con los datos del movimiento
            
        Returns:
            Movimiento: Instancia del movimiento creado
            
        Raises:
            SQLAlchemyError: Si ocurre un error al guardar en la base de datos
        """
        movimiento = Movimiento(**datos)
        db.session.add(movimiento)
        commit_or_rollback()
        return movimiento

    @classmethod
    def obtener_estadisticas(cls) -> Dict[str, Any]:
        """Obtiene estadísticas detalladas sobre los movimientos y sus relaciones.
        
        Returns:
            Dict[str, Any]: Diccionario con tres secciones:
                - estadisticas: Lista de tuplas con (id_movimiento, descripción, total_vuelos)
                - aerolineas: Diccionario con top 5 aerolíneas por movimiento (key: id_movimiento)
                - aeropuertos: Diccionario con top 5 aeropuertos por movimiento (key: id_movimiento)
                
        Example:
            {
                'estadisticas': [(1, 'Despegue', 50), ...],
                'aerolineas': {
                    1: [(1, 'Aerolínea X', 30), ...],
                    ...
                },
                'aeropuertos': {
                    1: [(1, 'Aeropuerto Y', 25), ...],
                    ...
                }
            }
        """
        # Estadísticas básicas de movimientos
        stats = (
            db.session.query(
                Movimiento.id_movimiento,
                Movimiento.descripcion,
                func.count(Vuelo.id).label('total_vuelos')
            )
            .join(Vuelo, Vuelo.id_movimiento == Movimiento.id_movimiento)
            .group_by(Movimiento.id_movimiento, Movimiento.descripcion)
            .all()
        )

        # Top 5 aerolíneas por movimiento
        aerolineas = {}
        for mov in Movimiento.query.all():
            aerolineas[mov.id_movimiento] = (
                db.session.query(
                    Aerolinea.id_aerolinea,
                    Aerolinea.nombre_aerolinea,
                    func.count(Vuelo.id).label('total_vuelos')
                )
                .join(Vuelo, Vuelo.id_aerolinea == Aerolinea.id_aerolinea)
                .filter(Vuelo.id_movimiento == mov.id_movimiento)
                .group_by(Aerolinea.id_aerolinea, Aerolinea.nombre_aerolinea)
                .order_by(func.count(Vuelo.id).desc())
                .limit(5)
                .all()
            )

        # Top 5 aeropuertos por movimiento
        aeropuertos = {}
        for mov in Movimiento.query.all():
            aeropuertos[mov.id_movimiento] = (
                db.session.query(
                    Aeropuerto.id_aeropuerto,
                    Aeropuerto.nombre_aeropuerto,
                    func.count(Vuelo.id).label('total_vuelos')
                )
                .join(Vuelo, Vuelo.id_aeropuerto == Aeropuerto.id_aeropuerto)
                .filter(Vuelo.id_movimiento == mov.id_movimiento)
                .group_by(Aeropuerto.id_aeropuerto, Aeropuerto.nombre_aeropuerto)
                .order_by(func.count(Vuelo.id).desc())
                .limit(5)
                .all()
            )

        return {
            'estadisticas': stats,
            'aerolineas': aerolineas,
            'aeropuertos': aeropuertos
        }

    @classmethod
    def obtener_vuelos_por_movimiento(cls, id_movimiento: int) -> Dict[str, Any]:
        """Obtiene todos los vuelos asociados a un movimiento específico con información relacionada.
        
        Args:
            id_movimiento (int): ID del movimiento a consultar
            
        Returns:
            Dict[str, Any]: Diccionario con:
                - movimiento: Instancia del movimiento
                - vuelos: Lista de tuplas (Vuelo, nombre_aerolinea, nombre_aeropuerto)
                
        Example:
            {
                'movimiento': <Movimiento object>,
                'vuelos': [
                    (<Vuelo>, 'Aerolínea X', 'Aeropuerto Y'),
                    ...
                ]
            }
        """
        movimiento = cls.obtener_por_id(id_movimiento)
        
        vuelos = (
            db.session.query(
                Vuelo,
                Aerolinea.nombre_aerolinea,
                Aeropuerto.nombre_aeropuerto
            )
            .join(Aerolinea, Aerolinea.id_aerolinea == Vuelo.id_aerolinea)
            .join(Aeropuerto, Aeropuerto.id_aeropuerto == Vuelo.id_aeropuerto)
            .filter(Vuelo.id_movimiento == id_movimiento)
            .order_by(Vuelo.dia.desc())
            .all()
        )
        
        return {
            'movimiento': movimiento,
            'vuelos': vuelos
        }