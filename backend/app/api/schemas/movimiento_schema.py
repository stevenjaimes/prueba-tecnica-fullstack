from marshmallow import Schema, fields, validate

class MovimientoSchema(Schema):
    id_movimiento = fields.Int(dump_only=True)
    descripcion = fields.Str(
        required=True, 
        validate=validate.OneOf(['Salida', 'Llegada']),
        error_messages={
            'validator_failed': 'El movimiento debe ser "Salida" o "Llegada"'
        }
    )
    