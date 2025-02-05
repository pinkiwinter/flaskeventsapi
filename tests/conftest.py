import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import create_app, db
import os
from app.models import User, Event, Participation, Review

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = os.getenv('TEST_JWT_SECRET_KEY')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_database():
    yield
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

@pytest.fixture
def first_user():
    hashed_password = generate_password_hash('12345678')
    user = User(username='John', email='johndoe@gmail.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def second_user():
    hashed_password = generate_password_hash('12345678')
    user = User(username='Jane', email='janedoe@gmail.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def first_event(first_user):
    event = Event(host_id=first_user.id, title='Pulse', description='Beat-driven fun and electrifying energy.', start_time=datetime(2025, 11, 10, 3, 15))
    db.session.add(event)
    db.session.commit()
    return event

@pytest.fixture
def finished_event(first_user):
    event = Event(host_id=first_user.id, title='Finished event', description='This event is finished.', start_time=datetime(2024, 11, 10, 3, 15), status='Finished')
    db.session.add(event)
    db.session.commit()
    return event

@pytest.fixture
def active_event(first_user):
    event = Event(host_id=first_user.id, title='Active event', description='This event is active.', start_time=datetime(2024, 11, 10, 3, 15), status='Active')
    db.session.add(event)
    db.session.commit()
    return event

@pytest.fixture
def starting_soon_event(first_user):
    event = Event(host_id=first_user.id, title='Starting soon event', description='This event is starting soon.', start_time=datetime.utcnow() + timedelta(minutes=25), status='Not Started')
    db.session.add(event)
    db.session.commit()
    return event

@pytest.fixture
def second_user_participation(second_user, first_event):
    participation = Participation(user_id=second_user.id, event_id=first_event.id)
    db.session.add(participation)
    db.session.commit()
    return participation

@pytest.fixture
def second_user_review(finished_event, second_user):
    review = Review(event_id=finished_event.id, user_id=second_user.id, comment='Amazing event!', rating='5/5')
    db.session.add(review)
    db.session.commit()
    return review

@pytest.fixture
def first_user_access_token(client, first_user):
    response = client.post('/login', json={'email': 'johndoe@gmail.com', 'password': '12345678'})
    assert response.status_code == 200
    access_token = response.json['access_token']
    return access_token
    
@pytest.fixture
def second_user_access_token(client, second_user):
    response = client.post('/login', json={'email': 'janedoe@gmail.com', 'password': '12345678'})
    assert response.status_code == 200
    access_token = response.json['access_token']
    return access_token