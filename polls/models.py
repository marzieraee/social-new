from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# class UserManager(BaseUserManager):
    
#     def _create_user(self, email, password, **extra_fields):
#         user = self.model(email=self.normalize_email(email), **extra_fields)
#         user.set_password(password)        
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password, **extra_fields):
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self._create_user(email, password, **extra_fields)


# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=255, unique=True)
   
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     # Add other fields here

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []




    

    


    