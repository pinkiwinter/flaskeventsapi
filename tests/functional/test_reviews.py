def test_add_review(client, finished_event, second_user_access_token):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'comment': 'Amazing event!', 'rating': '5'})
    assert response.status_code == 201
    assert finished_event.total_reviews == 1 # +1 (0 + 1)

def test_delete_review(client, finished_event, second_user_access_token, second_user_review):
    response = client.delete(f'/events/{finished_event.id}/review/delete', headers={'Authorization': f'Bearer {second_user_access_token}'})
    assert response.status_code == 200
    assert finished_event.total_reviews == -1 # 0 (1 - 1)