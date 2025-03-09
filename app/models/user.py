# from app.extensions import db, bcrypt
# from sqlalchemy.orm import validates
# from app.utils.jwt_utils import generate_token  # Import the JWT utility

# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # admin, driver, customer

#     # Relationships
#     buses = db.relationship('Bus', back_populates='driver', lazy=True)
#     bookings = db.relationship('Booking', back_populates='customer', lazy=True)

#     @validates('email')
#     def validate_email(self, key, email):
#         if '@' not in email:
#             raise ValueError("Invalid email address.")
#         return email

#     @validates('role')
#     def validate_role(self, key, role):
#         if role not in ['admin', 'driver', 'customer']:
#             raise ValueError("Invalid role. Must be 'admin', 'driver', or 'customer'.")
#         return role

#     def set_password(self, password):
#         if len(password) < 6:
#             raise ValueError("Password must be at least 6 characters long.")
#         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password_hash, password)

#     def generate_auth_token(self):
#         """
#         Generates a JWT token for the user.
#         """
#         return generate_token(self.id, self.role)

#     def to_dict(self):
#         """
#         Converts the User instance to a dictionary.
#         """
#         return {
#             "id": self.id,
#             "name": self.name,
#             "email": self.email,
#             "role": self.role,
#             "buses": [bus.to_dict() for bus in self.buses],  # Assuming Bus model has a to_dict method
#             "bookings": [booking.to_dict() for booking in self.bookings]  # Assuming Booking model has a to_dict method
#         }

#     def __repr__(self):
#         return f'<User  {self.name}>'