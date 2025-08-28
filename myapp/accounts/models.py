from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager , PermissionsMixin
from myapp.accounts.constants import Rolechoice
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models.signals import pre_save
# Create your models here.

# Define Role choices
class UserManager(BaseUserManager):
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
    
def task_file_upload_path(instance, filename):
    role = instance.role.replace(" ", "_")
    name = instance.name.replace(" ", "_")
    ext = filename.split('.')[-1]
    new_filename = f"{name}.{ext}"
    return os.path.join("profile_images/", role, new_filename)    


# Define User model here 
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    profile = models.ImageField(upload_to=task_file_upload_path,default='Default_images/default.jpg', blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=Rolechoice,default=Rolechoice.EMPLOYEE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    
    objects = UserManager()
    def __str__(self):
        return f"{self.name}"
    
    
    
# delete profile image from filesystem when user is deleted
@receiver(post_delete, sender=User)
def delete_profile_image_on_user_delete(sender, instance, **kwargs):
    if instance.profile and instance.profile.name != 'Default_images/default.jpg':
        if os.path.isfile(instance.profile.path):
            os.remove(instance.profile.path)
            
            
# update profile image and delete old image from filesystem
@receiver(pre_save, sender=User)
def delete_old_profile_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False  # New user, no old image yet

    try:
        old_instance = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return False

    old_file = old_instance.profile
    new_file = instance.profile

    if old_file and old_file != new_file and old_file.name != 'Default_images/default.jpg':
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

