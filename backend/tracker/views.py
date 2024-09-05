from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework_simplejwt_mongoengine.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .authentication import MongoAuthBackend
from django.urls import reverse


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
    try:
        user = User(
            username=data['username'],
            email=data['email'],
        )
        user.clean()
        user.clean_password(data['password'])
        user.save()
        return Response({'status': 'success', 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
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

def get_tokens_for_user(user):
    refresh = RefreshToken()
    refresh['user_id'] = str(user.id)  # Store the MongoDB user's ID in the token
    refresh['username'] = user.username  # Optionally store the username or other fields

    access_token = refresh.access_token
    return {
        'refresh': str(refresh),
        'access': str(access_token),
    }