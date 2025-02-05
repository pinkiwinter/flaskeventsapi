from marshmallow import Schema, fields

class ParticipationS(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    event_id = fields.Integer(dump_only=True)

    class Meta:
        ordered = True