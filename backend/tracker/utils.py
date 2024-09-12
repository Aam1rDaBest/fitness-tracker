from rest_framework_simplejwt_mongoengine.tokens import RefreshToken
from rest_framework_simplejwt_mongoengine.tokens import AccessToken
from rest_framework_simplejwt_mongoengine.exceptions import TokenError
from .models import User, AccessTokenBlacklist

def generate_reset_token(user):
    """Generate a token for password reset."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def validate_reset_token(token):
    """Validate a reset token."""
    try:
        AccessTokenBlacklist.cleanup_expired_and_inactive_tokens()
        encoded_token = AccessTokenBlacklist().encode_token(token)
        if AccessTokenBlacklist.objects(token=encoded_token).first():
            return False
        AccessToken(token)
        return True
    except TokenError as e:
        print(f"Token validation error: {e}")
        return False

def get_user_from_token(token):
    """Retrieve user from token."""
    try:
        token_obj = AccessToken(token)
        user_id = token_obj['user_id']
        return User.objects(id=user_id).first()
    except TokenError:
        return None
    
def blacklist_access_token(token):
    """Blacklist an access token."""
    try:
        encoded_token = AccessTokenBlacklist().encode_token(token)
        if AccessTokenBlacklist.objects(token=encoded_token).first():
            return False
        blacklisted_token = AccessTokenBlacklist(token=token)
        blacklisted_token.save()
        return True
    except Exception as e:
        print(f"Error blacklisting token: {e}")
        return False