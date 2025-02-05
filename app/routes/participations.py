from app.models import Participation
from app import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth import get_current_user, get_event
from marshmallow import ValidationError

participation_bp = Blueprint('participations', __name__, url_prefix='/events')

@participation_bp.route('/<int:event_id>/participation/sign', methods=['POST'])
@jwt_required()
def participate(event_id):
    user = get_jwt_identity()
    event = get_event(event_id)

    try:

        if event.host_id == user:
            return jsonify({'error': 'You already host this event.'}), 400

        if event.status in ['Active', 'Finished']:
            return jsonify({'error': 'Event cannot be participate because it has already started or has finished.'}), 400

        if not datetime.utcnow() < event.start_time - timedelta(minutes=30):
            return jsonify({'error': 'Event cannot be participate less than 30 minutes before it starts.'}), 400

        if Participation.query.filter_by(user_id=user, event_id=event.id).first():
            return jsonify({'error': 'You are already participating in this event.'}), 400

        participation = Participation(user_id=user, event_id=event.id)

        db.session.add(participation)

        event.total_participants += 1

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error, please try again later.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({'message': 'Successfully participated in the event.'}), 200


@participation_bp.route('/<int:event_id>/participation/cancel', methods=['DELETE'])
@jwt_required()
def cancel_participation(event_id):
    user = get_jwt_identity()
    event = get_event(event_id)
    participation = Participation.query.filter_by(user_id=user, event_id=event.id).first()

    try:

        if event.host_id == user:
            return jsonify({'error': 'You host this event.'}), 400

        if participation is None:
            return jsonify({'error': 'Participation not found.'}), 404

        db.session.delete(participation)

        event.total_participants -= 1

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error, please try again later.'}), 500

    return jsonify({'message': 'Successfully canceled participation in the event.'}), 200
