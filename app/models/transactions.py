# from app.extensions import db
# from sqlalchemy.orm import validates

# class Transaction(db.Model):
#     __tablename__ = 'transactions'

#     id = db.Column(db.Integer, primary_key=True)
#     booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
#     amount_paid = db.Column(db.Float, nullable=False)
#     payment_date = db.Column(db.DateTime, nullable=False)
#     payment_method = db.Column(db.String(50), nullable=False)  # e.g., M-Pesa, Credit Card

#     # Relationships
#     booking = db.relationship('Booking', back_populates='transaction')



#     def to_dict(self):
#         return {
#             "id": self.id,
#             "booking_id": self.booking_id,
#             "amount_paid": self.amount_paid,
#             "payment_date": self.payment_date.isoformat(),
#             "payment_method": self.payment_method,
#             "booking": self.booking.to_dict() if self.booking else None
#         }

#     @validates('amount_paid')
#     def validate_amount_paid(self, key, amount_paid):
#         if amount_paid < 0:
#             raise ValueError("Amount paid cannot be negative.")
#         return amount_paid

#     @validates('payment_method')
#     def validate_payment_method(self, key, payment_method):
#         if payment_method not in ['M-Pesa', 'Credit Card', 'PayPal']:
#             raise ValueError("Invalid payment method.")
#         return payment_method

#     def __repr__(self):
#         return f'<Transaction {self.id}>'