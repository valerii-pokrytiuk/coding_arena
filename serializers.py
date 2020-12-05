from marshmallow import Schema, fields


class UnitSchema(Schema):
    id = fields.Int()
    unit = fields.Str()
    type = fields.Str()
    task = fields.Str()
    data = fields.Str()  # All data should be forced to json str to be decoded at client side
    solution = fields.Str()
