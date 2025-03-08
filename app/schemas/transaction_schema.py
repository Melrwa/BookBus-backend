from marshmallow import Schema, fields, validate

class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    booking_id = fields.Int(required=True)
    amount_paid = fields.Float(required=True, validate=validate.Range(min=0))
    payment_date = fields.DateTime(required=True)
    payment_method = fields.Str(required=True, validate=validate.OneOf(['M-Pesa', 'Credit Card', 'PayPal']))

    class Meta:
        fields = ('id', 'booking_id', 'amount_paid', 'payment_date', 'payment_method')