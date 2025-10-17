import pytest

from phonebook.models import Contact, PhoneNumber
from phonebook.services import ContactService

pytestmark = pytest.mark.django_db


"""
FIXTURES
"""


@pytest.fixture
def create_contact():
    def make_contact(full_name: str, phone_number: str | None = None):
        c = Contact.objects.create(full_name=full_name)
        if phone_number:
            PhoneNumber.objects.create(contact=c, phone_number=phone_number)
        return c
    return make_contact


"""
UNIT TESTS
"""


def test_retrieve_all_contacts():
    c1 = Contact.objects.create(full_name="Bruce Schneier")
    PhoneNumber.objects.create(
        contact=c1,
        phone_number='(703)111-2121'
    )

    # no phone number for c2
    c2 = Contact.objects.create(
        full_name="Cher")

    c3 = Contact.objects.create(
        full_name="John O'Malley-Smith")

    PhoneNumber.objects.create(
        contact=c3,
        phone_number='1 (703) 123-1234'
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


def test_check_name_exists(create_contact):
    create_contact(full_name="Bruce Schneier")
    svc = ContactService()
    assert svc._check_name_exists("Bruce Schneier") is True
    assert svc._check_name_exists("Cher") is False


def test_check_phone_number_exists(create_contact):
    create_contact(full_name="Alice Example", phone_number="(703)111-2121")
    svc = ContactService()
    assert svc._check_phone_number_exists("(703)111-2121") is True
    assert svc._check_phone_number_exists("670-123-4567") is False


def test_create_new_contact_success():
    svc = ContactService()
    result = svc.create_new_contact(
        name="John O'Malley-Smith", phone_number="1 (703) 123-1234")

    assert result == {"name": "John O'Malley-Smith",
                      "phone_number": "1 (703) 123-1234"}
    assert Contact.objects.filter(full_name="John O'Malley-Smith").count() == 1
    c = Contact.objects.get(full_name="John O'Malley-Smith")
    assert PhoneNumber.objects.filter(
        contact=c, phone_number="1 (703) 123-1234").count() == 1


def test_create_new_contact_one_to_one_enforced():
    svc = ContactService()
    svc.create_new_contact(name="Cher", phone_number="670-123-4567")
    c = Contact.objects.get(full_name="Cher")
    # Exactly one phone number for this contact (one-to-one)
    assert PhoneNumber.objects.filter(contact=c).count() == 1
