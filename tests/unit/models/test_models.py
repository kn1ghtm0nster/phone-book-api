import pytest
from faker import Faker

from phonebook.models import Contact, PhoneNumber

pytestmark = pytest.mark.django_db


def test_create_contact():
    c = Contact.objects.create(full_name="Bruce Schneier")
    p = PhoneNumber.objects.create(
        phone_number='(703)111-2121', contact=c, is_primary=True
    )

    assert Contact.objects.count() == 1
    assert PhoneNumber.objects.count() == 1
    assert p.contact == c
    assert p.is_primary is True
