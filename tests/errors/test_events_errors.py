def test_add_event_missing_title(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'description': 'My first event description!', 'start_time': '10/11/2025 03:15'})
    assert response.status_code == 400

def test_add_event_missing_description(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'First event', 'start_time': '10/11/2025 03:15'})
    assert response.status_code == 400

def test_add_event_missing_start_time(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'First event', 'description': 'My first event description!'})
    assert response.status_code == 400

def test_add_event_title_min_length(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'hi', 'description': 'My first event description!', 'start_time': '10/11/2027 03:15'})
    assert response.status_code == 400

def test_add_event_title_max_length(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'description': 'My first event description!', 'start_time': '10/11/2025 03:15'})
    assert response.status_code == 400

def test_add_event_description_max_length(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'First event', 'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure.', 'start_time': '10/11/2025 03:15'})
    assert response.status_code == 400

def test_add_event_invalid_start_time(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'First event', 'description': 'My first event description!', 'start_time': 'invalid_date_string'})
    assert response.status_code == 400

def test_add_event_invalid_start_time_past(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'First event', 'description': 'My first event description!', 'start_time': '10/11/2012 03:15'})
    assert response.status_code == 400