from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth import get_current_user

account__bp = Blueprint('account', __name__, url_prefix='/account')

@account__bp.route('/', methods=['GET'])
@jwt_required()
def me():
    user = get_current_user()

    return ({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': '*' * len(user.password),
        'is_admin': user.is_admin
    }), 200

@account__bp.route('/participations', methods=['GET'])
@jwt_required()
def my_participations():
    user = get_current_user()
    events = user.participations

    return jsonify([{
        'id': e.id,
        'host_id': e.host_id,
        'title': e.title,
        'description': e.description,
        'start_time': e.start_time,
        'status': e.status,
        'total_participants': e.total_participants,
    } for e in events]), 200

@account__bp.route('/reviews', methods=['GET'])
@jwt_required()
def my_reviews():
    user = get_current_user()

    reviews = user.reviews

    return jsonify([{
        'id': r.id,
        'event_id': r.event_id,
        'comment': r.comment,
        'rating': r.rating
    } for r in reviews]), 200

@account__bp.route('/events', methods=['GET'])
@jwt_required()
def my_events():
    user = get_current_user()

    events = user.events

    return jsonify([{
        'title': e.title,
        'description': e.description,
        'start_time': e.start_time,
        'status': e.status,
        'total_participants': e.total_participants,
        'total_reviews': e.total_reviews
    } for e in events]), 200