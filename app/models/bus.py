from app.extensions import db
from sqlalchemy.orm import validates

class Bus(db.Model):
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

    def __repr__(self):
        return f'<Bus {self.route}>'