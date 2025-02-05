from . import db
from dateutil.parser import parse

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    ended_at = db.Column(db.DateTime, default=None)
    status = db.Column(db.String, default='Not started')
    total_participants = db.Column(db.Integer, default=0)
    total_reviews = db.Column(db.Integer, default=0)

    participations = db.relationship('Participation', backref='event', lazy=True)
    reviews = db.relationship('Review', backref='event', lazy=True)
