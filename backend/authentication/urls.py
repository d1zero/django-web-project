from django.urls import path
from .views import ConfirmRegisterAPIView, RegisterAPIView, LoginAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('confirm-register/<str:token>', ConfirmRegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
