import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user1(db):
    return User.objects.create_user(username="alice", password="testpass")


@pytest.fixture
def user2(db):
    return User.objects.create_user(username="bob", password="testpass")


@pytest.fixture
def auth_client(api_client, user1):
    api_client.force_authenticate(user=user1)
    return api_client
