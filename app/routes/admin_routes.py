from flask import request, jsonify, request, make_response
from flask_restful import Resource
from app.models.user import User
from app.models.bookings import Booking
from app.models.transactions import Transaction
from app.extensions import db
from app.utils.jwt_utils import token_required
from app.schemas.user_schema import UserSchema
from app.schemas.bookings_schema import BookingSchema
from app.schemas.transaction_schema import TransactionSchema
import logging

user_schema = UserSchema()
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)  # For serializing multiple bookings
transaction_schema = TransactionSchema()


class AddDriverResource(Resource):
    @token_required
    def post(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return {'message': 'Missing required fields'}, 400

        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400

        driver = User(name=name, email=email, role='driver')
        driver.set_password(password)

        db.session.add(driver)
        db.session.commit()

        return user_schema.dump(driver), 201

class ViewAllUsersResource(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        users = User.query.all()
        return user_schema.dump(users, many=True), 200

class ViewAllBookingsResource(Resource):
    @token_required
    def get(self, current_user):
        """Get all bookings (admin only)."""
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        try:
            # Fetch all bookings from the database
            bookings = Booking.query.all()
            logging.info(f"Fetched {len(bookings)} bookings from the database.")
        except Exception as e:
            logging.error(f"Error fetching bookings: {str(e)}")
            return {'message': 'Failed to fetch bookings'}, 500

        try:
            # Serialize the bookings using the schema
            serialized_bookings = bookings_schema.dump(bookings)
            logging.info("Bookings serialized successfully.")
        except Exception as e:
            logging.error(f"Error serializing bookings: {str(e)}")
            return {'message': 'Failed to serialize bookings'}, 500

        # Return the serialized bookings
        return {'bookings': serialized_bookings}, 200




class ViewAllTransactionsResource(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        transactions = Transaction.query.all()
        return transaction_schema.dump(transactions, many=True), 200