from flask import request, jsonify, request
from flask_restful import Resource
from app.models.user import User
from app.models.bookings import Booking
from app.models.transactions import Transaction
from app.extensions import db
from app.utils.jwt_utils import token_required
from app.schemas.user_schema import UserSchema
from app.schemas.bookings_schema import BookingSchema
from app.schemas.transaction_schema import TransactionSchema

user_schema = UserSchema()
booking_schema = BookingSchema()
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
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        # Get pagination parameters from the query string
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Paginate the bookings query
        bookings = Booking.query.paginate(page=page, per_page=per_page, error_out=False)

        # Serialize the paginated bookings
        try:
            serialized_bookings = booking_schema.dump(bookings.items, many=True)
        except Exception as e:
            return {'message': f'Serialization error: {str(e)}'}, 500

        # Ensure the output is JSON-serializable
        if not isinstance(serialized_bookings, (list, dict)):
            return {'message': 'Serialization error: Invalid data format'}, 500

        # Return the serialized bookings along with pagination metadata
        return {
            'bookings': serialized_bookings,
            'pagination': {
                'page': bookings.page,
                'per_page': bookings.per_page,
                'total_pages': bookings.pages,
                'total_items': bookings.total
            }
        }, 200

class ViewAllTransactionsResource(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        transactions = Transaction.query.all()
        return transaction_schema.dump(transactions, many=True), 200