from django.contrib.auth.backends import BaseBackend
from .models import User

class MongoAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(username, password)
        user = User.objects(username=username).first()
        print(user)
        if user and user.check_password(password):
            return user
        return None