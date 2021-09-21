from rest_framework import serializers


class PhoneValidateSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)


class CodeValidateSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    code = serializers.CharField(max_length=4)