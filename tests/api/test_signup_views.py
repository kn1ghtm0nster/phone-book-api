import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase, APIClient


pytestmark = pytest.mark.django_db


"""
FIXTURES
"""


"""
TESTS
"""


class TestSignUpAPIView(APITestCase):

    def setUp(self):
        self.url = reverse('user-signup')
        self.api_client: APIClient = APIClient()
        self.client = self.api_client

    def test_signup_successful(self):
        payload = {
            "username": "newuser1",
            "password": "StrongPass!23",
            "first_name": "New",
            "last_name": "User"
        }
        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 201  # type: ignore
        data = response.json()
        assert data['username'] == "newuser1"
        assert 'access_token' in data

        # ensure the user was actually created in the DB.
        User = get_user_model()
        user_exists = User.objects.filter(username="newuser1").exists()
        assert user_exists

        user = User.objects.get(username="newuser1")
        assert user.first_name == "New"
        assert user.last_name == "User"

        reader_group = Group.objects.get(name='reader')
        assert reader_group in user.groups.all()

    def test_signup_without_optional_fields(self):
        payload = {
            "username": "newuser2",
            "password": "AnotherStrongPass!45"
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 201  # type: ignore
        data = response.json()
        assert data['username'] == "newuser2"
        assert 'access_token' in data

        # ensure the user was actually created in the DB.
        User = get_user_model()
        user_exists = User.objects.filter(username="newuser2").exists()
        assert user_exists

        user = User.objects.get(username="newuser2")
        assert user.first_name == ""
        assert user.last_name == ""

        reader_group = Group.objects.get(name='reader')
        assert reader_group in user.groups.all()

    def test_signup_duplicate_username(self):
        User = get_user_model()
        User.objects.create_user(
            username="existinguser", password="SomePass!67")

        payload = {
            "username": "existinguser",
            "password": "NewPass!89"
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore
        data = response.json()
        assert 'username' in data
        assert data['username'] == ["Username is already taken."]

    def test_signup_weak_password(self):
        payload = {
            "username": "weakpassworduser",
            "password": "123"
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore
        data = response.json()
        assert 'password' in data

    def test_signup_missing_username(self):
        payload = {
            "password": "ValidPass!23"
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore
        data = response.json()
        assert 'username' in data

    def test_signup_missing_password(self):
        payload = {
            "username": "userwithoutpassword"
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore
        data = response.json()
        assert 'password' in data

    def test_signup_invalid_username(self):
        payload = {
            'username': '<script>alert(1)</script>',
            'password': 'ValidPass!23'
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore

        data = response.json()
        assert data['username'] == ["Invalid username."]

    def test_signup_invalid_password(self):
        payload = {
            'username': 'validusername',
            'password': '<script>alert(1)</script>'
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore

        data = response.json()
        assert data['password'] == ["Invalid characters in password."]

    def test_signup_whitespace_username(self):
        payload = {
            'username': ' username ',
            'password': 'ValidPass!23'
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 201  # type: ignore

        data = response.json()
        assert data['username'] == 'username'
        assert 'access_token' in data

    def test_signup_invalid_first_name(self):
        resp = self.client.post(self.url, data={
            "username": "alice", "password": "StrongPass!234", "first_name": "<script>"}, format="json")
        assert resp.status_code == 400
        assert "first_name" in resp.json()

    def test_signup_invalid_last_name(self):
        resp = self.client.post(self.url, data={
            "username": "alice", "password": "StrongPass!234", "last_name": "O''Malley--"}, format="json")
        assert resp.status_code == 400
        assert "last_name" in resp.json()

    def test_signup_sql_injection_username(self):
        payload = {
            'username': "user'; DROP TABLE auth_user;--",
            'password': 'ValidPass!23'
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore

        data = response.json()
        assert data['username'] == ["Invalid username."]

    def test_signup_sql_injection_password(self):
        payload = {
            'username': 'validuser',
            'password': "pass'; DROP TABLE auth_user;--"
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore

        data = response.json()
        assert data['password'] == ["Invalid password."]

    def test_signup_sql_injection_first_name(self):
        payload = {
            'username': 'validuser',
            'password': 'ValidPass!23',
            'first_name': "John'; DROP TABLE auth_user;--"
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore

        data = response.json()
        assert data['first_name'] == ["Invalid characters in name."]

    def test_signup_sql_injection_last_name(self):
        payload = {
            'username': 'validuser',
            'password': 'ValidPass!23',
            'last_name': "Doe'; DROP TABLE auth_user;--"
        }

        response = self.client.post(self.url, data=payload, format='json')
        assert response.status_code == 400  # type: ignore
        data = response.json()

        assert data['last_name'] == ["Invalid characters in name."]
