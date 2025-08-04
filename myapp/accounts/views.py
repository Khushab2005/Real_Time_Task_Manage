from rest_framework.decorators import api_view , APIView
from rest_framework.response import Response
from rest_framework import  permissions
from myapp.accounts.serializers import *
from myapp.accounts.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import status

#Register View
class RegisterView(APIView):
    def post(self, request):
        ser = RegisterSerializer(data=request.data, context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response({"msg": "Check your email to verify."}, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)



#Verify Email View
class VerifyEmailView(APIView):
    def get(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"msg": "Email verified."}, status=200)
            return Response({"error": "Invalid token"}, status=400)
        except:
            return Response({"error": "Invalid UID"}, status=400)

#login View
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.is_active:
            return Response({"error": "Email not verified"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role
        })


#profile View
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
            token.blacklist()
            return Response({"message": "Logout successful"}, status=200)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=400)
        except TokenError as e:
            return Response({"error": str(e)}, status=400)

#password Reset Request View
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = f"{request.build_absolute_uri(reverse('password-reset-confirm'))}?uid={uid}&token={token}"
                send_mail(
                    "Reset your password",
                    f"Click to reset your password: {reset_link}",
                    None,
                    [user.email]
                )
                return Response({"msg": "Reset link sent to email"}, status=200)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
        return Response(serializer.errors, status=400)

#password Reset Confirm View
class PasswordResetConfirmView(APIView):
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
                    return Response({"msg": "Password has been reset."}, status=200)
                else:
                    return Response({"error": "Invalid token"}, status=400)
            except:
                return Response({"error": "Invalid UID"}, status=400)
        return Response(serializer.errors, status=400)

    