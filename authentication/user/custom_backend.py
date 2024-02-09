from django.contrib.auth.backends import ModelBackend
from user.models import CustomUser


class AuthenticateUser(ModelBackend):
    # Staff Authentication (email, password)
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
