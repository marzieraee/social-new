from ast import Expression
from asyncio import exceptions
import email
from email.mime import image
from lib2to3.pgen2.tokenize import TokenError
from urllib import request
from django.forms import CharField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from drf_writable_nested.serializers import WritableNestedModelSerializer


class MediaSerialzer(serializers.ModelSerializer):
   class Meta:
        model = MediaPeofile
        fields = ('image','user')

class MediaproSerialzer(serializers.ModelSerializer):
       class Meta:
        model = MediaPeofile
        fields = ('image',)
        
class CaptionSerialzer(serializers.ModelSerializer):
       class Meta:
        model = Cptions
        fields = ('bio','user')

        
        
            
            
class MyUserSerializer(serializers.ModelSerializer):
        
        class Meta:
            
            model = MyUser
            fields = ('username','image','bio')
            
            
           
                
class UserProfileSerializer(serializers.ModelSerializer):
    user_related_name = MyUserSerializer()
   
    class Meta:
        model=User
        fields=('username','email','date_joined','last_login','user_related_name',)
    
    
            
class UserSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model=User
        
        fields=('username','email',)
        
            
        
class UserEditSerializer(WritableNestedModelSerializer):
        user_related_name=MyUserSerializer()
        
        class Meta:
            
            model = User
            fields = ('username','user_related_name')
            
            def update(self, instance, validated_data):
        
                instance.set_password(validated_data['username'],validated_data['user_related_name'])
                user_data = validated_data.get('user_related_name')
                username = self.data['user_related_name']['username']
                user = MyUser.objects.get(username=username)
                user_serializer = MyUserSerializer(data=user_data)
                if user_serializer.is_valid():
                    user_serializer.update(user, user_data)
            
                instance.save()

                return instance
        
        
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2' )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    
    
    


            
            
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email',)
    
    
    
        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})

            return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()
        username=MyUser.objects.create(username=user,
            image='profile/x22.png'
            ,bio='hi im here')
        username.save()
        
        return user        
            
class CommentListSerializer(serializers.ModelSerializer):
    commenter=UserProfileSerializer()
    class Meta:
        
        model=Comment
        
        fields=('body','commenter',)   
         
class CommentCreatSerializer(serializers.ModelSerializer):
    
    class Meta:
         
        model=Comment
        
        fields=('body',)    

    
class PostListSerializer(serializers.ModelSerializer):
    author=UserProfileSerializer()
    posts=CommentListSerializer(many=True)
    class Meta:
        
        model= MyPost
        
        fields=('title','content','likes','author','posts','image','id','created_date')
                
        
        
class MediaPicSerializer(serializers.ModelSerializer):
    post=PostListSerializer()
    class Meta:
        
        
        fields=('image','post')
        
    
        
        
class PostCreatSerializer(serializers.ModelSerializer):
    class Meta:
        
        model=MyPost
        
        fields=('title','content','image',)
        
        

       
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        
        model=MyPost
        
        fields=('title','content','image')

 
        
        
class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()
    
    
    def validate(self, attrs):
        self.token=attrs['refresh']
        
        return attrs
    
    def save(self, **kwargs):
        
        try:
            RefreshToken(self.token).blacklist()
        
        except TokenError:
            self.fail('bad token')
        
        

