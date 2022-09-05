from django.shortcuts import render
from requests import request
from .serializers import *
from .permisions import *
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,CreateAPIView,RetrieveUpdateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import action







class SignUp(CreateAPIView):
    
    
    serializer_class = CustomRegisterSerializer
    




class VerifyEmail(APIView):
    
    serializer_class=CustomRegisterSerializer
    def patch(self,request,*args, **kwargs):
        try:
            user = User.objects.get(email=request.GET.get('email'))
        except User.DoesNotExist:
            user = None
                              
        if user.cod == request.GET.get('cod'):
            user.is_active=True
            user.save()
        else:
            return Response({'isnot mach'},status=400)
    
        return Response({'chek your email'},status=200)
    
    
    
    
    
class Profile(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    
    
    
    
class ShowEditDelProfile(RetrieveUpdateDestroyAPIView) :
    queryset = User.objects.all()
    lookup_field = 'username'

    serializer_class = UserProfileSerializer
    
    # permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
    def get_queryset(self):
        super().get_queryset()
        if self.request.method=='GET':
               queryset = User.objects.all()
        else:
               queryset = User.objects.filter(username=self.request.user.username)
 
        return queryset
    
    def get_permissions(self):
        
        if self.request.method in permissions.SAFE_METHODS:
             return (permissions.AllowAny(),)
        return (IsAuthenticated(), UserIsOwnerOrReadOnly(),)
    
    
    
    
    
class ShowEditDelPost(RetrieveUpdateDestroyAPIView) :
    queryset = User.objects.all()

    serializer_class = PostSerializer
    
    # permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
    def get_queryset(self):
        super().get_queryset()
        if self.request.method=='GET':
               queryset = MyPost.objects.all()
        else:
               queryset = MyPost.objects.filter(author=self.request.user)
 
        return queryset
    
    def get_permissions(self):
        
        if self.request.method in permissions.SAFE_METHODS:
             return (permissions.AllowAny(),)
        return (IsAuthenticated(), UserIsOwnerPostOrReadOnly(),)
    
    
    
class CreatePost(CreateAPIView):
    serializer_class=PostSerializer
    permission_classes=(IsAuthenticated,)
    



class PostByUser(ListAPIView):
    lookup_field='username'
    queryset = User.objects.all()

    serializer_class = PostSerializer
    def get_queryset(self):
        super().get_queryset()
        username=self.kwargs['username']
        
        queryset = MyPost.objects.filter(author__username=username)
 
        return queryset
     
     