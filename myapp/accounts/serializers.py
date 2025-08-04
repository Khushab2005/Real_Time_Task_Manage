from rest_framework import serializers
from myapp.accounts.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

# Register Serializer 
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'confirm_password','role')
    
    def validate(self, attrs):
        if attrs['password']!=attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
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
        send_mail(
            subject="Verify your email",
            message=f"Click to verify: {activation_link}",
            from_email=None,
            recipient_list=[user.email],
        )

#password Reset Request Serializer 
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
