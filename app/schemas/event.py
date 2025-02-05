from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime
from flask import jsonify


class EventS(Schema):
    id = fields.Integer()
    host_id = fields.Integer()
    title = fields.String(required=True, validate=validate.Length(min=3, max=120))
    description = fields.String(required=True, validate=validate.Length(min=1, max=240))
    start_time = fields.String(required=True)
    ended_at = fields.DateTime(load_default=None)
    status = fields.String(load_default='Not Started', validate=validate.OneOf(['Not Started', 'Active', 'Finished']))
    total_participants = fields.Integer(load_default=0)
    total_reviews = fields.Integer(load_default=0)

    class Meta:
        ordered = True