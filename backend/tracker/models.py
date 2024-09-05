from mongoengine import Document, EmailField, StringField, BooleanField
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
import re

class CustomUserManager:
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = User(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class User(Document):
    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    is_active = BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def clean(self):
        # Email validation
        email_validator = EmailValidator(message="Invalid email format")
        email_validator(self.email)
        if User.objects(email=self.email).count() > 0:
            raise ValidationError("Email is already in use")
        
        # Username validation
        if len(self.username) < 5:
            raise ValidationError("Username must be at least 5 characters long")
        if User.objects(username=self.username).count() > 0:
            raise ValidationError("Username is already taken")

    def clean_password(self, password):
        # Password validation
        if len(password) < 5:
            raise ValidationError("Password must be at least 5 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[0-9]', password) and not re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', password):
            raise ValidationError("Password must contain at least one special character or number")
        
        # Hash the password if it’s not already hashed
        if not password.startswith('pbkdf2_sha256'):
            self.password = make_password(password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
