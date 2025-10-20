from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from typing import Any, cast

from phonebook.api.utilities import valid_name
from phonebook.api.utilities.valid_patterns import ATTACKER_REGEX


class SignUpSerializerInput(serializers.Serializer):
    """
    Serializer class for user sign-up input data validation.
    """

    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(
        write_only=True, trim_whitespace=False, required=True)
    first_name = serializers.CharField(
        required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(
        required=False, allow_blank=True, max_length=150)

    def validate_username(self, value: str) -> str:
        """
        Validate the username field.
        """

        username = value.strip()
        if not username:
            raise serializers.ValidationError(
                "Username cannot be empty or whitespace.")

        # use Django's built-in username validator
        validator = UnicodeUsernameValidator()
        try:
            validator(username)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid username.")

        # Check for uniqueness
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username is already taken.")

        return username

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Validate the entire input data.
        """
        # validate first_name and last_name if provided
        for key in ('first_name', 'last_name'):
            raw = attrs.get(key)
            if raw:
                cleaned, ok = valid_name(raw)
                if not ok:
                    raise serializers.ValidationError(
                        {
                            key: [cleaned]
                        }
                    )

        # Use Django's password validators
        pwd = attrs.get('password')
        if "<" in cast(str, pwd) or ">" in cast(str, pwd):
            raise serializers.ValidationError(
                {
                    "password": ["Invalid characters in password."]
                }
            )

        if ATTACKER_REGEX.search(cast(str, pwd)):
            raise serializers.ValidationError(
                {
                    "password": ["Invalid password."]
                }
            )

        # pass a lightweight user context so validators can check similarity
        username = attrs.get('username', '')
        User = get_user_model()
        temp_user = User(username=username)
        try:
            validate_password(password=cast(str, pwd), user=temp_user)
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                {
                    "password": list(e.messages)
                }
            )

        return attrs


class SignUpSerializerOutput(serializers.Serializer):
    """
    Serializer class for user sign-up output data representation.
    """

    username = serializers.CharField(max_length=150)
    access_token = serializers.CharField()
