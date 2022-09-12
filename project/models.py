from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
# Create your models here.
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
   
   
   


class MyPost(models.Model):
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='related_name')
    user_likes = models.ManyToManyField(CustomUser,related_name='userlike',blank=True)
    title=models.CharField(max_length=200)
    image = models.ImageField(default='profile/x22.png',upload_to='posts/',null=True)
    content=models.TextField(max_length=1000)
    likes = models.PositiveIntegerField(default=0) 
    created_date=models.DateTimeField(auto_now_add=True)
          
    def __str__(self):
        return self.title
    





    
class Comment(models.Model):
    post=models.ForeignKey(MyPost,on_delete=models.CASCADE,related_name='posts',default=1)
    commenter = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='comments',null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    
class ProfileFallow(models.Model):
    myprofile=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='myprofile')
    following=models.ManyToManyField(CustomUser,related_name='fallowing')