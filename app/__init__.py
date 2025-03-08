from flask import Flask
from flask_cors import CORS
from .config import Config
from flask_restful import Api
from .extensions import db, migrate, bcrypt
from .routes.auth_routes import RegisterResource, LoginResource
from .routes.admin_routes import AddDriverResource, ViewAllUsersResource, ViewAllBookingsResource, ViewAllTransactionsResource


def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    api = Api(app)

    CORS(
        app,
        origins=app.config["CORS_ORIGINS"],
        methods=app.config["CORS_METHODS"],
        allow_headers=app.config["CORS_ALLOW_HEADERS"],
        supports_credentials=True,  # Allow credentials (e.g., cookies, authorization headers)
    )


    # Register routes
    api.add_resource(RegisterResource, '/register')
    api.add_resource(LoginResource, '/login')
    api.add_resource(AddDriverResource, '/admin/add_driver')
    api.add_resource(ViewAllUsersResource, '/admin/users')
    api.add_resource(ViewAllBookingsResource, '/admin/bookings')
    api.add_resource(ViewAllTransactionsResource, '/admin/transactions')

    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    return app