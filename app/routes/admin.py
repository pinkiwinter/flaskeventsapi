from app.models import Review
from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.auth import get_event, admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/<int:event_id>/delete', methods=['DELETE'])
@jwt_required()
@admin_required
def admin_delete_event(event_id):
    event = get_event(event_id)

    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event has been deleted.'}), 204
    

@admin_bp.route('/review/<int:review_id>/delete', methods=['DELETE'])
@jwt_required()
@admin_required
def admin_delete_review(review_id):
    review = Review.query.filter_by(id=review_id).first()

    if review is None:
        return jsonify({'error': 'Review not found'}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review has been deleted.'}), 204