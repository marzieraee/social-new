from django.urls import reverse
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_writable_nested.serializers import WritableNestedModelSerializer
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
        
        ProfileFallow.objects.create(myprofile=user)
            
        return user
        
                                
                    
                     
class UserProfileSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=CustomUser
        fields=('username','last_login','image','bio','email',)
        read_only_fields = ('last_login',)
        
            
 
        
        
        
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


