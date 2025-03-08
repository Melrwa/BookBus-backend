from flask import request, jsonify
from flask_restful import Resource
from app.models.user import User
from app.models.bookings import Booking
from app.models.transactions import Transaction
from app.extensions import db
from app.utils.jwt_utils import token_required

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

        return {'message': 'Driver added successfully', 'driver_id': driver.id}, 201

class ViewAllUsersResource(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        users = User.query.all()
        users_data = [{'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role} for user in users]
        return {'users': users_data}, 200

class ViewAllBookingsResource(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        bookings = Booking.query.all()
        bookings_data = [{'id': booking.id, 'customer_id': booking.customer_id, 'bus_id': booking.bus_id, 'seat_number': booking.seat_number, 'status': booking.status} for booking in bookings]
        return {'bookings': bookings_data}, 200

class ViewAllTransactionsResource(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        transactions = Transaction.query.all()
        transactions_data = [{'id': transaction.id, 'booking_id': transaction.booking_id, 'amount_paid': transaction.amount_paid, 'payment_method': transaction.payment_method} for transaction in transactions]
        return {'transactions': transactions_data}, 200