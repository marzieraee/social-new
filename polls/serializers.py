import email
from lib2to3.pgen2.tokenize import TokenError
from django.forms import CharField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.name
        # ...

        return token
    
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

            
            
class MyUserSerializer(serializers.ModelSerializer):
        
        class Meta:
            
            model = MyUser
            fields = ('id','image','bio')
            
            
           
                
class UserProfileSerializer(serializers.ModelSerializer):
    user_related_name = MyUserSerializer()
   
    class Meta:
        model=User
        fields=('username','email','date_joined','last_login','user_related_name',)
    
    
            
class UserSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        
        model=User
        
        fields=('username','email',)
        
            
        
class UserEditSerializer():
        user_related_name=MyUserSerializer()
        
        class Meta:
            
            model = User
            fields = ('username','user_related_name','email')
            
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
                
        
        

        
    
        
        
class PostCreatSerializer(serializers.ModelSerializer):
    class Meta:
        
        model=MyPost
        
        fields=('title','content','image',)
        
        

       
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        
        model=MyPost
        
        fields=('title','content','image')

 
        
        
class FollowingSerializer(serializers.ModelSerializer):
    new_following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True, write_only=True)
    class Meta:
        model = Following
        fields = ('user', 'following_user', 'new_following')
        read_only_fields = ('following_user',)

    def create(self, validated_data):
        user = validated_data['user']
        new_follwoing = validated_data['new_following']
        user.following.following_user.add(new_follwoing)
        new_follwoing.followers.following_user.add(user)

        return user.following