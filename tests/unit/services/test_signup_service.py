import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from phonebook.services import SignUpService

pytestmark = pytest.mark.django_db


"""
FIXTURES
"""


@pytest.fixture
def signup_service():
    return SignUpService()


@pytest.fixture
def user_payload():
    return {
        "username": "testuser",
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "User"
    }


"""
UNIT TESTS
"""


def test_create_user_works(signup_service, user_payload):
    user = signup_service.create_user(**user_payload)

    User = get_user_model()

    assert isinstance(user, User)
    assert user.username == "testuser"
    assert user.first_name == "Test"
    assert user.last_name == "User"

    # Ensure password is hashed and valid
    assert user.password != "securepassword123"
    assert user.check_password(user_payload['password']) is True

    # Ensure user is in 'reader' group
    assert Group.objects.filter(name='reader').exists()
    assert user.groups.filter(name='reader').exists()

    # Ensure the new user is NOT in 'writer' group
    assert not user.groups.filter(name='writer').exists()


def test_multiple_users_each_get_reader_group(signup_service):
    u1 = signup_service.create_user(
        username="user1",
        password="password1"
    )

    u2 = signup_service.create_user(
        username="user2",
        password="password2"
    )

    assert u1.groups.filter(name='reader').exists()
    assert u2.groups.filter(name='reader').exists()
