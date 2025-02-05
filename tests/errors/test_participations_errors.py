def test_participate_user_is_host(client, first_user_access_token, first_event):
    response = client.post(f'/events/{first_event.id}/participation/sign', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 400
    assert response.json['error'] == 'You already host this event.'

def test_participate_event_is_active(client, second_user_access_token, active_event):
    response = client.post(f'/events/{active_event.id}/participation/sign', headers={'Authorization': f'Bearer {second_user_access_token}'})
    assert response.status_code == 400
    assert response.json['error'] == 'Event cannot be participate because it has already started or has finished.'

def test_participate_event_is_finished(client, second_user_access_token, finished_event):
    response = client.post(f'/events/{finished_event.id}/participation/sign', headers={'Authorization': f'Bearer {second_user_access_token}'})
    assert response.status_code == 400
    assert response.json['error'] == 'Event cannot be participate because it has already started or has finished.'

def test_paticipate_event_user_is_late(client, second_user_access_token, starting_soon_event):
    response = client.post(f'/events/{starting_soon_event.id}/participation/sign', headers={'Authorization': f'Bearer {second_user_access_token}'})
    assert response.status_code == 400
    assert response.json['error'] == 'Event cannot be participate less than 30 minutes before it starts.'

def test_participate_already_participating(client, second_user_access_token, first_event, second_user_participation):
    response = client.post(f'/events/{first_event.id}/participation/sign', headers={'Authorization': f'Bearer {second_user_access_token}'})
    assert response.status_code == 400
    assert response.json['error'] == 'You are already participating in this event.'

def test_cancel_participation_user_is_host(client, first_event, first_user_access_token):
    response = client.delete(f'/events/{first_event.id}/participation/cancel', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 400
    assert response.json['error'] == 'You host this event.'
