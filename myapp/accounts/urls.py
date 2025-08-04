from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),  # Add this path in urls.py of your app.  # For example, in myapp/urls.py  # Add this path in urls.py of your app.  # For example, in myapp/urls.py  # Add this path in urls.py of your app.  # For example, in myapp/urls.
    
]
