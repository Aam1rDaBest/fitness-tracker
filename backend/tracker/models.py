from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import make_aware
from mongoengine import Document, EmailField, StringField, BooleanField, DateTimeField
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import EmailValidator, RegexValidator
import re
import base64

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
        # Username validation
        if len(self.username) < 5:
            raise ValidationError("Username must be at least 5 characters long")
        if User.objects(username=self.username).count() > 0:
            raise ValidationError("Username is already taken")
        
        # Email validation
        email_validator = EmailValidator(message="Invalid email format")
        email_validator(self.email)
        if User.objects(email=self.email).count() > 0:
            raise ValidationError("Email is already in use")

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

class AccessTokenBlacklist(Document):  
    token = StringField(required=True) 
    created_at = DateTimeField(default=timezone.now)
    is_active = BooleanField(default=True)

    meta = {'collection': 'access_token_blacklist'}

    def encode_token(self, raw_token):
        """Encode the token string."""
        return base64.b64encode(raw_token.encode()).decode()

    def decode_token(self, encoded_token):
        """Decode the token string."""
        return base64.b64decode(encoded_token.encode()).decode()

    def save(self, *args, **kwargs):
        """Override save to handle token encoding."""
        if self.token:
            self.token = self.encode_token(self.token)
        super().save(*args, **kwargs)
        
    @staticmethod
    def deactivate_expired_tokens():
        """Deactivate tokens that have expired."""
        now = timezone.now()
        expiration_time = now - timedelta(minutes=15)
        AccessTokenBlacklist.objects(created_at__lt=expiration_time, is_active=True).update(is_active=False)

    @staticmethod
    def delete_inactive_tokens():
        """Delete tokens that are inactive."""
        AccessTokenBlacklist.objects(is_active=False).delete()

    def cleanup_expired_and_inactive_tokens():
        """Run cleanup for expired and inactive tokens."""
        AccessTokenBlacklist.deactivate_expired_tokens()
        AccessTokenBlacklist.delete_inactive_tokens()
    