
from rest_framework import serializers
from polls.models import User
from django.urls import reverse
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from project.models import *

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from .utils import sendemail
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['name'] = user.username
        # ...
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
    
    
    def get_cod(self):
        return get_random_string(length=6,allowed_chars='1234567')
    
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password',  'email',)                

            
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
        
                                
                    
                     
class UserProfileSerializer(serializers.ModelSerializer):
    follower=serializers.SerializerMethodField()
    following=serializers.SerializerMethodField()
    postcount=serializers.SerializerMethodField()

        

    def get_follower(self,obj):
        try:
            count=ProfileFallow.objects.get(myprofile=obj).following.count()
            return count
        except ProfileFallow.DoesNotExist:
                pass
    
    def get_following(self,obj):
        count=0
        alluser=CustomUser.objects.all()
        for singleuser in alluser:
            try:
                ProfileFallow.objects.get(myprofile=singleuser,following=obj)
                count=+1
            except ProfileFallow.DoesNotExist:
                pass
        return count
    
    def get_postcount(self,obj):
        count=MyPost.objects.filter(author=obj).count()
        return count
        
            

   
    class Meta:
        model=CustomUser
        fields=('username','last_login','image','bio','email','id','follower','following','postcount',)
        read_only_fields = ('last_login','id')
        