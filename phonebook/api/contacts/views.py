from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, permissions

from .serializers import (
    ContactListOutputSerializer,
)
from phonebook.services import ContactService


class ContactListAPI(APIView):
    """
    API view to list all contacts.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request: Request) -> Response:
        service = ContactService()
        contacts = service.retrieve_all_contacts()
        serializer = ContactListOutputSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
