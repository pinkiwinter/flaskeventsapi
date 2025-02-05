def test_register_missing_args(client):
    response = client.post('/register', json={})
    assert response.status_code == 400

def test_register_email_pattern(client):
    response = client.post('/register', json={'username': 'user1', 'email': 'user1@.com', 'password': '12345678'})
    assert response.status_code == 400

def test_register_password_length(client):
    response = client.post('/register', json={'username': 'user1', 'email': 'pluh@email.com', 'password': '12345'})
    assert response.status_code == 400

def test_register_username_exists(client, first_user):
    response = client.post('/register', json={'username': 'John', 'email': 'pluh@email.com', 'password': '12345678'})
    assert response.status_code == 400
    assert response.json['error'] == 'User with this username already exists.'

def test_register_email_exists(client, first_user):
    response = client.post('/register', json={'username': 'user1', 'email': 'johndoe@gmail.com', 'password': '12345678'})
    assert response.status_code == 400
    assert response.json['error'] == 'User with this email already exists.'
