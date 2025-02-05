from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db
from app.models import User
from app.schemas import UserS
from sqlalchemy.exc import SQLAlchemyError

register_bp = Blueprint('register', __name__)
login_bp = Blueprint('login', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    try:

        data = UserS().load(request.get_json())
        if not data:
            return jsonify({'error': 'No data.'}), 400

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User with this email already exists.'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'User with this username already exists.'}), 400
        
        hashed_password = generate_password_hash(password)

        user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error, please try again later.'}), 500
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify({
        'username': user.username,
        'email': user.email
    }), 201


@login_bp.route('/login', methods=['POST'])
def login():
    try:

        data = UserS(partial=True).load(request.get_json())
        if not data:
            return jsonify({'error': 'No data.'}), 400

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Invalid email or password.'}), 400
        
        access_token = create_access_token(identity=user.id)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400

    return jsonify(access_token=access_token), 200