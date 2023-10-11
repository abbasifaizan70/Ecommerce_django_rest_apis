from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None
        if user is not None and user.check_password(password):
            if user.is_active:
                return user
        return None
