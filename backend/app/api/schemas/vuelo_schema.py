from marshmallow import Schema, fields, validate

class VueloSchema(Schema):
    id = fields.Int(dump_only=True, validate=validate.Length(min=1, max=50))
    id_aerolinea = fields.Int(required=True, validate=validate.Length(min=1, max=50))
    id_aeropuerto = fields.Int(required=True, validate=validate.Length(min=1, max=50))
    id_movimiento = fields.Int(required=True, vvalidate=validate.Length(min=1, max=50))
    dia = fields.Date(required=True)



