from django.urls import path
from myapp.accounts.views import DeleteUserView,VerifyEmailView, CreateUserView, LoginView, ProfileView, LogoutView, PasswordResetRequestView, PasswordResetConfirmView


urlpatterns = [
    # ------------------USER URLS------------------
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
]
