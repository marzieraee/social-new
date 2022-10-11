
from ast import IsNot
from crypt import methods
from rest_framework import serializers
from polls.models import User
from django.urls import reverse
from rest_framework import serializers
from .models import *
from project.models import *
from rest_framework import exceptions, serializers
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from .utils import sendemail
from django.contrib.auth import get_user_model, authenticate
import json
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# def get_cod():
#     return get_random_string(length=6,allowed_chars='1234567')

# class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    
#     def validate(self, attrs):
#         authenticate_kwargs = {
#             self.username_field: attrs[self.username_field],
#             'password': attrs['password'],
#         }
        
        
#         try:
#             authenticate_kwargs['request'] = self.context['request']
#         except KeyError:
#             pass
#         try :
#             myuser=CustomUser.objects.get(email=attrs['email'],password=attrs['password'])
            
#             if myuser and myuser.is_active()==False:
#                 code=get_cod()
#                 main={"email_body":code,
#             "to_email":myuser.email,"subject":"its ok",} 
#                 sendemail.send_email(main)
#                 myuser.cod=code
#                 myuser.save()
#             elif myuser and myuser.is_active()==True:
        
#                 self.user = authenticate(**authenticate_kwargs)
#                 print(self.user)
#         except:
#                 # raise Exception({'ثبت نام کن '})     
#             if self.user is None or not self.user.is_active:
#                 self.error_messages['no_active_account'] = _(
#                     'No active account found with the given credentials') 
#                 raise exceptions.AuthenticationFailed(
#                     self.error_messages['no_active_account'],
#                     'no_active_account',
#                 )
#             return super().validate(attrs)   



    
    
    
    
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['name'] = user.username
        return token 
    
    
class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            print(attrs['refresh'])
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')
        


User = get_user_model()
class CustomRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(min_length=8, write_only=True)
    
    
    
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password',  'email',)                

    

            
   
    def create(self, validated_data):
        relatatedlink=reverse('verifyemail',)
        current_site=get_current_site(self.context['request']).domain
        created=User.objects.create(email=validated_data['email'],username=validated_data['username'])
            
        email=str(created.email)
        cod=str(created.cod)
        absurl=current_site+relatatedlink+'?email='+email+'&cod='+cod
        data={"email_body":absurl,
            "to_email":created.email,"subject":"its ok",} 
           
        created.password=make_password(validated_data['password'])
        created.cod=self.get_cod()
        created.save()
        print(data)   
        sendemail.send_email(data)
        return Response({'لطفا ایمیل خود را چک کنید'},created)
    
    
    
       
        

                   
                     
class UserProfileSerializer(serializers.ModelSerializer):
    postcount=serializers.SerializerMethodField()
    followingcount=serializers.SerializerMethodField()
    followercount=serializers.SerializerMethodField()
    
            

    
    
    def get_followercount(self,obj):
        obj1=ProfileFallow.objects.get(myprofile=obj)
        
        try:
            count=ProfileFallow.objects.filter(following=obj).count()
            return count
        except ProfileFallow.DoesNotExist:
                pass
        
        
        
            
    def get_followingcount(self,obj):
        obj1=ProfileFallow.objects.get(myprofile=obj)
        try:
            count=ProfileFallow.objects.get(myprofile=obj).following.count()
            return count
        except ProfileFallow.DoesNotExist:
                pass
    
  
    def get_postcount(self,obj):
        count=MyPost.objects.filter(author=obj).count()
        return count
        
            

   
    class Meta:
        model=CustomUser
        fields=('username','image','bio','email','id','followingcount','postcount','last_login','followercount')
        read_only_fields = ('email','id','postcount','followingcount','last_login','followercount')
        
        
    
  

class ProfileSerializer(serializers.ModelSerializer):
    myprofile=serializers.CharField(source='myprofile.username')
    following=UserProfileSerializer(many=True)
    
  
            
    class Meta:
        model=ProfileFallow
        fields=('myprofile','following')
        read_only_fields = ('myprofile','following')
        
        
        

    