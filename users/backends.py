from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        # Пытается найти пользователя по username или email
        try:
            user = UserModel.objects.get(
                models.Q(username__iexact=username) | 
                models.Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
            
        if user.check_password(password):
            return user
        return None