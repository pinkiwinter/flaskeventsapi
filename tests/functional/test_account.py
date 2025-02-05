def test_account(client, first_user_access_token):
    response = client.get('/account/', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 200

def test_my_participations(client, first_user_access_token):
    response = client.get('/account/participations', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 200

def test_my_reviews(client, first_user_access_token):
    response = client.get('/account/reviews', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 200

def test_my_reviews(client, first_user_access_token):
    response = client.get('/account/reviews', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 200

def test_my_events(client, first_user_access_token):
    response = client.get('/account/events', headers={'Authorization': f'Bearer {first_user_access_token}'})
    assert response.status_code == 200
