import profile

from rest_framework.response import Response
from .serializers import *
from .permisions import *
from .models import *
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView, CreateAPIView,RetrieveUpdateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status, viewsets







    
    
    
    
class ShowEditDelPost(RetrieveUpdateDestroyAPIView) :
    queryset = MyPost.objects.all()

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
    queryset = MyPost.objects.all()

    serializer_class = PostSerializer
    def get_queryset(self):
        super().get_queryset()
        username=self.kwargs['username']
        
        queryset = MyPost.objects.filter(author__username=username)
 
        return queryset
     
     
class Home(ListAPIView):
    
    
    queryset = MyPost.objects.all()

    serializer_class = PostSerializer
    
    def get_queryset(self):
        
        own_profile = self.request.user.myprofile.first()
        myfollowing=own_profile.following.all()
        
        return MyPost.objects.filter(author__in=myfollowing)
    
    
class Explore(ListAPIView):
    
    

    serializer_class = PostSerializer
    
        
    MyPost.objects.all()
   
    


        
class CreateComment(CreateAPIView):
    serializer_class=CommentSerializer
# permission_classes=(IsAuthenticated,)
    def perform_create(self,serializer):
        serializer.save(commenter=self.request.user,post_id=self.kwargs['pk'])
    
    
    
class DeleteComment(DestroyAPIView):
        serializer_class=CommentSerializer
        queryset = Comment.objects.all()

        permission_classes=(IsAuthenticated,)
    
    

    