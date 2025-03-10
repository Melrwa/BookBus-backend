from flask import request, make_response, jsonify
from flask_restful import Resource
from app.models.models import User
from app.extensions import db, bcrypt
from app.utils.jwt_utils import generate_token, decode_token
from datetime import datetime, timedelta


class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'customer')  # Default role is 'customer'

        # Validate required fields
        if not name or not email or not password:
            return make_response(jsonify({'message': 'Missing required fields (name, email, password)'}), 400)

        # Check if email is already registered
        if User.query.filter_by(email=email).first():
            return make_response(jsonify({'message': 'Email already registered'}), 400)

        # Create a new user
        user = User(name=name, email=email, role=role)
        user.password_hash = password  # This will hash the password automatically

        # Add and commit the user to the database
        db.session.add(user)
        db.session.commit()

        # Generate a JWT token for the new user
        token = generate_token(user.id, user.role)

        # Create a response and set the JWT as a cookie
        response = make_response(jsonify({
            'user': user.to_dict()  # Return user data (excluding password)
        }), 201)

        # Set the JWT as a secure, HTTP-only cookie
        response.set_cookie(
            'jwt_token',
            token,
            httponly=True,
            secure=True,  # Set to True in production (HTTPS only)
            samesite='Strict',  # Prevent CSRF attacks
            max_age=timedelta(hours=1).total_seconds()  # Token expires in 1 hour
        )

        return response


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate required fields
        if not email or not password:
            return make_response(jsonify({'message': 'Missing email or password'}), 400)

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if not user or not user.check_password(password):
            return make_response(jsonify({'message': 'Invalid email or password'}), 401)

        # Generate a JWT token for the authenticated user
        token = generate_token(user.id, user.role)

        # Create a response and set the JWT as a cookie
        response = make_response(jsonify({
            'user': user.to_dict()  # Return user data (excluding password)
        }), 200)

        # Set the JWT as a secure, HTTP-only cookie
        response.set_cookie(
            'jwt_token',
            token,
            httponly=True,
            secure=True,  # Set to True in production (HTTPS only)
            samesite='Strict',  # Prevent CSRF attacks
            max_age=timedelta(hours=1).total_seconds()  # Token expires in 1 hour
        )

        return response


class CheckSessionResource(Resource):
    def get(self):
        """
        Check if the user is authenticated by verifying the JWT cookie.
        """
        # Get the JWT token from the cookie
        token = request.cookies.get('jwt_token')

        if not token:
            return make_response(jsonify({'message': 'Not authenticated'}), 401)

        # Decode the token
        payload = decode_token(token)
        if not payload:
            return make_response(jsonify({'message': 'Invalid or expired token'}), 401)

        # Fetch the user from the database
        user = User.query.get(payload['user_id'])
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        # Return the user's data
        return make_response(jsonify({
            'user': user.to_dict()  # Return user data (excluding password)
        }), 200)


class LogoutResource(Resource):
    def delete(self):
        """
        Log out the user by clearing the JWT cookie.
        """
        # Create a response and clear the JWT cookie
        response = make_response(jsonify({'message': 'Logged out successfully'}), 200)
        response.set_cookie(
            'jwt_token',
            '',
            httponly=True,
            secure=True,  # Set to True in production (HTTPS only)
            samesite='None',  # Prevent CSRF attacks
            expires=0  # Expire the cookie immediately
        )

        return response