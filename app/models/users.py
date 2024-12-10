from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _  # Import this




class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)  # Make email unique
    phone_number = models.CharField(max_length=15, default="", blank=True,unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)  # Profile photo field
    
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'  # Use email as the username
    REQUIRED_FIELDS = ['username','phone_number']  # No additional fields required


User = get_user_model()

