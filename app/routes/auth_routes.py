from flask import request, make_response, jsonify
from flask_restful import Resource
from app.models.models import User
from app.extensions import db, bcrypt
from app.utils.jwt_utils import generate_token

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

        # Return the token and user data
        return make_response(jsonify({
            'token': token,
            'user': user.to_dict()  # Use the to_dict() method to serialize the user
        }), 201)

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

        # Return the token and user data
        return make_response(jsonify({
            'token': token,
            'user': user.to_dict()  # Use the to_dict() method to serialize the user
        }), 200)