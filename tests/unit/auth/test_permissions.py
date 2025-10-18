import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group,
    AnonymousUser,
)
from rest_framework.test import APIRequestFactory

from config.authentication import (
    IsReaderOrWriter,
    IsWriter
)


pytestmark = pytest.mark.django_db

"""
FIXTURES
"""


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()


@pytest.fixture
def groups():
    reader, _ = Group.objects.get_or_create(name='reader')
    writer, _ = Group.objects.get_or_create(name='writer')

    return {
        'reader': reader,
        'writer': writer,
    }


@pytest.fixture
def user_factory(groups):
    User = get_user_model()

    def _make(username='u', is_superuser=False, reader=False, writer=False):
        u = User.objects.create_user(
            username=username,
            password='testpass123',
        )
        u.is_superuser = is_superuser
        u.save()

        if reader:
            u.groups.add(groups['reader'])
        if writer:
            u.groups.add(groups['writer'])
        return u

    return _make


"""
HELPER FUNCS
"""


def attach_user(req, user):
    req.user = user
    return req


"""
UNIT TESTS
"""


class TestIsReaderOrWriter:

    def test_unauthenticated_is_denied(self, api_request_factory):
        req = attach_user(api_request_factory.get('/'), AnonymousUser())
        assert IsReaderOrWriter().has_permission(req, None) is False

    def test_plain_user_with_no_groups_is_denied(self, api_request_factory, user_factory):
        user = user_factory(username='plain_user')
        req = attach_user(api_request_factory.get('/'), user)
        assert IsReaderOrWriter().has_permission(req, None) is False

    def test_reader_is_allowed(self, api_request_factory, user_factory):
        user = user_factory(username='reader_user', reader=True)
        req = attach_user(api_request_factory.get('/'), user)
        assert IsReaderOrWriter().has_permission(req, None) is True

    def test_writer_is_allowed(self, api_request_factory, user_factory):
        user = user_factory(username='writer_user', writer=True)
        req = attach_user(api_request_factory.get('/'), user)
        assert IsReaderOrWriter().has_permission(req, None) is True

    def test_superuser_is_allowed(self, api_request_factory, user_factory):
        user = user_factory(username='superuser', is_superuser=True)
        req = attach_user(api_request_factory.get('/'), user)
        assert IsReaderOrWriter().has_permission(req, None) is True


class TestIsWriter:

    def test_unauthenticated_is_denied(self, api_request_factory):
        req = attach_user(api_request_factory.get('/'), AnonymousUser())
        assert IsWriter().has_permission(req, None) is False

    def test_plain_user_with_no_groups_is_denied(self, api_request_factory, user_factory):
        user = user_factory(username='plain_user')
        req = attach_user(api_request_factory.get('/'), user)
        assert IsWriter().has_permission(req, None) is False

    def test_reader_is_denied(self, api_request_factory, user_factory):
        user = user_factory(username='reader_user', reader=True)
        req = attach_user(api_request_factory.get('/'), user)
        assert IsWriter().has_permission(req, None) is False

    def test_writer_is_allowed(self, api_request_factory, user_factory):
        user = user_factory(username='writer_user', writer=True)
        req = attach_user(api_request_factory.get('/'), user)
        assert IsWriter().has_permission(req, None) is True

    def test_superuser_is_allowed(self, api_request_factory, user_factory):
        user = user_factory(username='superuser', is_superuser=True)
        req = attach_user(api_request_factory.get('/'), user)
        assert IsWriter().has_permission(req, None) is True
