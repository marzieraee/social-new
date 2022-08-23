from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_related_name')
    image=models.ImageField(default='profile/x22.png',upload_to='profile/')
    bio=models.TextField(null=True)





    
class MyPost(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='related_name')
    user_likes = models.ManyToManyField(User,related_name='userlike',blank=True)
    title=models.CharField(max_length=200)
    image = models.ImageField(default='posts/x22.png',upload_to='posts/')
    content=models.TextField(null=True)
    likes = models.PositiveIntegerField(default=0) 
    created_date=models.DateTimeField(auto_now_add=True)
          
    def __str__(self):
        return self.title
    





    
class Comment(models.Model):
    post=models.ForeignKey(MyPost,on_delete=models.CASCADE,related_name='posts',default=1)
    commenter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments',null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
 
 
 

class Follower(models.Model):
    user = models.OneToOneField(User,related_name="followers", on_delete=models.CASCADE)
    follower_user = models.ManyToManyField(User,related_name='follower_user')



class Following(models.Model):
    user = models.OneToOneField(User, related_name="following",unique=False, on_delete=models.CASCADE)
    following_user = models.ManyToManyField(User, related_name='following_user')


     