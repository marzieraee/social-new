import email
from django.forms import CharField
from rest_framework import serializers

from .models import *


from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class MediaSerialzer(serializers.ModelSerializer):
    

    class Meta:
            model = MediaPeofile
            fields = ('image',)

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

        return user
        
        
class UserEditSerializer(serializers.ModelSerializer):
        class Meta:
            
            model = User
            fields = ('username','email')
            
            def update(self, instance, validated_data):
        
                instance.set_password(validated_data['username'],validated_data['email'])
                instance.save()

                return instance
            
            
                
class UserProfileSerializer(serializers.ModelSerializer):
    media=MediaSerialzer()
    class Meta:
    
        model=User
        
        fields=('username','email','media')
        
        
            
class UserCreatSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model=User
        
        fields=('username','email',)
        
        
        
        
        
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
    
    
    
    
    
    
    
class PostListSerializer(serializers.ModelSerializer):
    author=UserProfileSerializer()
    class Meta:
        
        model= MyPost
        
        fields=('title','contet','likes','author',)
        
        
        
        
class MediaPicSerializer(serializers.ModelSerializer):
    post=PostListSerializer()
    class Meta:
        
        
        fields=('image','post')
        
    
        
        
class PostCreatSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model=MyPost
        
        fields=('title','contet',)
        
        

       
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        
        model=MyPost
        
        fields=('title','contet',)

        
