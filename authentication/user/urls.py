from django.urls import path
from user.api_views.register import register
from user.api_views.login import LoginView
from user.api_views.token_verification import verify_token


urlpatterns = [
    path("signup/", register, name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token-verification/", verify_token, name="token-verification"),
]
