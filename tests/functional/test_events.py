from app.models import Event

def test_add_event(client, first_user_access_token):
    response = client.post('/events/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'First event', 'description': 'My first event description!', 'start_time': '10/11/2025 03:15'})
    assert response.status_code == 201

    event = Event.query.filter_by(title='First event').first()
    assert event is not None
    assert event.title == 'First event'

def test_start_event(client, first_event, first_user_access_token):
    response = client.post(f'/events/{first_event.id}/start', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 200
    assert first_event.status == 'Active'
    assert response.json['message'] == f'Event with id {first_event.id} has been started.'

def test_end_event(client, active_event, first_user_access_token):
    response = client.post(f'/events/{active_event.id}/end', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 200
    assert active_event.status == 'Finished'
    assert response.json['message'] == f'Event with id {active_event.id} has been finished.'

def test_edit_event(client, first_event, first_user_access_token):
    response = client.put(f'/events/{first_event.id}/edit', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'title': 'Dreamscape', 'description': 'Step into a world of lights and sound.'})
    assert response.status_code == 200
    assert first_event.title == 'Dreamscape'
    assert first_event.description == 'Step into a world of lights and sound.'

def test_cancel_event(client, first_event, first_user_access_token):
    response = client.delete(f'/events/{first_event.id}/cancel', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == f'Event with id {first_event.id} has been canceled.'

# def test_get_events(client, first_user_access_token, first_event):
#     response = client.get('/events/all', headers={'Authorization': f'Bearer {first_user_access_token}'})
#     # assert response.status_code == 200
#     assert response.json['error'] == 'qweq'