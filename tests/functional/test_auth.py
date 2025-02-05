from app.models import User

def test_register(client):
    response = client.post('/register', json={'username': 'Yui', 'email': 'yui@email.com', 'password': '1234123213123123'})
    assert response.status_code == 201

    user = User.query.filter_by(email='yui@email.com').first()
    assert user is not None
    assert user.username == 'Yui'

def test_login(client, first_user):
    response = client.post('/login', json={'email': 'johndoe@gmail.com', 'password': '12345678'})
    assert response.status_code == 200
    assert 'access_token' in response.json

    access_token = response.json.get('access_token')
    assert access_token is not None