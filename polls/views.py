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
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import  EmailMultiAlternatives



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
        
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()        
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                                    value = data["access"],
                                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                        )
                csrf.get_token(request)
                email_template = render_to_string('login_success.html',{"username":user.username})    
                login = EmailMultiAlternatives(
                    "Successfully Login", 
                    "Successfully Login",
                    settings.EMAIL_HOST_USER, 
                     [user.email],
                )
                login.attach_alternative(email_template, 'text/html')
                login.send()
                response.data = {"Success" : "Login successfully","data":data}
                
                return response
            else:
                return Response({"No active" : "This account is not active!!"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"},status=status.HTTP_404_NOT_FOUND)













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
    
    
class CreateComment(CreateAPIView):
    serializer_class = CommentCreatSerializer
    permission_classes=(IsAuthenticated,)

    def get_queryset(self):
        queryset = Comment.objects.filter(post_id=self.kwargs['pk'])
        return queryset
    def perform_create(self,serializer):
        serializer.save(commenter=self.request.user,post_id=self.kwargs['pk'])
    
# class ShowComment(ListAPIView):
#     serializer_class = CommentListSerializer
#     permission_classes=(IsAuthenticated,)

#     def get_queryset(self,*args, **kwargs):
        
#         queryset = Comment.objects.filter(post_id=self.kwargs['pk'])
#         return queryset