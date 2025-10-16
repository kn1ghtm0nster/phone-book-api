import pytest
from django.urls import reverse
from rest_framework.test import APITestCase

from phonebook.models import Contact, PhoneNumber

pytestmark = pytest.mark.django_db

# TODO: Update tests when Authentication and Permissions are added


class TestContactListAPI(APITestCase):

    def setUp(self):
        self.url = reverse('contact-list')

    def test_get_contacts(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.json() == []  # Expecting an empty list initially

    def test_get_contacts_with_existing_data(self):
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
            phone_number='1 (703) 123-1234',
        )

        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.json() == [
            {
                "name": "Bruce Schneier",
                "phone_number": "(703)111-2121"
            },
            {
                "name": "Cher",
                "phone_number": None
            },
            {
                "name": "John O'Malley-Smith",
                "phone_number": "1 (703) 123-1234"
            }
        ]
