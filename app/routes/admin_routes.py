from flask import request, jsonify
from flask_restful import Resource
from app.models.models import Booking, Bus, Transaction, User
from app.extensions import db
from app.utils.jwt_utils import token_required


class AddDriverResource(Resource):
    def post(self):
        """
        Add a new driver (no admin check).
        """
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # Validate required fields
        if not name or not email or not password:
            return {'message': 'Missing required fields'}, 400

        # Check if email is already registered
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400

        # Create a new driver
        driver = User(name=name, email=email, role='driver')
        driver.password_hash = password  # Hash the password

        # Add and commit the driver to the database
        db.session.add(driver)
        db.session.commit()

        # Return the driver's details
        return driver.to_dict(), 201

class ViewAllBookingsResource(Resource):
    def get(self):
        bookings = Booking.query.all()
        bookings_data = [booking.to_dict() for booking in bookings]
        return bookings_data, 200


class ViewAllTransactionsResource(Resource):
    def get(self):
        transactions = Transaction.query.all()
        transactions_data = [transaction.to_dict() for transaction in transactions]
        return transactions_data, 200

class ViewAllUsersResource(Resource):
    def get(self):
        users = User.query.all()
        users_data = [user.to_dict() for user in users]
        return users_data, 200

class AssignDriverToBusResource(Resource):
    def post(self):
        """
        Assign a driver to a bus (no admin check).
        """
        data = request.get_json()
        driver_id = data.get('driver_id')
        bus_id = data.get('bus_id')

        # Validate required fields
        if not driver_id or not bus_id:
            return {'message': 'Missing required fields (driver_id, bus_id)'}, 400

        # Fetch the driver and bus
        driver = User.query.get(driver_id)
        bus = Bus.query.get(bus_id)

        # Check if the driver and bus exist
        if not driver:
            return {'message': 'Driver not found'}, 404
        if not bus:
            return {'message': 'Bus not found'}, 404

        # Check if the user is a driver
        if driver.role != 'driver':
            return {'message': 'User is not a driver'}, 400

        # Assign the driver to the bus
        bus.driver_id = driver.id
        db.session.commit()

        # Return success response with updated driver and bus details
        return {
            'message': 'Driver assigned to bus successfully',
            'driver': driver.to_dict(),
            'bus': bus.to_dict()
        }, 200

class ChangeUserRoleResource(Resource):
    def post(self):
        """
        Change a user's role (no admin check).
        """
        data = request.get_json()
        user_id = data.get('user_id')
        new_role = data.get('new_role')

        # Validate required fields
        if not user_id or not new_role:
            return {'message': 'Missing required fields (user_id, new_role)'}, 400

        # Fetch the user
        user = User.query.get(user_id)

        # Check if the user exists
        if not user:
            return {'message': 'User not found'}, 404

        # Validate the new role
        valid_roles = ['admin', 'driver', 'customer']
        if new_role not in valid_roles:
            return {'message': 'Invalid role'}, 400

        # Change the user's role
        user.role = new_role
        db.session.commit()

        # Return success response
        return {'message': f'User role changed to {new_role} successfully'}, 200
    


class ViewMyBusesResource(Resource):
     def get(self):
        """
        View all buses added by the driver.
        """
        # Fetch all buses (for simplicity, no driver filtering)
        buses = Bus.query.all()
        buses_data = [bus.to_dict() for bus in buses]
        return buses_data, 200
     

