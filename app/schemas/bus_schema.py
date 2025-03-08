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
    travel_time = fields.Method("get_travel_time")  # Add travel_time field
    available_seats = fields.Method("get_available_seats")  # Add available_seats field

    def get_travel_time(self, obj):
        """
        Method to calculate and return travel time.
        """
        return obj.travel_time

    def get_available_seats(self, obj):
        """
        Method to calculate and return available seats.
        """
        return obj.available_seats

    class Meta:
        fields = ('id', 'driver_id', 'number_of_seats', 'cost_per_seat', 'route', 'departure_time', 'arrival_time', 'is_available', 'travel_time', 'available_seats')