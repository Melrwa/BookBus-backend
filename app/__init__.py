from flask import Flask
from flask_cors import CORS
from .config import Config, config  # Import the config dictionary
from flask_restful import Api
from .extensions import db, migrate, bcrypt, cors, api  # Import all extensions
from .routes.auth_routes import RegisterResource, LoginResource
from app.routes.admin_routes import AddDriverResource, ViewAllUsersResource, ViewAllBookingsResource, ViewAllTransactionsResource, AssignDriverToBusResource, ChangeUserRoleResource,  ViewMyBusesResource
from app.routes.driver_routes import AddBusResource, UpdateBusResource, DeleteBusResource, ScheduleBusResource,  UpdatePriceResource, MyAssignedBusesResource
import os

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Load configuration based on environment
    env = os.getenv("FLASK_ENV", "development")  # Default to development
    app.config.from_object(config[env])  # Load the appropriate config class
    api = Api(app) 
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app)  # Initialize CORS
    api.init_app(app)  # Initialize Flask-RESTful
   

    # Configure CORS
    CORS(
        app,
        origins=app.config["CORS_ORIGINS"],
        methods=app.config["CORS_METHODS"],
        allow_headers=app.config["CORS_ALLOW_HEADERS"],
        supports_credentials=True,  # Allow credentials (e.g., cookies, authorization headers)
    )

    # Register routes
    # Auth Routes
    api.add_resource(RegisterResource, '/register')
    api.add_resource(LoginResource, '/login')

    #Admin Routes
    api.add_resource(AddDriverResource, '/admin/add_driver')
    api.add_resource(ViewAllUsersResource, '/admin/users')
    api.add_resource(ViewAllBookingsResource, '/admin/bookings')
    api.add_resource(ViewAllTransactionsResource, '/admin/transactions')
    api.add_resource(AssignDriverToBusResource, '/admin/assign_driver')
    api.add_resource(ChangeUserRoleResource, '/admin/change_user_role')
    api.add_resource(ViewMyBusesResource,'/admin/my_buses' )

    # Driver Routes
    api.add_resource(AddBusResource, '/driver/add_bus')
    api.add_resource(UpdateBusResource, '/driver/update_bus/<bus_id>')
    api.add_resource(UpdatePriceResource, '/driver/update_price/<bus_id>')
    api.add_resource(DeleteBusResource, '/driver/delete_bus/<bus_id>')
    api.add_resource(ScheduleBusResource, '/driver/schedule_bus/<bus_id>')
    api.add_resource(MyAssignedBusesResource, '/driver/my_assigned_bus?driver_id')


    

   




    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    return app