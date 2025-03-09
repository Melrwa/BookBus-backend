from flask import request, jsonify
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

        if not name or not email or not password:
            return {'message': 'Missing required fields'}, 400

        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400

        user = User(name=name, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        token = generate_token(user.id, user.role)
        return {'token': token, 'user': user.to_dict()}, 201  # Use .to_dict() instead of user_schema.dump(user)

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Missing email or password'}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid email or password'}, 401

        token = generate_token(user.id, user.role)
        return {'token': token, 'user': user.to_dict()}, 200  # Use .to_dict() instead of user_schema.dump(user)