from django.db import models
from login.models import CustomUser


class MyPost(models.Model):
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='related_name')
    user_likes = models.ManyToManyField(CustomUser,related_name='userlike',blank=True)
    title=models.CharField(max_length=200)
    image = models.ImageField(default='profile/x22.png',upload_to='posts/',null=True)
    content=models.TextField(max_length=1000)
    created_date=models.DateTimeField(auto_now_add=True)
          
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ("-created_date",)

    
class Comment(models.Model):
    post=models.ForeignKey(MyPost,on_delete=models.CASCADE,related_name='comment',default=1)
    commenter = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='commenter',null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
      
    
