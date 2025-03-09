from app.models.bookings import Booking
from marshmallow import Schema, fields, validate


class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    bus_id = fields.Int(required=True)
    seat_number = fields.Int(required=True, validate=validate.Range(min=1))
    booking_date = fields.DateTime(required=True)
    status = fields.Str(validate=validate.OneOf(['confirmed', 'pending', 'cancelled']))

    class Meta:
        fields = ('id', 'customer_id', 'bus_id', 'seat_number', 'booking_date', 'status')






def get_all_bookings_service(page=1, per_page=10):
    """Get all bookings with pagination."""
    query = Booking.query
    
    # Paginate the query
    bookings = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Serialize the bookings
    serialized_bookings = booking_schema.dump(bookings.items, many=True)
    
    # Return the paginated results
    return {
        "bookings": serialized_bookings,
        "total_pages": bookings.pages,
        "current_page": bookings.page,
        "total_bookings": bookings.total
    }