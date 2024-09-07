from django.urls import path
from rest_framework_simplejwt_mongoengine.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_user/', views.add_user, name='add_user'),
    path('login/', views.login_view, name= 'login' ),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('protected/', views.protected_view, name='protected_view'),
    path('password-reset/', views.request_password_reset, name='password_reset_request'),
    path('password-reset/verify/', views.verify_reset_token, name='password_reset_verify'),
    path('password-reset/confirm/', views.confirm_password_reset, name='password_reset_confirm'),
]