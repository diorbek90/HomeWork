from django.urls import path
from users.views import RegistrationAPIView, AuthorizationAPIView, ConfirmUserAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
    path('confirm/', ConfirmUserAPIView.as_view()),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]