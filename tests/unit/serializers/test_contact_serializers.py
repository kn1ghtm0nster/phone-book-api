import pytest

from phonebook.api.contacts.serializers import ContactListOutputSerializer

"""
FIXTURES
"""


"""
TESTS
"""


def test_contact_list_output_serializer():
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


def test_contact_list_serializer_allows_nul():
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
