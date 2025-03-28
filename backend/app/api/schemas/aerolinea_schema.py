# app/api/schemas/aerolinea_schema.py
from marshmallow import Schema, fields, validate

class AerolineaSchema(Schema):

    id_aerolinea = fields.Int(dump_only=True)
    nombre_aerolinea = fields.Str(required=True, validate=validate.Length(min=1, max=50))
