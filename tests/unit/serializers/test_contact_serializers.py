import pytest
from rest_framework import serializers

from phonebook.api.contacts.serializers import (
    ContactListOutputSerializer,
    CreateContactInputSerializer
)

pytestmark = pytest.mark.django_db

"""
FIXTURES
"""


@pytest.fixture
def contact_factory():
    def make_contact(full_name: str, phone_number: str | None = None):
        from phonebook.models import Contact, PhoneNumber
        c = Contact.objects.create(full_name=full_name)
        if phone_number:
            PhoneNumber.objects.create(contact=c, phone_number=phone_number)
        return c
    return make_contact


"""
TESTS
"""


class TestContactListOutputSerializer:

    def test_contact_list_output_serializer(self):
        items = [
            {
                "name": "Alice Smith",
                "phone_number": "(123) 456-7890"
            },
            {
                "name": "Bob Johnson",
                "phone_number": None
            }
        ]

        results = ContactListOutputSerializer(items, many=True)

        assert results.data == [
            {
                "name": "Alice Smith",
                "phone_number": "(123) 456-7890"
            },
            {
                "name": "Bob Johnson",
                "phone_number": None
            }
        ]

    def test_contact_list_serializer_allows_nul(self):
        items = [
            {
                "name": "Cher",
                "phone_number": None
            }
        ]

        results = ContactListOutputSerializer(items, many=True)

        assert results.data == [
            {
                "name": "Cher",
                "phone_number": None
            }
        ]


class TestCreateContactInputSerializer:

    def test_create_contact_input_serializer_works(self):
        data = {
            "name": "Cher",
            "phone_number": '(123) 456-7890'
        }

        serializer = CreateContactInputSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data == {
            "name": "Cher",
            "phone_number": '(123) 456-7890'
        }

    def test_create_contact_input_serializer_raises_for_empty_name(self):
        data = {
            "name": "   ",
            "phone_number": '(123) 456-7890'
        }

        serializer = CreateContactInputSerializer(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        detail = exc.value.detail
        assert "name" in detail

    def test_create_contact_input_serializer_raises_for_duplicate_name(self, contact_factory):
        contact_factory(full_name="Cher")

        data = {
            "name": "Cher",
            "phone_number": '(123) 456-7890'
        }

        serializer = CreateContactInputSerializer(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        detail = exc.value.detail
        assert "name" in detail

    def test_create_contact_input_serializer_raises_for_empty_phone(self):
        data = {
            "name": "Cher",
            "phone_number": '   '
        }

        serializer = CreateContactInputSerializer(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        detail = exc.value.detail
        assert "phone_number" in detail

    def test_create_contact_input_serializer_raises_for_duplicate_phone(self, contact_factory):
        contact_factory(full_name="Alice", phone_number="(123) 456-7890")

        data = {
            "name": "Bob",
            "phone_number": '(123) 456-7890'
        }

        serializer = CreateContactInputSerializer(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        detail = exc.value.detail
        assert "phone_number" in detail

    def test_create_contact_input_serializer_raises_for_invalid_phone(self):
        data = {
            "name": "Cher",
            "phone_number": '<script>alert(1)</script>'
        }

        serializer = CreateContactInputSerializer(data=data)

        with pytest.raises(serializers.ValidationError) as exc:
            serializer.is_valid(raise_exception=True)

        detail = exc.value.detail
        assert "phone_number" in detail
