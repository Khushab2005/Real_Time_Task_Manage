from rest_framework import serializers
from myapp.accounts.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from myapp.accounts.constants import Rolechoice

# Create User Serializer
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name','profile', 'email', 'password', 'role']

    def validate(self, attrs):
        request_user = self.context['request'].user
        role = attrs.get('role')

        if role == Rolechoice.ADMIN:
            raise serializers.ValidationError("You do not have permission to create an admin.")

        if request_user.role == Rolechoice.MANAGER and role != Rolechoice.EMPLOYEE:
            raise serializers.ValidationError("Manager can only create employees.")
        
        if request_user.role == Rolechoice.EMPLOYEE:
            raise serializers.ValidationError("Employees cannot create users.")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = False  
        user.save()

        self.send_email_verification(user)
        return user

    def send_email_verification(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_path = reverse('verify-email')
        activation_link = f"{self.context['request'].build_absolute_uri(activation_path)}?uid={uid}&token={token}"
        #for this check the email and send the link
        # print(activation_link)
        send_mail(
            subject="Verify your email",
            message=f"Click the link to verify your account: {activation_link}",
            from_email=None,
            recipient_list=[user.email],
        )

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


#password Reset Confirm Serializer
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    def validate(self, attrs):
        if attrs['new_password']!=attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
