from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthentication(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        print('hi')
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            
        return None


