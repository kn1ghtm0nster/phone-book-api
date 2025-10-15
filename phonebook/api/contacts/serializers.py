from rest_framework import serializers


class ContactListOutputSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True, allow_null=True)
