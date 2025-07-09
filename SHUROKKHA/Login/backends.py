from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class UserIDBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Accept user ID instead of username
            user = User.objects.get(id=int(username))
            if user.check_password(password):
                return user
        except (User.DoesNotExist, ValueError):
            return None
