from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from .models import CustomUser
from .serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        username = request.data.get('username')

        payload = {
            'username': username,
            'code': get_random_string(length=32)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        user = CustomUser.objects.get(username=username)
        user.token = token
        user.save()

        link = f'http://127.0.0.1:8000/api/auth/confirm-register/{token}'

        send_mail('Активация аккаунта Musicality', f'Привет, {username}! Перейди по ссылке: {link} С уважением, команда Musicality',
                  settings.EMAIL_HOST_USER, [request.data.get('email')], fail_silently=False)

        return Response({'message': 'success'})


class ConfirmRegisterAPIView(APIView):
    def patch(self, _, token):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed(detail='Codes are different')
        user = CustomUser.objects.get(username=payload['username'])
        if user.token != token:
            raise AuthenticationFailed(detail='Codes are different')
        user.is_active = True
        user.save()
        return Response({'message': 'success'})


class LoginAPIView(APIView):
    def post(self, request):
        user = CustomUser.objects.get(email=request.data.get('email'))
        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        print(refresh)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
