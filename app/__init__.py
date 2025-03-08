from flask import Flask
from .config import Config
from .extensions import db, migrate, bcrypt

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    

    # Register blueprints (if any)
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    # Create database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    return app