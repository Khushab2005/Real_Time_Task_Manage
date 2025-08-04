from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
from myapp.accounts.constants import ROLE_CHOICES
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, name ,email, password=None,role='employee'):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            name=name,
            email=self.normalize_email(email),
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, name, email, password):
        user = self.create_user(
            name=name,
            email=email,
            password=password,
            role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    objects = UserManager()
    def __str__(self):
        return f"{self.name} - {self.email} - {self.role}"
    
    