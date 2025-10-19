from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
from typing import Any, cast

from phonebook.services import SignUpService
from .serializers import (
    SignUpSerializerInput,
    SignUpSerializerOutput,
)


class SignUpAPIView(APIView):
    """
    API view for user sign-up.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        serializer = SignUpSerializerInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, Any], serializer.validated_data)

        sign_up_service = SignUpService()
        new_user = sign_up_service.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data.get('first_name', ""),
            last_name=data.get('last_name', "")
        )

        # Issue JWT access token
        refresh = RefreshToken.for_user(new_user)
        access_token = str(refresh.access_token)

        serializer = SignUpSerializerOutput(data={
            'username': new_user.username,
            'access_token': access_token
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
