from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.database.connection import db
from flask import abort

def get_or_404(model, object_id):
    """Obtiene un objeto o devuelve 404"""
    obj = model.query.get(object_id)
    if not obj:
        abort(404, description=f"{model.__name__} no encontrado")
    return obj

def commit_or_rollback():
    """Intenta hacer commit, si falla hace rollback"""
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e