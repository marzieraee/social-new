import email
from email.policy import default
from lib2to3.pgen2.tokenize import TokenError
from wsgiref.util import request_uri
from django.conf import settings
from django.urls import reverse
from rest_framework.response import Response
from django.forms import CharField
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_writable_nested.serializers import WritableNestedModelSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings
from django.db import transaction
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from .util import sendemail
from django.contrib.auth import get_user_model



User = get_user_model()
class CustomRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(min_length=8, write_only=True)
    
    
    def get_cod(self):
        return get_random_string(length=6,allowed_chars='1234567')
    
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password',  'email',)
        

        
        
    # Define transaction.atomic to rollback the save operation in case of error
                

            
    def create(self, validated_data):
        user = User.objects.create(
        email=validated_data['email'],
        username=validated_data['username'],
        
        )
        user.password=make_password(validated_data['password'])
        user.cod=self.get_cod()
        user.save()
        relatatedlink=reverse('verifyemail',)
        current_site=get_current_site(self.context['request']).domain
        email=str(user.email)
        cod=str(user.cod)
        absurl=current_site+relatatedlink+'?email='+user.email+'&cod='+cod
        
        
        
        data={"email_body":absurl,
              "to_email":user.email,"subject":"its ok",} 
        print(data)   
        
        sendemail.send_email(data)
            
            
        return user
        
                                
                    
                
            
            
         
            






# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.name
#         # ...

#         return token
    
    

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

            
            

           
                
class UserProfileSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=CustomUser
        fields=('username','last_login','image','bio','email',)
        read_only_fields = ('last_login',)
        
            
 
        
class UserEditSerializer(WritableNestedModelSerializer):
        # user_related_name=MyUserSerializer()
        
        class Meta:
            
            model = User
            fields = ('username','user_related_name','email')
            
#             def update(self, instance, validated_data):
        
#                 # instance.set_password(validated_data['username'],validated_data['user_related_name'])
#                 # user_data = validated_data.get('user_related_name')
#                 # username = self.data['user_related_name']['username']
#                 # # user = MyUser.objects.get(username=username)
#                 # # user_serializer = MyUserSerializer(data=user_data)
#                 # if user_serializer.is_valid():
#                 #     user_serializer.update(user, user_data)
            
#                 instance.save()

#                 return instance
        
        
        
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
    
    
    


            
            
# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#             required=True,
#             validators=[UniqueValidator(queryset=User.objects.all())]
#             )

#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     # password2 = serializers.CharField(write_only=True, required=True)
    
    
        
        
        # def validate(self, attrs):
        #     if attrs['password'] != attrs['password2']:
        #         raise serializers.ValidationError({"password": "Password fields didn't match."})

            # return attrs
        
       





#     def create(self, validated_data):
        

        
#             user = User.objects.create(
#                 username=validated_data['username'],
#                 email=validated_data['email'],
#             )
#             user.set_password(validated_data['password'])
            
            

#     #     send_mail(
#     #     'Custom Subject',
#     #     None, # Pass None because it's a HTML mail
#     #     'marzyra@yahoo.com',
#     #     [validated_data['email']],
#     #     fail_silently=False,
#     #     html_message = 'template'
#     # )
    
#             # user.save()
#             # username=MyUser.objects.create(username=user,
#             #     image='profile/x22.png'
#             #     ,bio='hi im here')
#             # username.save()
            
#             return user        
#         # return Response({"Error": "Something went wrong"}, status=400)
        
class CommentListSerializer(serializers.ModelSerializer):
    commenter=UserProfileSerializer()
    class Meta:
        
        model=Comment
        
        fields=('body','commenter',)   
         
# class CommentCreatSerializer(serializers.ModelSerializer):
    
#     class Meta:
         
#         model=Comment
        
#         fields=('body',)    

    
class PostSerializer(serializers.ModelSerializer):
    author=UserProfileSerializer(read_only=True)
    posts=CommentListSerializer(many=True,read_only=True)
    class Meta:
        
        model= MyPost
        
        fields=('title','content','likes','author','posts','image','created_date','id',)
        read_only_fields = ('last_login','posts','created_date','author','likes',)

    
    def create(self, validated_data):
        post=MyPost.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            image=validated_data['image'],
            author=self.context['request'].user
        )           
        post.save()
        return post
        
        

        
    
        
        
# class PostCreatSerializer(serializers.ModelSerializer):
#     class Meta:
        
#         model=MyPost
        
#         fields=('title','content','image',)
        
        

       
# class PostUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
        
#         model=MyPost
        
#         fields=('title','content','image')

 
        
        
# class FollowingSerializer(serializers.ModelSerializer):
#     new_following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True, write_only=True)
#     class Meta:
#         model = Following
#         fields = ('user', 'following_user', 'new_following')
#         read_only_fields = ('following_user',)

#     def create(self, validated_data):
#         user = validated_data['user']
#         new_follwoing = validated_data['new_following']
#         user.following.following_user.add(new_follwoing)
#         new_follwoing.followers.following_user.add(user)

#         return user.following