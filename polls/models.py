from email.policy import default
import profile
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class MyUser(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_related_name')
    email=models.EmailField()
    

class MediaPeofile(models.Model):
    user=models.ForeignKey(User,related_name='media',on_delete=models.CASCADE)
    image=models.ImageField(default='profile/x22.png',upload_to='profile/') 
    
    
class MyPost(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='related_name')
    user_likes = models.ManyToManyField(User,related_name='userlike',blank=True)
    title=models.CharField(max_length=200)
    image = models.ImageField(default='posts/x22.png',upload_to='posts/')
    contet=models.TextField(null=True)
    likes = models.PositiveIntegerField(default=0) 
    created_date=models.DateTimeField(auto_now_add=True)
          
    def __str__(self):
        return self.title
    




class MediaPic(models.Model):
    image=models.ImageField(null=True,blank=True,default='',upload_to='posts/') 
    post=models.ForeignKey(MyPost,related_name='pic',on_delete=models.CASCADE)
    
    
class Comment(models.Model):
    post=models.ForeignKey(MyPost,on_delete=models.CASCADE,related_name='posts',default=1)
    commenter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments',null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)