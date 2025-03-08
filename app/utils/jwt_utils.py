from datetime import datetime, timedelta
import jwt
from flask import current_app

from functools import wraps
from flask import request, jsonify


def generate_token(user_id, role):
    """
    Generates a JWT token for a user.
    """
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    """
    Decodes a JWT token and returns the payload.
    """
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    

def token_required(f):
    """
    Decorator to protect routes with JWT authentication.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'message': 'Invalid or expired token'}), 401

        # Add user info to the request context
        request.current_user = payload
        return f(*args, **kwargs)
    return decorated