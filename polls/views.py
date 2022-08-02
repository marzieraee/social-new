from django.shortcuts import render


from urllib import request
from django.shortcuts import get_object_or_404

from .models import *
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,CreateAPIView,RetrieveUpdateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
# from .paginations import * 
from rest_framework import status,permissions
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

class CookieTokenObtainPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
        del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
    
class UserIsOwnerPostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user.id    

class SignUp(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    


class Profile(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes=(IsAuthenticated,)

   
    
class EditProfile(RetrieveUpdateAPIView) :
    queryset = User.objects.all()
    lookup_field = 'username'

    serializer_class = UserEditSerializer
    
    permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
    
    
          
        
        
class ChangePass(RetrieveUpdateAPIView):
    lookup_field = 'username'
    serializer_class = ChangePasswordSerializer
    permission_classes=(IsAuthenticated,)
    

    queryset = User.objects.all()
    def get_queryset(self):
            
        qs=super().get_queryset()
        return qs.filter(username=self.request.user)

class PostList(ListAPIView):
    serializer_class = PostListSerializer
    
    queryset = MyPost.objects.all()
    
    
    

class CreatPost(CreateAPIView):
    serializer_class = PostCreatSerializer
    permission_classes=(IsAuthenticated,)

    queryset = MyPost.objects.all()
    
    def perform_create(self,serializer):
        serializer.save(author=self.request.user)
        



class SinglePost(RetrieveAPIView):
    serializer_class = PostListSerializer
    
    queryset = MyPost.objects.all()
   


class EditPost(UpdateAPIView):
    permission_classes=(IsAuthenticated,)
    queryset = MyPost.objects.all()
    serializer_class = PostUpdateSerializer
    
    def get_queryset(self):
        
        qs=super().get_queryset()
        return qs.filter(author=self.request.user)

    
class SetImageProfile(UpdateAPIView):
    
    permission_classes=(IsAuthenticated,)
    queryset = MediaPeofile.objects.all()
    serializer_class = MediaSerialzer
    lookup_field = 'username'
    def get_queryset(self):
        
        qs=super().get_queryset()
        return qs.filter(user=self.request.user)
    
    
