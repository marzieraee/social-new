
from .models import *
from project.models import *
from .utils import sendemail
from django.urls import reverse
from rest_framework import exceptions
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import exceptions, serializers
from django.utils.http import urlsafe_base64_encode 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import RefreshToken, TokenObtainSerializer,TokenRefreshSerializer




def get_cod():
    '''this func make random code'''
    return get_random_string(length=6,allowed_chars='1234567')



def make_email(email,cod,request):
    '''this func get email and cod then hash email ,absurl is the link that send to client,so return sending email'''
    
    emailhash=urlsafe_base64_encode(force_bytes(email))
    cod = urlsafe_base64_encode(force_bytes(cod))
    absurl= 'http://localhost:3001'+'/verify/confirmation'+'?email='+emailhash+'&token='+cod
    data={"email_body":absurl,
        "to_email":email,"subject":"its ok",} 
    send=sendemail.send_email(data) 
    return send
    
class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    
    '''this class inherit TOS that get username filed and pass and serilize them, in this class we customize 
    validations if the email dosent exist then response,or if it exist but isnt active send them activations
    email,and say them to check their email'''
    
    def validate(self,attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        
        try:
         user = CustomUser.objects.get(email=authenticate_kwargs['email'])
         if not user.is_active:
            self.error_messages['no_active_account']=_(
                 'ایمیل شما تایید نشده است لطفا مجددا ایمیل خود را بررسی کنید'
             )
            cod=MyTokenObtainPairSerializer.get_token(user)
            request=self.context['request']

            make_email(user.email,cod,request)
            raise exceptions.AuthenticationFailed(
                 self.error_messages['no_active_account'],
                 'ایمیل شما تایید نشده است لطفا مجددا ایمیل خود را بررسی کنید',
             )
        except CustomUser.DoesNotExist:
          self.error_messages['no_active_account'] =_(
              'لطفا ابتدا ثبت نام کنید')
          raise exceptions.AuthenticationFailed(
              self.error_messages['no_active_account'],
              'لطفا مجددا تلاش کنید',
          )
        print(super().validate(attrs))
        return super().validate(attrs)
    
    
    
class MyTokenObtainPairSerializer(CustomTokenObtainPairSerializer):
    
    
    '''calling refresh token and adding another feature 
    in validate,valid_data of access and refresh token send to view  to login '''
    
    @classmethod
    
    def get_token(cls, user):
        token=RefreshToken.for_user(user)
        token['name'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

    
    
class CookieTokenRefreshSerializer(TokenRefreshSerializer):

    '''here we get refresh token from cookie and then send it to view'''
    
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')
        
   
User=get_user_model()            
     
class UserProfileSerializer(serializers.ModelSerializer):
    
    '''this is a usefull class for me as you see,i use it in register and all doing that it dose for user,
    you follow check you follow the person or not!'''
   
   
    postcount=serializers.SerializerMethodField()
    youfollow=serializers.SerializerMethodField()
    myimage=serializers.SerializerMethodField()
    followercount=serializers.SerializerMethodField()
    followingcount=serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    
    
    def get_followercount(self,obj):
        try:
            count = ProfileFallow.objects.filter(to_user=obj).count()
            return count
        except ProfileFallow.DoesNotExist:
                pass
            
    def get_followingcount(self,obj):
        try:
            count = ProfileFallow.objects.filter(from_user=obj).count()
            return count
        except ProfileFallow.DoesNotExist:
                pass
    
  
    def get_postcount(self,obj):
        count = MyPost.objects.filter(author=obj).count()
        return count
        
    def get_youfollow(self,obj):
        if self.context['request'].user != obj:
            try:
                ProfileFallow.objects.get(from_user=self.context['request'].user,to_user=obj)
                return True
            except:
                
                return False
        else:
            
            return {'ITS YOURSELF'}
            
    def get_myimage(self, obj):
        
        '''myimage is for the time that user want to edit his profile exclude image,the myimage put instead of image in edit profile,
            it convert the former image url to valid format for again saving '''
        try:
            return self.context["request"].build_absolute_url("/").strip("/")+str(obj.image.url)
        except Exception as E:
            print(E)
            return str("")

    class Meta:
        model=CustomUser
        fields=('username','image','bio','email','id','postcount','password','last_login','myimage','youfollow','followercount','followingcount')
        read_only_fields = ('id','postcount','last_login','youfollow','myimage','followercount','followingcount')
        extra_kwargs = {
        "username": {
            "validators": [],
        },
        "email": {
            "validators": [],
            },
        "bio": {
            "validators": [],
            },
        "image":{
            "validators": [],
            },
        "password":{
            "validators": [],
            }
       }  
                
    
        
    def validate(self, value):
       
    
        return value
    def update(self, instance, validated_data):
        try :
            CustomUser.objects.filter(username=instance["username"]).exists()
            raise serializers.ValidationError({'detail':'با این نام کاربری یا ایمیل قبلا وارد شده است '})
        except:
            instance.username = validated_data.get('username', instance.username)
            instance.save()
            return instance        
        
  
    def create(self, validated_data):
        if CustomUser.objects.filter(username=validated_data["username"]).exists() or CustomUser.objects.filter(email=validated_data["email"]).exists()  :
            raise serializers.ValidationError({'detail':'با این نام کاربری یا ایمیل قبلا ثبت نام شده است '})
        if len(validated_data['password'])<8 :
            raise serializers.ValidationError({'detail':'پسورد باید بیش از ۸ کارکتر باشد'})
        created=User.objects.create(email=validated_data['email'],username=validated_data['username'])
        created.password=make_password(validated_data['password'])
        cod=str(MyTokenObtainPairSerializer.get_token(created))
        created.save()
        email=str(created.email)

        request=self.context['request']
        make_email(email,cod,request)
        return created



class FollowerSerializer(serializers.ModelSerializer):
    
   from_user=UserProfileSerializer()
   class Meta:
        model=ProfileFallow
        fields=('from_user',)
        read_only_fields = ('from_user',)
        
        
        
        
        
class FollowingSerializer(serializers.ModelSerializer):
    to_user=UserProfileSerializer()
    class Meta:
        model=ProfileFallow
        fields=('to_user',)
        read_only_fields = ('to_user',)
        
        
        

    
