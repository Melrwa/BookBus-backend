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




# Initialize the schema
booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)  # For serializing multiple bookings

class ViewAllBookingsResource(Resource):
    @token_required
    def get(self, current_user):
        """Get all bookings (admin only)."""
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        # Get pagination parameters from the query string
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Fetch all bookings from the database with pagination
        bookings = Booking.query.paginate(page=page, per_page=per_page, error_out=False)

        # Serialize the bookings using the schema
        try:
            serialized_bookings = bookings_schema.dump(bookings.items)
            logging.info("Serialized Bookings: %s", serialized_bookings)  # Log the serialized data
        except Exception as e:
            logging.error("Serialization error: %s", str(e))  # Log the error
            return {'message': f'Serialization error: {str(e)}'}, 500

        # Ensure the output is JSON-serializable
        if not isinstance(serialized_bookings, (list, dict)):
            logging.error("Serialization error: Invalid data format")  # Log the error
            return {'message': 'Serialization error: Invalid data format'}, 500

        # Prepare the response data
        response_data = {
            'bookings': serialized_bookings,
            'pagination': {
                'page': bookings.page,
                'per_page': bookings.per_page,
                'total_pages': bookings.pages,
                'total_bookings': bookings.total
            }
        }

        # Use make_response to construct the response
        response = make_response(response_data, 200)
        response.headers['Content-Type'] = 'application/json'
        return response




class ViewAllTransactionsResource(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        transactions = Transaction.query.all()
        return transaction_schema.dump(transactions, many=True), 200