from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models here
from .models import Bus, User, Transaction, Booking



# Optional: Export models for easier access
__all__ = ["Bus",  "User", "Transaction", "Booking"]

