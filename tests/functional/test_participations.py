def test_participate(client, first_event, second_user_access_token):
    response = client.post(f'/events/{first_event.id}/participation/sign', headers={'Authorization': f'Bearer {second_user_access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Successfully participated in the event.'
    assert first_event.total_participants == 1 # +1 (0 + 1)
    
def test_cancel_participation(client, first_event, second_user_access_token, second_user_participation):
    response = client.delete(f'/events/{int(first_event.id)}/participation/cancel', headers={'Authorization': f'Bearer {second_user_access_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Successfully canceled participation in the event.'
    assert first_event.total_participants == -1 # 0 (1 - 1)