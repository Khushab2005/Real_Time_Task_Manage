from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
from myapp.accounts.constants import Rolechoice
import os
# Create your models here.

# Define Role choices
class UserManager(BaseUserManager):
    # Create a new user with the given email and password.
    # The email must be normalized and unique.
    # The role must be one of the choices defined in ROLE_CHOICES.
    # The is_staff and is_active flags are set to False by default.
    # The password is set using set_password method.
    # The user is saved using the provided database.
    def create_user(self, name ,email, password):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            name=name,
            email=self.normalize_email(email), 
            role=Rolechoice.EMPLOYEE,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_manager(self, name, email, password):
        if not email:
            raise ValueError("Email is required")
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            role=Rolechoice.MANAGER,)
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, password):
        if not email:
            raise ValueError("Email is required")
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            role=Rolechoice.ADMIN,)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
def upload_path(instance, filename):
    role = instance.role.replace(" ", "_")
    name = instance.name.replace(" ", "_")
    ext = filename.split('.')[-1]
    new_filename = f"{name}.{ext}"
    return os.path.join("profile_images/", role, new_filename)    


# Define User model here 
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=True)
    profile = models.ImageField(upload_to=upload_path, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=Rolechoice,default=Rolechoice.EMPLOYEE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    
    objects = UserManager()
    def __str__(self):
        return f"{self.name} - {self.email} - {self.role}"
    
    