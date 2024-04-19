from django.urls import path
from api.authentication.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view())
]
