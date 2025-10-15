import pytest

from phonebook.models import Contact, PhoneNumber
from phonebook.services import ContactService

pytestmark = pytest.mark.django_db


"""
FIXTURES
"""


"""
UNIT TESTS
"""


def test_retrieve_all_contacts():
    c1 = Contact.objects.create(full_name="Bruce Schneier")
    PhoneNumber.objects.create(
        contact=c1,
        phone_number='(703)111-2121',
        is_primary=True
    )

    # no phone number for c2
    c2 = Contact.objects.create(
        full_name="Cher")

    c3 = Contact.objects.create(
        full_name="John O'Malley-Smith")

    PhoneNumber.objects.create(
        contact=c3,
        phone_number='1 (703) 123-1234',
        is_primary=True
    )

    PhoneNumber.objects.create(
        contact=c3,
        phone_number='011 703 123 1234',
        is_primary=False
    )

    service = ContactService()
    results = service.retrieve_all_contacts()

    assert len(results) == 3
    assert results[0] == {
        "name": "Bruce Schneier",
        "phone_number": "(703)111-2121"
    }
    assert results[1] == {
        "name": "Cher",
        "phone_number": None
    }
    assert results[2] == {
        "name": "John O'Malley-Smith",
        "phone_number": "1 (703) 123-1234"
    }
