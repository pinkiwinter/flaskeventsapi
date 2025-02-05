from marshmallow import Schema, fields, validate

class ReviewS(Schema):
    id = fields.Integer(dump_only=True)
    event_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    comment = fields.String(required=True, validate=validate.Length(min=1, max=500))
    rating = fields.String(required=True, validate=validate.OneOf(['1', '2', '3', '4', '5']))

    class Meta:
        ordered = True
        
