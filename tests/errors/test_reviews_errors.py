def test_add_review__required_comment(client, second_user_access_token, finished_event):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'rating': '5'})
    assert response.status_code == 400

def test_add_review__required_rating(client, second_user_access_token, finished_event):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'comment': 'Amazing event!'})
    assert response.status_code == 400

def test_add_review__comment_too_long(client, second_user_access_token, finished_event):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'comment': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vehicula, libero in tincidunt lobortis, urna purus dapibus ante, a hendrerit arcu velit at erat. Vivamus sit amet volutpat elit. Nullam auctor massa vel tristique lacinia. Quisque euismod, leo at malesuada facilisis, urna erat maximus elit, a euismod libero augue at nisi. Nam euismod nunc id tortor tincidunt auctor. Integer volutpat, neque nec efficitur feugiat, leo sapien tempor neque, ac venenatis neque magna sit amet ipsum. Sed viverra felis a metus efficitur, non vehicula odio dapibus. Aliquam erat volutpat. Integer posuere metus non augue vulputate, vitae vestibulum justo blandit. Ut pretium metus id ante fermentum, et elementum nulla malesuada.', 'rating': '5'})
    assert response.status_code == 400

def test_add_review__rating_too_low(client, second_user_access_token, finished_event):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'comment': 'Amazing event!', 'rating': '0'})
    assert response.status_code == 400
   
def test_add_review__rating_too_high(client, second_user_access_token, finished_event):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'comment': 'Amazing event!', 'rating': '6'})
    assert response.status_code == 400

def test_add_review__rating_is_str(client, second_user_access_token, finished_event):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'comment': 'Amazing event!', 'rating':'Wow!'})
    assert response.status_code == 400

def test_add_review__event_is_not_finished(client, second_user_access_token, active_event):
    response = client.post(f'/events/{active_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'comment': 'Amazing event!', 'rating': '5'})
    assert response.status_code == 400
    assert response.json['error'] == 'You cannot leave a review until the event has finished.'

def test_add_review__user_is_host(client, first_user_access_token, finished_event):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {first_user_access_token}'}, json={'comment': 'Amazing event!', 'rating': '5'}) 
    assert response.status_code == 400
    assert response.json['error'] == 'You cant leave review for your own event.'

def test_add_review__reviews_is_more_than_one(client, second_user_access_token, finished_event, second_user_review):
    response = client.post(f'/events/{finished_event.id}/review/add', headers={'Authorization': f'Bearer {second_user_access_token}'}, json={'comment': 'Amazing event!', 'rating': '5'})
    assert response.status_code == 400
    assert response.json['error'] == 'You cannot leave more than one review for a single event.'
