from app.extensions import db
from sqlalchemy.orm import validates
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Must not be null
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)  # Must not be null
    seat_number = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # Default status is 'pending'

    # Relationships
    customer = db.relationship('User', back_populates='bookings')
    bus = db.relationship('Bus', back_populates='bookings')
    transaction = db.relationship('Transaction', back_populates='booking', uselist=False, lazy=True)

    # Unique constraint to prevent double booking
    __table_args__ = (
        db.UniqueConstraint('bus_id', 'seat_number', name='unique_seat_booking'),
    )

    @validates('seat_number')
    def validate_seat_number(self, key, seat_number):
        if seat_number < 1:
            raise ValueError("Seat number must be at least 1.")
        return seat_number

    @validates('status')
    def validate_status(self, key, status):
        if status not in ['confirmed', 'canceled', 'pending']:
            raise ValueError("Invalid status. Must be 'confirmed', 'canceled', or 'pending'.")
        return status

    def __repr__(self):
        return f'<Booking {self.id}>'