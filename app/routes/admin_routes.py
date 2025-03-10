from flask import request, jsonify
from flask_restful import Resource
from app.models.models import Booking, Transaction, User
from app.extensions import db
from app.utils.jwt_utils import token_required


class AddDriverResource(Resource):
    @token_required
    def post(self, current_user):
        """
        Add a new driver (admin-only).
        """
        # Check if the current user is an admin
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

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