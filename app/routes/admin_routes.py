from flask import request, make_response, jsonify
from flask_restful import Resource
from app.models.models import Booking, Transaction, User
from app.extensions import db
from app.utils.jwt_utils import token_required


class AddDriverResource(Resource):
    @token_required
    def post(self, current_user):
        if current_user.role != 'admin':
            return make_response({'message': 'Unauthorized'}, 403)

        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return make_response({'message': 'Missing required fields'}, 400)

        if User.query.filter_by(email=email).first():
            return make_response({'message': 'Email already registered'}, 400)

        driver = User(name=name, email=email, role='driver')
        driver.set_password(password)

        db.session.add(driver)
        db.session.commit()

        return make_response(driver.to_dict(), 201)  # Use .to_dict() instead of user_schema.dump(driver)
    
    
class ViewAllBookingsResource(Resource):
    @token_required
    def get(self, current_user):
        """
        Retrieve all bookings.
        """
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        bookings = Booking.query.all()
        print( booking.to_dict() for booking in bookings)

        return [booking.to_dict() for booking in bookings]




class ViewAllTransactionsResource(Resource):
    @token_required
    def get(self, current_user):
        """
        Retrieve all transactions.
        """
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        transactions = Transaction.query.all()
        return jsonify([
            {
                "id": transaction.id,
                "booking_id": transaction.booking_id,
                "amount_paid": transaction.amount_paid,
                "payment_date": transaction.payment_date.isoformat(),
                "payment_method": transaction.payment_method,
                "booking": transaction.booking.id if transaction.booking else None  # Assuming booking has an id attribute
            }
            for transaction in transactions
        ])


class ViewAllUsersResource(Resource):
    @token_required
    def get(self, current_user):
        """
        Retrieve all users.
        """
        if current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        users = User.query.all()
        return jsonify([
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "buses": [bus.id for bus in user.buses],  # Return only IDs to avoid circular references
                "bookings": [booking.id for booking in user.bookings]  # Return only IDs to avoid circular references
            }
            for user in users
        ])