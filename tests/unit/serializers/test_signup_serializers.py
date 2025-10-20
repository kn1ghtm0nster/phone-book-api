import pytest
from django.contrib.auth import get_user_model
from rest_framework import serializers
from typing import cast

from phonebook.api.signup.serializers import (
    SignUpSerializerInput,
    SignUpSerializerOutput
)

pytestmark = pytest.mark.django_db

"""
FIXTURES
"""


@pytest.fixture
def user_factory():
    User = get_user_model()

    def make_user(username="existing_user"):
        return User.objects.create_user(
            username=username,
            password="SafePassword123!"
        )
    return make_user


"""
TESTS
"""


class TestSignUpSerializerInput:

    def test_signup_input_valid_data(self):
        data = {
            'username': 'new_user',
            'password': 'SafePassword123!',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = SignUpSerializerInput(data=data)
        assert serializer.is_valid()

        data = cast(dict[str, str], serializer.validated_data)
        assert data['username'] == 'new_user'
        assert data['first_name'] == 'John'
        assert data['last_name'] == 'Doe'

    def test_signup_works_no_optional_fields(self):
        data = {
            'username': 'simple_user',
            'password': 'SafePassword123!'
        }
        serializer = SignUpSerializerInput(data=data)
        assert serializer.is_valid()

        data = cast(dict[str, str], serializer.validated_data)
        assert data['username'] == 'simple_user'
        assert 'first_name' not in data
        assert 'last_name' not in data

    def test_signup_serializer_trims_whitespace(self):
        data = {
            'username': '   trimmed_user   ',
            'password': 'SafePassword123!'
        }
        serializer = SignUpSerializerInput(data=data)
        assert serializer.is_valid()

        data = cast(dict[str, str], serializer.validated_data)
        assert data['username'] == 'trimmed_user'

    def test_signup_input_denies_whitespace_username(self):
        data = {
            'username': '     ',
            'password': 'SafePassword123!'
        }
        serializer = SignUpSerializerInput(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors

    def test_signup_input_denies_invalid_chars(self):
        data = {
            'username': '<script>alert("You were hacked!")</script>',
            'password': 'SafePassword123!'
        }

        serializer = SignUpSerializerInput(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors

    def test_signup_input_denies_duplicate_username(self, user_factory):
        user_factory(username='existing_user')
        data = {
            'username': 'existing_user',
            'password': 'SafePassword123!'
        }

        serializer = SignUpSerializerInput(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors

    def test_signup_input_denies_invalid_phone_chars(self):
        data = {
            'username': 'alice',
            'password': '<script>alert("hack")</script>'
        }
        serializer = SignUpSerializerInput(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        assert 'password' in exc.value.detail

    def test_signup_input_denies_weak_password(self):
        data = {
            'username': 'bob',
            'password': 'password'
        }
        serializer = SignUpSerializerInput(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        assert 'password' in exc.value.detail

    def test_signup_input_denies_invalid_first_name(self):
        data = {
            'username': 'charlie',
            'password': 'SafePassword123!',
            'first_name': 'select * from users;'
        }
        serializer = SignUpSerializerInput(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        assert 'first_name' in exc.value.detail

    def test_signup_input_denies_invalid_last_name(self):
        data = {
            'username': 'david',
            'password': 'SafePassword123!',
            'last_name': 'drop table contacts;'
        }
        serializer = SignUpSerializerInput(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        assert 'last_name' in exc.value.detail


class TestSignUpSerializerOutput:

    def test_output_serializer(self):
        data = {
            'username': 'new_user',
            'access_token': 'some.jwt.token.here'
        }
        serializer = SignUpSerializerOutput(data=data)
        assert serializer.is_valid()

        data = cast(dict[str, str], serializer.validated_data)
        assert data['username'] == 'new_user'
        assert data['access_token'] == 'some.jwt.token.here'
