from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import textwrap
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework_simplejwt_mongoengine.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, PasswordResetRequestSerializer
from .authentication import MongoAuthBackend
from .utils import generate_reset_token, validate_reset_token, get_user_from_token, blacklist_access_token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def index(request):
    return HttpResponse("<h1>App is running..</h1>")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'message': 'This is a protected view'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_user(request):
    data = request.data
    errors = {}
    try:
        user = User(
            username=data['username'],
            email=data['email'],
        )
        
        try:
            user.clean()  # Validate email and username
            user.clean_password(data['password'])  # Validate password
        except ValidationError as e:
            # Convert the error message to a string and remove list formatting
            if "Email" in str(e):
                errors['email'] = str(e).strip("[]").replace("'", "")
            elif "Username" in str(e):
                errors['username'] = str(e).strip("[]").replace("'", "")
            elif "Password" in str(e):
                errors['password'] = str(e).strip("[]").replace("'", "")
            print("Validation Error:", str(e))
        
        if errors:
            print("Validation Errors Detected:", errors)
            return Response({'status': 'error', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        return Response({'status': 'success', 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print("Exception occurred:", str(e))
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Authenticate the user
    user = MongoAuthBackend().authenticate(request=None, username=username, password=password)
    
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    tokens = get_tokens_for_user(user)
    return Response({
        'access': tokens['access'],
        'refresh': tokens['refresh']
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def request_password_reset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects(email=email).first()
        username = user.username
        if user:
            token = generate_reset_token(user)
            reset_link = f"{settings.FRONTEND_URL}/password-reset/?token={token}"
            email_message = textwrap.dedent(f"""
            Your account username: {username}
                
            Click the following link to reset your password: {reset_link}
            """)
            send_mail(
                'Password Reset Request',
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
        return Response({'message': 'If the email is associated with an account, a password reset link has been sent.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verify_reset_tokens(request):
    token = request.query_params.get('token')
    print(f"Token received: {token}")
    if validate_reset_token(token):
        return Response({'message': 'Token is valid.'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm_password_reset(request):
    token = request.data.get('token')
    new_password = request.data.get('password')
    errors = {}

    user = get_user_from_token(token)
    if user:
        # Validate the new password
        try:
            user.clean_password(new_password)
        except ValidationError as e:
            errors['password'] = str(e).strip("[]").replace("'", "")

        if errors:
            return Response({'status': 'error', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save(validate=False)
        blacklist_access_token(token)
        return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
    
    # If the token is invalid or expired, or if there's any other issue
    return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
    

def get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh['user_id'] = str(user.id)  # Store the MongoDB user's ID in the token
    refresh['username'] = user.username  # Optionally store the username or other fields

    access_token = refresh.access_token
    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }