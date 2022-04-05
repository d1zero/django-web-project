from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ConfirmUserAPIView

urlpatterns = [
    path('confirm-register/<str:token>', ConfirmUserAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
