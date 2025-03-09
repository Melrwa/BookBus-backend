from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret_key")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

    JWT_TOKEN_LOCATION = ["cookies", "headers"]  # Store tokens in cookies and headers
    JWT_COOKIE_SECURE = True  # Set to True in production (HTTPS only)
    JWT_COOKIE_CSRF_PROTECT = False  # Set to True if using CSRF protection
    JWT_ACCESS_COOKIE_NAME = 'access_token'
    JWT_COOKIE_SAMESITE = 'None'  # Prevents cookies from being sent in cross-site requests
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token expires in 24 hours


    CORS_HEADERS = "Content-Type"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5001,http://localhost:3000").split(",")  # List of allowed origins
    CORS_METHODS = os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE,OPTIONS").split(",")  # Allowed HTTP methods
    CORS_ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS", "Content-Type,Authorization").split(",")  # Allowed headers
    
    PAGINATION_PER_PAGE = int(os.getenv("PAGINATION_PER_PAGE", 10))  # Default items per page
    PAGINATION_MAX_PER_PAGE = int(os.getenv("PAGINATION_MAX_PER_PAGE", 100))  # Max items per page



    NEXT_PUBLIC_BACKEND_URL = os.getenv("NEXT_PUBLIC_BACKEND_URL")


  

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Dictionary to select the configuration based on ENV
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}