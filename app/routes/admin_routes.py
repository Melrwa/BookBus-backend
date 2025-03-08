from flask import request, jsonify
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

            # Fetch all bookings from the database
            bookings = Booking.query.all()

            # Serialize the bookings using the schema
            serialized_bookings = booking_schema.dump(bookings, many=True)

            # Return the serialized bookings as a JSON response
            return serialized_bookings, 200

class ViewAllTransactionsResource(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        transactions = Transaction.query.all()
        return transaction_schema.dump(transactions, many=True), 200