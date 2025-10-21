from rest_framework import serializers

from phonebook.services import ContactService
from phonebook.api.utilities import valid_phone_number, valid_name


class ContactListOutputSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True, allow_null=True)


class CreateContactInputSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    phone_number = serializers.CharField(required=True, max_length=50)

    def validate_name(self, value: str) -> str:
        # ensure name matches accepted patterns per specs
        result, is_valid = valid_name(value)
        if not is_valid:
            raise serializers.ValidationError(result)

        if ContactService()._check_name_exists(result):
            raise serializers.ValidationError(
                "A contact with this name already exists.")
        return result

    def validate_phone_number(self, value: str) -> str:
        # ensure phone number matches accepted patterns per specs
        result_string, is_valid = valid_phone_number(value)
        if not is_valid:
            raise serializers.ValidationError(result_string)

        if ContactService()._check_phone_number_exists(result_string):
            raise serializers.ValidationError(
                "This phone number is already associated with another contact.")

        return result_string


class DeleteContactInputSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=False, allow_null=True, max_length=255)
    phone_number = serializers.CharField(
        required=False, allow_null=True, max_length=50)

    def validate(self, attrs: dict) -> dict:
        name = attrs.get('name')
        phone_number = attrs.get('phone_number')

        if not name and not phone_number:
            raise serializers.ValidationError(
                "Either 'name' or 'phone_number' must be provided for deletion."
            )

        if phone_number is not None:
            cleaned_phone, ok = valid_phone_number(
                phone_number)
            if not ok:
                raise serializers.ValidationError(
                    "Invalid phone number."
                )
            attrs['phone_number'] = cleaned_phone

        if name is not None:
            cleaned_name, ok = valid_name(name)
            if not ok:
                raise serializers.ValidationError(
                    "Invalid name."
                )
            attrs['name'] = cleaned_name

        return attrs
