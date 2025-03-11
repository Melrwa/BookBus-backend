from flask import request, jsonify
from flask_restful import Resource
from app.models.models import Bus, User, UserRole
from app.extensions import db
from datetime import datetime


class AddBusResource(Resource):
    def post(self):
        """
        Add a new bus.
        """
        data = request.get_json()

        # Validate required fields
        required_fields = ['number_of_seats', 'cost_per_seat', 'route', 'departure_time', 'arrival_time']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400

        # Validate number_of_seats
        try:
            number_of_seats = int(data.get('number_of_seats'))  # Convert to integer
        except (ValueError, TypeError):
            return {'message': 'Number of seats must be a valid integer'}, 400

        if number_of_seats < 1:
            return {'message': 'Number of seats must be at least 1'}, 400

        # Validate cost_per_seat
        try:
            cost_per_seat = float(data.get('cost_per_seat'))  # Convert to float
        except (ValueError, TypeError):
            return {'message': 'Cost per seat must be a valid number'}, 400

        # Create a new bus
        bus = Bus(
            number_of_seats=number_of_seats,
            cost_per_seat=cost_per_seat,
            route=data.get('route'),
            departure_time=datetime.fromisoformat(data.get('departure_time')),
            arrival_time=datetime.fromisoformat(data.get('arrival_time')),
            is_available=True
        )

        # Add and commit the bus to the database
        db.session.add(bus)
        db.session.commit()

        # Return the bus's details
        return bus.to_dict(), 201
    
class UpdateBusResource(Resource):
    def put(self, bus_id):
        """
        Update bus details.
        """
        # Fetch the bus
        bus = Bus.query.get(bus_id)

        # Check if the bus exists
        if not bus:
            return {'message': 'Bus not found'}, 404

        data = request.get_json()

        # Update bus details with validation
        try:
            number_of_seats = data.get('number_of_seats')
            if number_of_seats is not None:
                number_of_seats = int(number_of_seats)  # Convert to integer
                if number_of_seats < 1:
                    return {'message': 'Number of seats must be at least 1'}, 400
                bus.number_of_seats = number_of_seats

            cost_per_seat = data.get('cost_per_seat')
            if cost_per_seat is not None:
                cost_per_seat = float(cost_per_seat)  # Convert to float
                if cost_per_seat < 0:
                    return {'message': 'Cost per seat cannot be negative'}, 400
                bus.cost_per_seat = cost_per_seat

            route = data.get('route')
            if route is not None:
                bus.route = route

            departure_time = data.get('departure_time')
            if departure_time is not None:
                bus.departure_time = datetime.fromisoformat(departure_time)

            arrival_time = data.get('arrival_time')
            if arrival_time is not None:
                bus.arrival_time = datetime.fromisoformat(arrival_time)

            is_available = data.get('is_available')
            if is_available is not None:
                if not isinstance(is_available, bool):
                    return {'message': 'is_available must be a boolean'}, 400
                bus.is_available = is_available

        except (ValueError, TypeError) as e:
            # Handle invalid input (e.g., non-integer number_of_seats or non-float cost_per_seat)
            return {'message': f'Invalid input: {str(e)}'}, 400

        # Commit changes to the database
        db.session.commit()

        # Return the updated bus details
        return bus.to_dict(), 200


class DeleteBusResource(Resource):
    def delete(self, bus_id):
        """
        Delete a bus.
        """
        # Fetch the bus
        bus = Bus.query.get(bus_id)

        # Check if the bus exists
        if not bus:
            return {'message': 'Bus not found'}, 404

        # Delete the bus
        db.session.delete(bus)
        db.session.commit()

        # Return success message
        return {'message': 'Bus deleted successfully'}, 200


class ScheduleBusResource(Resource):
    def put(self, bus_id):
        """
        Schedule a bus for travel.
        """
        # Fetch the bus
        bus = Bus.query.get(bus_id)

        # Check if the bus exists
        if not bus:
            return {'message': 'Bus not found'}, 404

        data = request.get_json()
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')

        # Validate required fields
        if not departure_time or not arrival_time:
            return {'message': 'Missing required fields (departure_time, arrival_time)'}, 400

        # Update the bus's schedule
        bus.departure_time = datetime.fromisoformat(departure_time)
        bus.arrival_time = datetime.fromisoformat(arrival_time)
        db.session.commit()

        # Return success message
        return {'message': 'Bus scheduled successfully'}, 200


class UpdatePriceResource(Resource):
    def put(self, bus_id):
        """
        Update the price per seat for a bus.
        """
        # Fetch the bus
        bus = Bus.query.get(bus_id)

        # Check if the bus exists
        if not bus:
            return {'message': 'Bus not found'}, 404

        data = request.get_json()
        cost_per_seat = data.get('cost_per_seat')

        # Validate required fields
        if not cost_per_seat:
            return {'message': 'Missing required field (cost_per_seat)'}, 400

        # Update the price per seat
        bus.cost_per_seat = cost_per_seat
        db.session.commit()

        # Return success message
        return {'message': 'Price per seat updated successfully'}, 200


class MyAssignedBusesResource(Resource):
    def get(self):
        """
        Fetch buses assigned to the current driver.
        """
        # In a real application, this would come from the authenticated user's session or token.
        driver_id = request.args.get('driver_id')  # Example: /driver/my_assigned_buses?driver_id=1

        if not driver_id:
            return {'message': 'Driver ID is required'}, 400

        # Fetch buses assigned to the driver
        buses = Bus.query.filter_by(driver_id=driver_id).all()

        if not buses:
            return {'message': 'You do not have any buses assigned'}, 404

        # Return the list of buses
        buses_data = [bus.to_dict() for bus in buses]
        return buses_data, 200
    

class FetchDriversResource(Resource):
    def get(self):
        """
        Fetch all users with the role 'driver'.
        """
        drivers = User.query.filter_by(role=UserRole.DRIVER).all()
        drivers_data = [driver.to_dict() for driver in drivers]
        return drivers_data, 200
    


class DeleteDriverResource(Resource):
    def delete(self, driver_id):
        """
        Delete a driver by their ID.
        """
        driver = User.query.get(driver_id)

        # Check if the driver exists
        if not driver:
            return {'message': 'Driver not found'}, 404

        # Check if the user is a driver
        if driver.role != UserRole.DRIVER:
            return {'message': 'User is not a driver'}, 400

        # Delete the driver
        db.session.delete(driver)
        db.session.commit()

        return {'message': 'Driver deleted successfully'}, 200