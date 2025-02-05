from marshmallow import Schema, fields, validate

class UserS(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=1, max=30))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=120))
    is_admin = fields.Boolean(dump_only=True, load_default=False)

    class Meta:
        ordered = True