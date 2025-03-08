from marshmallow import Schema, fields, validate

class BusSchema(Schema):
    id = fields.Int(dump_only=True)
    driver_id = fields.Int(required=True)
    number_of_seats = fields.Int(required=True, validate=validate.Range(min=1))
    cost_per_seat = fields.Float(required=True, validate=validate.Range(min=0))
    route = fields.Str(required=True)
    departure_time = fields.DateTime(required=True)
    arrival_time = fields.DateTime(required=True)
    is_available = fields.Boolean()

    class Meta:
        fields = ('id', 'driver_id', 'number_of_seats', 'cost_per_seat', 'route', 'departure_time', 'arrival_time', 'is_available')