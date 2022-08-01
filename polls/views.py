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
    
    
