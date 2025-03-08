from marshmallow import Schema, fields, validate

class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    bus_id = fields.Int(required=True)
    seat_number = fields.Int(required=True, validate=validate.Range(min=1))
    booking_date = fields.DateTime(required=True)
    status = fields.Str(validate=validate.OneOf(['confirmed', 'cancelled']))

    class Meta:
        fields = ('id', 'customer_id', 'bus_id', 'seat_number', 'booking_date', 'status')