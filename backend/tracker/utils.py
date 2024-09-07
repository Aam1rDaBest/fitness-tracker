from rest_framework_simplejwt_mongoengine.tokens import RefreshToken
from rest_framework_simplejwt_mongoengine.exceptions import TokenError
from .models import User

def generate_reset_token(user):
    """Generate a token for password reset."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def validate_reset_token(token):
    """Validate a reset token."""
    try:
        token_obj = RefreshToken(token)
        token_obj.check_blacklist()  
        return True
    except TokenError:
        return False

def get_user_from_token(token):
    """Retrieve user from token."""
    try:
        token_obj = RefreshToken(token)
        user_id = token_obj['user_id']
        return User.objects(id=user_id).first()
    except TokenError:
        return None