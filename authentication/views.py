from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
import jwt
from rest_framework.exceptions import AuthenticationFailed, NotFound, ParseError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from .models import CustomUser, UserFavorite
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


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
        favs = UserFavorite.objects.create(user=user)
        favs.save()
        return Response({'message': 'success'})


class LoginAPIView(APIView):
    def post(self, request):
        try:
            user = CustomUser.objects.get(email=request.data.get('email'))
        except CustomUser.DoesNotExist:
            raise NotFound('User does not exists')

        if not user.check_password(request.data.get('password')):
            raise AuthenticationFailed('Incorrect password')

        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)
        response = Response()
        response.set_cookie('refresh', str(refresh))
        response.data = {'access': str(refresh.access_token), }
        return response


class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response(data)


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        if 'refresh' not in request.COOKIES:
            raise AuthenticationFailed(detail='Unauthenticated')
        token = request.COOKIES.get('refresh')
        token = RefreshToken(token)
        token.blacklist()

        response.delete_cookie('refresh')
        response.data = {'message': 'success'}
        return response


class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        data = request.data
        if 'username' in data and len(data.get('username')) > 0:
            try:
                candidate = CustomUser.objects.get(
                    username=data.get('username'))
                raise ParseError(detail='Username already taken')
            except CustomUser.DoesNotExist:
                pass
            user.username = data.get('username')
            user.save()
        if 'avatar' in data and len(data.get('avatar')) > 0:
            user.avatar = request.FILES['avatar']
            user.save()

        return Response()
