from django.db import models
from django.contrib.auth.models import User

# Create your models here.



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
    
 
 
 
class Fallow(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_user',null=True)
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user',null=True)

     
     
     