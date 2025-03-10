from flask import request, jsonify
from flask_restful import Resource
from app.models.models import Bus, User
from app.extensions import db
from datetime import datetime


class AddBusResource(Resource):
    def post(self):
        """
        Add a new bus.
        """
        data = request.get_json()
        number_of_seats = data.get('number_of_seats')
        cost_per_seat = data.get('cost_per_seat')
        route = data.get('route')
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')

        # Validate required fields
        if not all([number_of_seats, cost_per_seat, route, departure_time, arrival_time]):
            return {'message': 'Missing required fields'}, 400

        # Create a new bus
        bus = Bus(
            number_of_seats=number_of_seats,
            cost_per_seat=cost_per_seat,
            route=route,
            departure_time=datetime.fromisoformat(departure_time),
            arrival_time=datetime.fromisoformat(arrival_time),
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
        number_of_seats = data.get('number_of_seats')
        cost_per_seat = data.get('cost_per_seat')
        route = data.get('route')
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')
        is_available = data.get('is_available')

        # Update bus details
        if number_of_seats:
            bus.number_of_seats = number_of_seats
        if cost_per_seat:
            bus.cost_per_seat = cost_per_seat
        if route:
            bus.route = route
        if departure_time:
            bus.departure_time = datetime.fromisoformat(departure_time)
        if arrival_time:
            bus.arrival_time = datetime.fromisoformat(arrival_time)
        if is_available is not None:
            bus.is_available = is_available

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