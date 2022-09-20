from django.urls import reverse
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from login.models import *
from login.serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model




            
 
        
        
        
# class ChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('old_password', 'password', 'password2' )

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})

#         return attrs

#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError({"old_password": "Old password is not correct"})
#         return value

#     def update(self, instance, validated_data):
        
#         instance.set_password(validated_data['password'])
#         instance.save()

#         return instance
    
    
    


            
            





            


        
class CommentSerializer(serializers.ModelSerializer):
    commenter=UserProfileSerializer(read_only=True)
    class Meta:
        
        model=Comment
        
        fields=('body','commenter','post')
        read_only_fields = ('commenter','post')
        
    def create(self, validated_data):
        comment=Comment.objects.create(
            body=validated_data['body'],
            post_id=self.context['pk'],
            commenter=self.context['request'].user
        )
        comment.save()
        return comment

         

    
class PostSerializer(serializers.ModelSerializer):
    author=UserProfileSerializer(read_only=True)
    comment=CommentSerializer(many=True,read_only=True)
    class Meta:
        
        model= MyPost
        
        fields=('title','content','user_likes','author','comment','image','created_date','id',)
        read_only_fields = ('last_login','posts','created_date','user_likes')

    
    def create(self, validated_data):
        post=MyPost.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            image=validated_data['image'],
            author=self.context['request'].user
        )           
        post.save()
        return post


