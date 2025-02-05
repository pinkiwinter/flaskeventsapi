from app.models import Review
from app import db
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth import get_current_user, get_event
from app.auth import get_event
from app.schemas import ReviewS

review_bp = Blueprint('reviews', __name__, url_prefix='/events')

@review_bp.route('/<int:event_id>/review/add', methods=['POST'])
@jwt_required()
def add_review(event_id):
    user  = get_jwt_identity()
    event = get_event(event_id)

    try:

        data = ReviewS().load(request.get_json())
        if not data:
            return jsonify({'error': 'No data.'}), 400

        comment = data.get('comment')
        rating = data.get('rating')

        if event.status in ['Active', 'Not started']:
            return jsonify({'error': 'You cannot leave a review until the event has finished.'}), 400

        if event.host_id == user:
            return jsonify({'error': 'You cant leave review for your own event.'}), 400
        
        if Review.query.filter_by(user_id=user, event_id=event_id).first():
            return jsonify({'error': 'You cannot leave more than one review for a single event.'}), 400

        review = Review(event_id=event_id, user_id=user, comment=comment, rating=rating)

        db.session.add(review)

        event.total_reviews += 1

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error, please try again later.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({
        'id': review.id,
        'event_id': review.event_id,
        'user_id': review.user_id,
        'comment': review.comment,
        'rating': review.rating
    }), 201


@review_bp.route('/<int:event_id>/review/delete', methods=['DELETE'])
@jwt_required()
def delete_review(event_id):
    user = get_jwt_identity()
    event = get_event(event_id)
    review = Review.query.filter_by(user_id=user, event_id=event_id).first()

    try:

        if review is None:
            return jsonify({'error': 'Review not found'}), 404

        db.session.delete(review)

        event.total_reviews -= 1

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error, please try again later.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({'message': f'Successfully deleted review under event with id {event_id}.'}), 200

    

@review_bp.route('/<int:event_id>/review/all', methods=['GET'])
@jwt_required()
def get_reviews(event_id):
    reviews = Review.query.filter_by(event_id=event_id).all()
    rating = ReviewS(partial=True).load(request.args).get('rating')

    try:

        if rating:
            reviews = Review.query.filter_by(event_id=event_id, rating=rating).all()

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify([{
        'id': r.id,
        'user_id': r.user_id,
        'comment': r.comment,
        'rating': r.rating
    } for r in reviews]), 200