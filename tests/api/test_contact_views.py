import pytest
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from phonebook.models import Contact, PhoneNumber

pytestmark = pytest.mark.django_db


class TestContactListAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        # create groups if they do not exist
        cls.reader_group, _ = Group.objects.get_or_create(name='reader')
        cls.reader = User.objects.create_user(
            username='reader_user1',
            password='readerpass123'
        )
        cls.reader.groups.add(cls.reader_group)

    def setUp(self):
        self.url = reverse('contact-list')
        self.api_client: APIClient = APIClient()
        self.api_client.force_authenticate(user=self.reader)

    def test_get_contacts(self):
        response = self.api_client.get(self.url)
        assert response.status_code == 200  # type: ignore
        assert response.data == []  # Expecting an empty list initially #type:ignore

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

        response = self.api_client.get(self.url)
        assert response.status_code == 200  # type: ignore
        assert response.json() == [  # type: ignore
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

    def test_get_contacts_no_auth(self):
        client = APIClient()  # unauthenticated client
        response = client.get(self.url)
        assert response.status_code == 401  # Unauthorized #type: ignore


class TestContactCreateAPI(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.writer_group, _ = Group.objects.get_or_create(name='writer')
        cls.writer = User.objects.create_user(
            username='writer_user1',
            password='writerpass123'
        )
        cls.writer.groups.add(cls.writer_group)

        cls.reader_group, _ = Group.objects.get_or_create(name='reader')
        cls.reader = User.objects.create_user(
            username='reader_user1',
            password='readerpass123'
        )
        cls.reader.groups.add(cls.reader_group)

    def setUp(self):
        self.url = reverse('contact-add')
        self.api_client: APIClient = APIClient()
        self.client = self.api_client

    def test_create_contact_success(self):
        request_body = {
            "name": "Alice Smith",
            "phone_number": "(123) 456-7890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 201
        assert response.json() == request_body

    def test_create_contact_no_auth(self):
        client = APIClient()
        request_body = {
            "name": "Alice Smith",
            "phone_number": "(123) 456-7890"
        }

        response = client.post(self.url, data=request_body, format='json')
        assert response.status_code == 401  # type: ignore

    def test_create_contact_no_permissions(self):
        request_body = {
            "name": "Alice Smith",
            "phone_number": "(123) 456-7890"
        }

        response = self.client.post(self.url, data=request_body, format='json')
        assert response.status_code == 403  # type: ignore

    def test_create_contact_missing_name(self):
        request_body = {
            "phone_number": "(123) 456-7890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "name": ["This field is required."]
        }

    def test_create_contact_missing_phone_number(self):
        request_body = {
            "name": "Alice Smith"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "phone_number": ["This field is required."]
        }

    def test_create_contact_empty_name(self):
        request_body = {
            "name": None,
            "phone_number": "(123) 456-7890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "name": ["This field may not be null."]
        }

    def test_create_contact_whitespace_name(self):
        request_body = {
            "name": "   ",
            "phone_number": "(123) 456-7890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "name": ["This field may not be blank."]
        }

    def test_create_contact_duplicate_name(self):
        Contact.objects.create(full_name="Alice Smith")

        request_body = {
            "name": "Alice Smith",
            "phone_number": "(123) 456-7890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "name": ["A contact with this name already exists."]
        }

    def test_create_contact_invalid_name_xss(self):
        request_body = {
            "name": "<script>alert('XSS')</script>",
            "phone_number": "(123) 456-7890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "name": ["Invalid characters in name."]
        }

    def test_create_contact_sql_injection_name(self):
        request_body = {
            "name": "Alice'; DROP TABLE Contacts;--",
            "phone_number": "(123) 456-7890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "name": ["Invalid characters in name."]
        }

    def test_create_contact_duplicate_phone_number(self):
        c = Contact.objects.create(full_name="Bob Jones")
        PhoneNumber.objects.create(contact=c, phone_number="(123) 456-7890")

        request_body = {
            "name": "Alice Smith",
            "phone_number": "(123) 456-7890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "phone_number": [
                "This phone number is already associated with another contact."
            ]
        }

    def test_create_contact_invalid_phone_number_format(self):
        request_body = {
            "name": "Alice Smith",
            "phone_number": "1234567890"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "phone_number": ["Invalid phone number format."]
        }

    def test_create_contact_xss_phone_number(self):
        request_body = {
            "name": "Alice Smith",
            "phone_number": "<script>alert('XSS')</script>"
        }

        self.client.force_authenticate(user=self.writer)  # type: ignore
        response = self.client.post(self.url, data=request_body, format='json')

        assert response.status_code == 400
        assert response.json() == {
            "phone_number": ["Invalid characters in phone number."]
        }
