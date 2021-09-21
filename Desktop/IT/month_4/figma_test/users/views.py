import secrets
import random
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OTPCode
from .serializers import PhoneValidateSerializer, CodeValidateSerializer


class OTPView(APIView):
    def post(self, request):
        serializer = PhoneValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'message': 'error',
                    'errors': serializer.errors
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        phone = serializer.validated_data['phone']
        try:
            user = User.objects.get(username=phone)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=phone,
                email='a@k.ru',
                password=secrets.token_hex(16)
            )
            user.save()
        OTPCode.objects.filter(user=user).delete()
        OTPCode.objects.create(
            user=user,
            code=str(random.randint(1000, 9999))
        )
        return Response(data={'message': 'code created!!!'})


class ConfirmOTPCodeView(APIView):
    def post(self, request):
        serializer = CodeValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    'message': 'error',
                    'errors': serializer.errors
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        try:
            code = OTPCode.objects.get(user__username=phone, code=code)
        except OTPCode.DoesNotExist:
            return Response(data={'message': 'error'}, status=status.HTTP_404_NOT_FOUND)
        Token.objects.filter(user=code.user).delete()
        token = Token.objects.create(user=code.user)
        code.delete()
        return Response(data={'key': token.key})
