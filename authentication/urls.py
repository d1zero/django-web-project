from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('register/', RegisterAPIView.as_view(), name='register'),
    # path('confirm-register/<str:token>', ConfirmRegisterAPIView.as_view()),
    # path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('user/', GetUserAPIView.as_view()),
    # path('logout/', LogoutAPIView.as_view()),
    # path('update/', UpdateUserAPIView.as_view()),
]
