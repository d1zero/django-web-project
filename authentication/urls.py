from django.urls import path
from .views import ConfirmRegisterAPIView, GetUserAPIView, RegisterAPIView, LoginAPIView, LogoutAPIView, UpdateUserAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('confirm-register/<str:token>', ConfirmRegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', GetUserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('update/', UpdateUserAPIView.as_view()),
]
