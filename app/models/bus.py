from app.extensions import db
from sqlalchemy.orm import validates
from datetime import datetime, timedelta

class Bus(db.Model):
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Allow null for unassigned buses
    number_of_seats = db.Column(db.Integer, nullable=False)
    cost_per_seat = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(200), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    # Relationships
    driver = db.relationship('User', back_populates='buses')
    bookings = db.relationship('Booking', back_populates='bus', lazy=True)

    @validates('number_of_seats')
    def validate_number_of_seats(self, key, number_of_seats):
        if number_of_seats < 1:
            raise ValueError("Number of seats must be at least 1.")
        return number_of_seats

    @validates('cost_per_seat')
    def validate_cost_per_seat(self, key, cost_per_seat):
        if cost_per_seat < 0:
            raise ValueError("Cost per seat cannot be negative.")
        return cost_per_seat

    @validates('arrival_time')
    def validate_arrival_time(self, key, arrival_time):
        if arrival_time <= self.departure_time:
            raise ValueError("Arrival time must be after departure time.")
        return arrival_time

    @property
    def travel_time(self):
        """
        Calculates the travel time in hours and minutes.
        """
        delta = self.arrival_time - self.departure_time
        total_seconds = delta.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    @property
    def available_seats(self):
        """
        Calculates the number of available seats.
        """
        confirmed_bookings = [booking for booking in self.bookings if booking.status == 'confirmed']
        return self.number_of_seats - len(confirmed_bookings)

    def __repr__(self):
        return f'<Bus {self.route}>'