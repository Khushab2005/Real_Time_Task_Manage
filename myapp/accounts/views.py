from django.shortcuts import render
from rest_framework.decorators import  APIView
from rest_framework.response import Response
from myapp.accounts.serializers import UserCreateSerializer,PasswordResetConfirmSerializer,PasswordResetRequestSerializer
from myapp.accounts.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import status
from django.core.cache import cache
from myapp.accounts.rate_limiter import rate_limited
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from myapp.accounts.constants import Rolechoice


# Create User View
class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "link sent to email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete User View
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if request.user.role != Rolechoice.ADMIN:
                return Response({"error": "You do not have permission to delete users."}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"msg": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#Verify Email View
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]  # Change from IsAuthenticated to AllowAny

    def post(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")
        
        if not uid or not token:
            return Response({"error": "Missing UID or token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            #for checking the token
            # print( uid,user_id)
            user_id = urlsafe_base64_decode(uid).decode()

            user = User.objects.get(pk=user_id)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"msg": "Email verified."}, status=status.HTTP_201_CREATED)
            return Response({"error": "Invalid token"},  status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Invalid UID"},  status=status.HTTP_400_BAD_REQUEST)

#login View
class LoginView(APIView):
    permission_classes =[AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        cache_key = f"user_{email}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"},  status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "Email not verified"},  status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role
        }

        cache.set(cache_key, data, timeout=60 * 2)
        return Response(data, status=status.HTTP_200_OK)

#profile View
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "name": user.name,
            "role": user.role
        })

#logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)

            try:
                token.blacklist()
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({"message": "Token already invalid or blacklisted"}, status=status.HTTP_200_OK)

        except KeyError:
            return Response({"error": "Refresh token is required"},  status=status.HTTP_400_BAD_REQUEST)

#password Reset Request View
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    @rate_limited(max_requests=2,time_window = 60)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = f"{request.build_absolute_uri(reverse('password-reset-confirm'))}?uid={uid}&token={token}"
                #for this check the email and send the link
                # print(uid,token,user)
     
                send_mail(
                    "Reset your password",
                    f"Click to reset your password: {reset_link}",
                    None,
                    [user.email]
                )
                return Response({"msg": "Reset link sent to email"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED)

#password Reset Confirm View
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            try:
                user_id = urlsafe_base64_decode(uid).decode()
                user = User.objects.get(pk=user_id)
                if default_token_generator.check_token(user, token):
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    return Response({"msg": "Password has been reset."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid token"},  status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"error": "Invalid UID"},  status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

# UI SECTION 
# home View
def home(request):
    return render(request, 'home.html')

def loginpage(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')


    return render(request, 'logout.html')