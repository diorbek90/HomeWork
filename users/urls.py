

from django.urls import path
from .views import registration_api_view, authorization_api_view, confirm_user_api_view
urlpatterns = [
    path('registration/', registration_api_view),
    path('authorization/', authorization_api_view),
    path('confirm/', confirm_user_api_view)
]