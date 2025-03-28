# app/schemas.py
from marshmallow import Schema, fields, validate

class AeropuertoSchema(Schema):
    id_aeropuerto = fields.Int(dump_only=True)
    nombre_aeropuerto = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    
    class Meta:
        fields = ("id_aeropuerto", "nombre_aeropuerto") 
