from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, permissions
from typing import cast

from .serializers import (
    ContactListOutputSerializer,
    CreateContactInputSerializer,
)
from phonebook.services import ContactService
from config.authentication import (
    IsWriter,
    IsReaderOrWriter
)


class ContactListAPI(APIView):
    """
    API view to list all contacts.
    """

    permission_classes = [permissions.IsAuthenticated, IsReaderOrWriter]

    def get(self, request: Request) -> Response:
        service = ContactService()
        contacts = service.retrieve_all_contacts()
        serializer = ContactListOutputSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactCreateAPI(APIView):
    """
    API view to create a new contact.
    """

    permission_classes = [permissions.IsAuthenticated, IsWriter]

    def post(self, request: Request):
        serializer = CreateContactInputSerializer(data=request.data)
        service = ContactService()
        serializer.is_valid(raise_exception=True)

        validated_data = cast(dict, serializer.validated_data)
        name = validated_data['name']
        phone_number = validated_data['phone_number']

        new_contact = service.create_new_contact(name, phone_number)

        serializer = ContactListOutputSerializer(new_contact)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
