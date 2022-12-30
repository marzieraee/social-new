from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)




class MyUserManager(BaseUserManager):
    def create_user(self, email,password=None,**extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password=None,**extra_fields):

        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            **extra_fields
        )
        
        user.is_active=True
        user.is_admin = True
        
        user.set_password(password)
        user.save(using=self._db)
        return user

   


class CustomUser(AbstractBaseUser):
   username=models.CharField(max_length=20,unique=True)
   image=models.ImageField(default='profile/x22.png',upload_to='profile/')
   bio=models.TextField(default='hi',null=True)
   cod=models.CharField(max_length=20,null=True)
   is_active=models.BooleanField(default=False)
   
   REQUIRED_FIELDS = [ 'username']
   USERNAME_FIELD = ('email')
   email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
   is_active = models.BooleanField(default=False)
   is_admin = models.BooleanField(default=False)

   objects = MyUserManager()

   
   def __str__(self):
        return self.username

   def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

   def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

   @property
   def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
   
   
   


class ProfileFallow(models.Model):
    from_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='following',null=True)
    to_user=models.ForeignKey(CustomUser,related_name='follower',on_delete=models.CASCADE,null=True)
    
   
