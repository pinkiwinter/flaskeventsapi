from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    participations = db.relationship('Participation', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    events = db.relationship('Event', backref='user', lazy=True)