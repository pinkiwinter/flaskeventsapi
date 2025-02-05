from app.models import Event
from app import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from dateutil.parser import parse
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth import get_current_user, get_event_with_host
from app.schemas import EventS

events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.route('/add', methods=['POST'])
@jwt_required()
def add_event():
    user = get_current_user()
    try:

        data = EventS().load(request.get_json())
        if not data:
            return jsonify({'error': 'No data.'}), 404

        title = data.get('title')
        description = data.get('description')
        start_time = data.get('start_time')

        if start_time:
            try:
                start_time_parsed = parse(start_time, dayfirst=True)
                if start_time_parsed <= datetime.utcnow():
                    return jsonify({'error': 'Event start time must be in the future.'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid start time format. Expected format: DD/MM/YYYY HH:MM.'}), 400

        event = Event(host_id=user.id, title=title, description=description, start_time=start_time_parsed)

        db.session.add(event)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'An error ocurred while saving the event. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({
        'host': user.username,
        'title': event.title,
        'description': event.description,
        'start_time': event.start_time,
        'status': event.status
    }), 201

    
@events_bp.route('/<int:event_id>/start', methods=['POST'])
@jwt_required()
def start_event(event_id):
    user = get_jwt_identity()
    event = get_event_with_host(event_id, user)

    try:

        if event.status == 'Finished':
            return jsonify({'error': 'Event has already finished.'}), 400
        
        if event.status == 'Active':
            return jsonify({'error': 'Event is already active'}), 400
        
        event.status = 'Active'

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'An error ocurred while updating the event status. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({'message': f'Event with id {event_id} has been started.'}), 200


@events_bp.route('/<int:event_id>/end', methods=['POST'])
@jwt_required()
def end_event(event_id):
    user = get_jwt_identity()
    event = get_event_with_host(event_id, user)

    try:
    
        if event.status == 'Not started':
            return jsonify({'error': 'Event is not active and cannot be finished.'}), 400

        if event.status == 'Finished':
            return jsonify({'error': 'Event has already finished.'}), 400
        
        event.status = 'Finished'
        event.ended_at = parse(str(datetime.utcnow())[:-7], dayfirst=True)

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the event status. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({'message': f'Event with id {event_id} has been finished.'}), 200


@events_bp.route('/<int:event_id>/edit', methods=['PUT'])
@jwt_required()
def edit_event(event_id):
    user = get_current_user()
    event = get_event_with_host(event_id, user.id)

    try:

        data = EventS(partial=True).load(request.get_json())
        if not data:
            return jsonify({'error': 'No data.'}), 404

        title = data.get('title')
        description = data.get('description')

        time_now = datetime.utcnow()
        if not time_now < event.start_time - timedelta(minutes=30):
            return jsonify({'error': 'Event cannot be modified less than 30 minutes before it starts'}), 400
        
        if title:
            event.title = title
        if description:
            event.description = description

        db.session.commit()

    except SQLAlchemyError:
       db.session.rollback()
       return jsonify({'error': 'An error occurred while updating the event. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({
        'host': user.username,
        'title': event.title,
        'descripton': event.description,
        'start_time': event.start_time,
        'status': event.status
    }), 200


@events_bp.route('/<int:event_id>/cancel', methods=['DELETE'])
@jwt_required()
def cancel_event(event_id):
    user = get_jwt_identity()
    event = get_event_with_host(event_id, user)

    try:

        if event.status == 'Finished':
            return jsonify({'error': 'Event has already finished and cannot be canceled.'}), 400
        
        if event.status == 'Active':
            return jsonify({'error': 'Event has already started and cannot be canceled.'}), 400

        db.session.delete(event)
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while canceling the event. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({'message': f'Event with id {event_id} has been canceled.'}), 200


# @events_bp.route('/all', methods=['GET'])
# @jwt_required()
# def get_events():
#     try:

#         args = EventS(partial=True).load(request.args)

#         host_id = args.get('host_id')
#         title = args.get('title')
#         start_time = args.get('start_time')
#         status = args.get('status')
        
#         query = Event.query

#         if host_id:
#             query = query.filter(Event.host_id==int(host_id))

#         if title:
#             query = query.filter(Event.title.ilike(f'%{title}%'))

#         if status:
#             query = query.filter(Event.status.ilike(f'%{status}%'))

#         if start_time:
#             try:
#                 parsed_start_time = parse(start_time)
#                 # query = query.filter(Event.start_time.ilike(f'%{parsed_start_time}%'))
#                 query = query.filter(Event.start_time >= parsed_start_time)
#             except ValueError:
#                 return jsonify({'error': 'Invalid format. Standart: DD/MM/YYYY HH:MM.'}), 400
        
#         events = query.all()

#     except Exception as e:
#         return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400
    
#     return jsonify([{
#         'id': event.id,
#         'host_id': event.host_id,
#         'title': event.title,
#         'description': event.description,
#         'start_time': event.start_time,
#         'ended_at': event.ended_at,
#         'status': event.status,
#         'total_participants': event.total_participants,
#         'total_reviews': event.total_reviews,
#     } for event in events]), 200

