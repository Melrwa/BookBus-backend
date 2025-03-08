from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models here
from .bus import Bus
from .user import User
from .transactions import Transaction
from .bookings import Booking


# Optional: Export models for easier access
__all__ = ["Bus",  "User", "Transaction", "Booking"]

