from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from app.extensions import db, bcrypt
from sqlalchemy.orm import validates
from app.utils.jwt_utils import generate_token
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    ADMIN = "admin"
    DRIVER = "driver"
    CUSTOMER = "customer"


class BookingStatus(str, PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"


# User Model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)

    # Relationships
    bookings = db.relationship('Booking', back_populates='customer', cascade='all, delete-orphan')
    buses = db.relationship('Bus', back_populates='driver', lazy=True)

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def generate_auth_token(self):
        """Generates a JWT token for the user."""
        return generate_token(self.id, self.role)
            
    def to_dict(self, serialize=True):
            data = {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "role": self.role.value if hasattr(self.role, 'value') else str(self.role),
            }
            if serialize:
                data.update({
                    "buses": [bus.id for bus in self.buses],  # Only return bus IDs
                    "bookings": [booking.id for booking in self.bookings]  # Only return booking IDs
                })
            return data

    def __repr__(self):
        return f'<User {self.name}>'


# Bus Model
class Bus(db.Model, SerializerMixin):
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    number_of_seats = db.Column(db.Integer, nullable=False)
    cost_per_seat = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(200), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    # Relationships
    driver = db.relationship('User', back_populates='buses')
    bookings = db.relationship('Booking', back_populates='bus', lazy=True)

    @property
    def available_seats(self):
        """Calculates the number of available seats."""
        confirmed_bookings = [booking for booking in self.bookings if booking.status == BookingStatus.CONFIRMED]
        return self.number_of_seats - len(confirmed_bookings)

    @property
    def travel_time(self):
        """Calculates the travel time in hours and minutes."""
        delta = self.arrival_time - self.departure_time
        total_seconds = delta.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


    def to_dict(self, serialize=True):
        data = {
            "id": self.id,
            "driver_id": self.driver_id,
            "number_of_seats": self.number_of_seats,
            "cost_per_seat": self.cost_per_seat,
            "route": self.route,
            "departure_time": self.departure_time.isoformat(),
            "arrival_time": self.arrival_time.isoformat(),
            "is_available": self.is_available,
            "available_seats": self.available_seats,
            "travel_time": self.travel_time,
        }
        if serialize:
            data.update({
                "driver": self.driver.to_dict(serialize=False) if self.driver else None,
                "bookings": [booking.to_dict(serialize=False) for booking in self.bookings]
            })
        return data
    
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

    def __repr__(self):
        return f'<Bus {self.route}>'


class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(Enum(BookingStatus), default=BookingStatus.PENDING, nullable=False)

    # Relationships
    customer = db.relationship('User', back_populates='bookings')
    bus = db.relationship('Bus', back_populates='bookings')
    transaction = db.relationship('Transaction', back_populates='booking', uselist=False)  # Add this line


    def to_dict(self, serialize=True):
        data = {
            "id": self.id,
            "customer_id": self.customer_id,
            "bus_id": self.bus_id,
            "seat_number": self.seat_number,
            "booking_date": self.booking_date.isoformat(),
            "status": self.status.value if hasattr(self.status, 'value') else str(self.status),
        }
        if serialize:
            data.update({
                "customer": self.customer.to_dict(serialize=False) if self.customer else None,
                "bus": self.bus.to_dict(serialize=False) if self.bus else None,
                "transaction": self.transaction.to_dict(serialize=False) if self.transaction else None
            })
        return data


    @validates('seat_number')
    def validate_seat_number(self, key, seat_number):
        if seat_number < 1:
            raise ValueError("Seat number must be at least 1.")
        return seat_number

    @validates('status')
    def validate_status(self, key, status):
        if status not in [BookingStatus.CONFIRMED, BookingStatus.CANCELED, BookingStatus.PENDING]:
            raise ValueError("Invalid status. Must be 'confirmed', 'canceled', or 'pending'.")
        return status

    def __repr__(self):
        return f"<Booking {self.id}>"


# Transaction Model
class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., M-Pesa, Credit Card

    # Relationships
    booking = db.relationship('Booking', back_populates='transaction')



    def to_dict(self, serialize=True):
        data = {
            "id": self.id,
            "booking_id": self.booking_id,
            "amount_paid": self.amount_paid,
            "payment_date": self.payment_date.isoformat(),
            "payment_method": self.payment_method,
        }
        if serialize:
            data.update({
                "booking": self.booking.to_dict(serialize=False) if self.booking else None
            })
        return data

    @validates('amount_paid')
    def validate_amount_paid(self, key, amount_paid):
        if amount_paid < 0:
            raise ValueError("Amount paid cannot be negative.")
        return amount_paid

    @validates('payment_method')
    def validate_payment_method(self, key, payment_method):
        if payment_method not in ['M-Pesa', 'Credit Card', 'PayPal']:
            raise ValueError("Invalid payment method.")
        return payment_method

    def __repr__(self):
        return f'<Transaction {self.id}>'