

from django.urls import path
from .views import *
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView().as_view()),
    path('confirm/', ConfirmUserAPIView.as_view())
]