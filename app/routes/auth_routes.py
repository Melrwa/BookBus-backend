from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from app.utils.jwt_utils import generate_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'customer')  # Default role is 'customer'

    if not name or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # Generate a token for the new user
    token = user.generate_auth_token()
    return jsonify({'token': token, 'user_id': user.id, 'role': user.role}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Generate a token for the logged-in user
    token = user.generate_auth_token()
    return jsonify({'token': token, 'user_id': user.id, 'role': user.role}), 200