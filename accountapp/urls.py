from django.contrib import admin
from django.urls import path,include
from accountapp.views import (
    CustomerRegistrationView, 
    CustomerLoginView, 
    CustomerLoginViewJWT,
    CustomerProfileView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    CustomerPasswordResetView
    )



urlpatterns = [
    path('register/', CustomerRegistrationView.as_view(), name='register'),
    path('login/', CustomerLoginView.as_view(), name='login'),
    path('loginjwt/',CustomerLoginViewJWT.as_view(), name = 'login_jwt'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', CustomerProfileView.as_view(), name='profile_update'),
    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send_reset_email'),
    path('reset-password/<uid>/<token>', CustomerPasswordResetView.as_view(), name='reset_password'),

]


#127.0.0.1:8000/api/user/reset/Mg/b90ooe-90cb78109dc4c11956e6e2c0e99f9c52
