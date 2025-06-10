import pytest
from chat.models import Thread, Message
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_thread(auth_client, user2):
    response = auth_client.post('/api/threads/', {'receiver_id': user2.id})
    assert response.status_code == 201
    assert response.data['participants']
    assert user2.username in [p['username'] for p in response.data['participants']]


@pytest.mark.django_db
def test_create_thread_with_self(auth_client, user1):
    response = auth_client.post('/api/threads/', {'receiver_id': user1.id})
    assert response.status_code == 400
    assert "yourself" in str(response.data).lower()


@pytest.mark.django_db
def test_create_same_thread_twice(auth_client, user2):
    response1 = auth_client.post('/api/threads/', {'receiver_id': user2.id})
    response2 = auth_client.post('/api/threads/', {'receiver_id': user2.id})
    assert response1.data['id'] == response2.data['id']


@pytest.mark.django_db
def test_list_threads(auth_client, user2):
    auth_client.post('/api/threads/', {'receiver_id': user2.id})
    response = auth_client.get('/api/threads/')
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)


@pytest.mark.django_db
def test_create_message(auth_client, user2):
    thread_resp = auth_client.post('/api/threads/', {'receiver_id': user2.id})
    thread_id = thread_resp.data['id']
    message_resp = auth_client.post(f'/api/threads/{thread_id}/messages/', {'text': 'Hello'})
    assert message_resp.status_code == 201
    assert message_resp.data['text'] == 'Hello'


@pytest.mark.django_db
def test_list_messages(auth_client, user2):
    thread = auth_client.post('/api/threads/', {'receiver_id': user2.id}).data
    auth_client.post(f"/api/threads/{thread['id']}/messages/", {'text': 'Hi!'})
    response = auth_client.get(f"/api/threads/{thread['id']}/messages/")
    assert response.status_code == 200
    assert len(response.data['results']) >= 1


@pytest.mark.django_db
def test_mark_message_as_read(auth_client, user2):
    thread = auth_client.post('/api/threads/', {'receiver_id': user2.id}).data
    msg = auth_client.post(f"/api/threads/{thread['id']}/messages/", {'text': 'Hello'}).data
    mark_resp = auth_client.post(f"/api/threads/{thread['id']}/messages/{msg['id']}/mark_as_read/")
    assert mark_resp.status_code == 200
    assert mark_resp.data['status'] == 'marked as read'


@pytest.mark.django_db
def test_unread_count(auth_client, user2):
    thread = auth_client.post('/api/threads/', {'receiver_id': user2.id}).data
    auth_client.post(f"/api/threads/{thread['id']}/messages/", {'text': 'Unread'})
    response = auth_client.get(f"/api/threads/{thread['id']}/messages/unread-count/")
    assert response.status_code == 200
    assert 'unread_count' in response.data


@pytest.mark.django_db
def test_thread_access_denied(api_client, user1, user2):
    thread = Thread.objects.create()
    thread.participants.set([user1, user2])
    other = User.objects.create_user(username="hacker", password="123")
    api_client.force_authenticate(user=other)
    resp = api_client.get(f"/api/threads/{thread.id}/")
    assert resp.status_code == 404 or resp.status_code == 403


@pytest.mark.django_db
def test_delete_thread(auth_client, user2):
    thread = auth_client.post('/api/threads/', {'receiver_id': user2.id}).data
    resp = auth_client.delete(f"/api/threads/{thread['id']}/")
    assert resp.status_code == 204
    assert not Thread.objects.filter(id=thread['id']).exists()
