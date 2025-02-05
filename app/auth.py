from flask import jsonify
from app.models import User
from app.models import Event
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from datetime import datetime

def get_current_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    return user

def get_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event:
        return event
    else:
        return jsonify({'error': 'Event not found.'}), 404
    
def get_event_with_host(event_id, host_id):
    event = Event.query.filter_by(id=event_id, host_id=host_id).first()
    if event:
        return event
    else:
        return jsonify({'error': 'Event not found.'}), 404

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = get_current_user()

        if user.is_admin:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Access denied.'}), 400
        
    return decorated_function
