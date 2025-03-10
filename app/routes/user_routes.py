from flask import request, jsonify
from flask_restful import Resource
from app.models.models import Bus, Booking, Transaction, User
from app.extensions import db
from datetime import datetime
from sqlalchemy import and_


class ViewAvailableBusesResource(Resource):
    def get(self):
        """
        View all available buses.
        """
        buses = Bus.query.filter_by(is_available=True).all()
        buses_data = [bus.to_dict() for bus in buses]
        return buses_data, 200


class BookSeatResource(Resource):
    def post(self):
        """
        Book a seat on a bus.
        """
        data = request.get_json()
        customer_id = data.get('customer_id')
        bus_id = data.get('bus_id')
        seat_number = data.get('seat_number')

        # Validate required fields
        if not all([customer_id, bus_id, seat_number]):
            return {'message': 'Missing required fields (customer_id, bus_id, seat_number)'}, 400

        # Fetch the bus
        bus = Bus.query.get(bus_id)
        if not bus:
            return {'message': 'Bus not found'}, 404

        # Check if the seat is available
        if seat_number < 1 or seat_number > bus.number_of_seats:
            return {'message': 'Invalid seat number'}, 400

        # Check if the seat is already booked
        existing_booking = Booking.query.filter_by(bus_id=bus_id, seat_number=seat_number).first()
        if existing_booking:
            return {'message': 'Seat already booked'}, 400

        # Create a new booking
        booking = Booking(
            customer_id=customer_id,
            bus_id=bus_id,
            seat_number=seat_number,
            status='pending'
        )
        db.session.add(booking)
        db.session.commit()

        # Return the booking details
        return booking.to_dict(), 201


class ViewMyBookingsResource(Resource):
    def get(self, customer_id):
        """
        View all bookings for a customer.
        """
        bookings = Booking.query.filter_by(customer_id=customer_id).all()
        bookings_data = [booking.to_dict() for booking in bookings]
        return bookings_data, 200


class CancelBookingResource(Resource):
    def delete(self, booking_id):
        """
        Cancel a booking.
        """
        booking = Booking.query.get(booking_id)
        if not booking:
            return {'message': 'Booking not found'}, 404

        # Delete the booking
        db.session.delete(booking)
        db.session.commit()

        # Return success message
        return {'message': 'Booking canceled successfully'}, 200


class UpdateBookingResource(Resource):
    def put(self, booking_id):
        """
        Update a booking (e.g., change seat number).
        """
        booking = Booking.query.get(booking_id)
        if not booking:
            return {'message': 'Booking not found'}, 404

        data = request.get_json()
        seat_number = data.get('seat_number')

        # Validate seat number
        if seat_number:
            if seat_number < 1 or seat_number > booking.bus.number_of_seats:
                return {'message': 'Invalid seat number'}, 400

            # Check if the new seat is already booked
            existing_booking = Booking.query.filter_by(bus_id=booking.bus_id, seat_number=seat_number).first()
            if existing_booking:
                return {'message': 'Seat already booked'}, 400

            booking.seat_number = seat_number

        # Commit changes to the database
        db.session.commit()

        # Return the updated booking details
        return booking.to_dict(), 200


class ViewAvailableSeatsResource(Resource):
    def get(self, bus_id):
        """
        View available seats for a bus.
        """
        bus = Bus.query.get(bus_id)
        if not bus:
            return {'message': 'Bus not found'}, 404

        # Get all confirmed bookings for the bus
        confirmed_bookings = Booking.query.filter_by(bus_id=bus_id, status='confirmed').all()
        booked_seats = [booking.seat_number for booking in confirmed_bookings]

        # Calculate available seats
        available_seats = [seat for seat in range(1, bus.number_of_seats + 1) if seat not in booked_seats]

        return {'available_seats': available_seats}, 200


class SearchBusResource(Resource):
    def get(self):
        """
        Search buses by travel date and route.
        """
        departure_date = request.args.get('departure_date')
        from_location = request.args.get('from')
        to_location = request.args.get('to')

        # Validate required fields
        if not all([departure_date, from_location, to_location]):
            return {'message': 'Missing required fields (departure_date, from, to)'}, 400

        # Convert departure_date to a datetime object (ignoring time)
        try:
            departure_date = datetime.fromisoformat(departure_date).date()  # Extract only the date part
        except ValueError:
            return {'message': 'Invalid departure date format (use ISO format)'}, 400

        # Search for buses
        buses = Bus.query.filter(
            and_(
                Bus.departure_time.cast(db.Date) == departure_date,  # Compare only the date part
                Bus.route.ilike(f'%{from_location}%'),  # Origin is the first part of the route
                Bus.route.ilike(f'%{to_location}%'),    # Destination is the last part of the route
                Bus.is_available == True
            )
        ).all()

        buses_data = [bus.to_dict() for bus in buses]
        return buses_data, 200

class SimulatePaymentResource(Resource):
    def post(self, booking_id):
        """
        Simulate payment for a booking.
        """
        booking = Booking.query.get(booking_id)
        if not booking:
            return {'message': 'Booking not found'}, 404

        data = request.get_json()
        amount_paid = data.get('amount_paid')
        payment_method = data.get('payment_method')

        # Validate required fields
        if not all([amount_paid, payment_method]):
            return {'message': 'Missing required fields (amount_paid, payment_method)'}, 400

        # Check if the booking is already confirmed
        if booking.status == 'confirmed':
            return {'message': 'Booking is already confirmed'}, 400

        # Create a new transaction
        transaction = Transaction(
            booking_id=booking_id,
            amount_paid=amount_paid,
            payment_method=payment_method
        )
        db.session.add(transaction)

        # Update the booking status to confirmed
        booking.status = 'confirmed'
        db.session.commit()

        # Return the transaction details
        return transaction.to_dict(), 201
    
    
    
class BookMultipleSeatsResource(Resource):
    def post(self):
        """
        Book multiple seats on a bus.
        """
        data = request.get_json()
        customer_id = data.get('customer_id')  # Automatically fetched from the logged-in user
        bus_id = data.get('bus_id')
        seat_numbers = data.get('seat_numbers')  # List of seat numbers selected by the user

        # Validate required fields
        if not all([customer_id, bus_id, seat_numbers]):
            return {'message': 'Missing required fields (customer_id, bus_id, seat_numbers)'}, 400

        # Fetch the bus
        bus = Bus.query.get(bus_id)
        if not bus:
            return {'message': 'Bus not found'}, 404

        # Check if all selected seats are available
        for seat_number in seat_numbers:
            if seat_number < 1 or seat_number > bus.number_of_seats:
                return {'message': f'Invalid seat number: {seat_number}'}, 400

            existing_booking = Booking.query.filter_by(bus_id=bus_id, seat_number=seat_number).first()
            if existing_booking:
                return {'message': f'Seat {seat_number} is already booked'}, 400

        # Calculate total amount to be paid
        total_amount = len(seat_numbers) * bus.cost_per_seat

        # Create bookings for each selected seat
        bookings = []
        for seat_number in seat_numbers:
            booking = Booking(
                customer_id=customer_id,
                bus_id=bus_id,
                seat_number=seat_number,
                status='pending'
            )
            db.session.add(booking)
            bookings.append(booking)

        db.session.commit()

        # Return the booking details and total amount
        return {
            'bookings': [booking.to_dict() for booking in bookings],
            'total_amount': total_amount
        }, 201