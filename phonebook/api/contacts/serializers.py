from rest_framework import serializers

from phonebook.services import ContactService
from phonebook.api.utilities import valid_phone_number


class ContactListOutputSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True, allow_null=True)


class CreateContactInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    phone_number = serializers.CharField(required=True, max_length=50)

    def validate_name(self, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise serializers.ValidationError(
                "Name cannot be empty or whitespace.")

        if ContactService()._check_name_exists(cleaned_value):
            raise serializers.ValidationError(
                "A contact with this name already exists.")
        return cleaned_value

    def validate_phone_number(self, value: str) -> str:
        # ensure phone number matches accepted patterns per specs
        result_string, is_valid = valid_phone_number(value)
        if not is_valid:
            raise serializers.ValidationError(result_string)

        if ContactService()._check_phone_number_exists(result_string):
            raise serializers.ValidationError(
                "This phone number is already associated with another contact.")

        return result_string
