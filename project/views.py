from requests import request

from rest_framework.response import Response

from project.paginations import StandardPagination,StandardcommentPagination
from .serializers import *
from .permisions import *
from .models import *
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView, CreateAPIView,RetrieveUpdateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import action


class CommentView(viewsets.ModelViewSet):
    serializer_class=CommentSerializer
    queryset = Comment.objects.all()
    pagination_class=StandardcommentPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request,"pk":self.kwargs["pk"]})
        return context
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PATCH' or 'DELETE':
            permission_classes = [IsAuthenticated,UserIsOwnerCommentOrReadOnly,]
            
        return [permission() for permission in permission_classes]
        
    




class PostByUser(ListAPIView):
    lookup_field = 'username'
    serializer_class = PostSerializer
    permission_classes=(IsAuthenticated,)
    pagination_class=StandardPagination

    queryset = MyPost.objects.all()
    def get_queryset(self,*args, **kwargs):
        qs=super().get_queryset()
        
        return qs.filter(author__username=self.kwargs['username'])        
    
    
class PostView(viewsets.ModelViewSet):
    serializer_class=PostSerializer
    queryset = MyPost.objects.all()
    pagination_class=StandardPagination
    
    def list(self, request, *args, **kwargs):
        
        own_profile = ProfileFallow.objects.filter(to_user=request.user)
        route=request.query_params["route"]
        if route=="home":
            qs=MyPost.objects.filter(author__following__in=own_profile)
        elif route=="explore": 
            qs=MyPost.objects.exclude(author__following__in=own_profile)
        else:
            qs=MyPost.objects.all()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)
        else:   
            return Response({'چنین صفحه ای نداریم '})
    

    
    @action(detail=True, methods=['post','get'])
    def like(self, request,pk):
        obj=self.get_object()
        if request.method=='POST':
            try: 
                MyPost.objects.get(user_likes=request.user,id=pk)
                obj.user_likes.remove(request.user)
                return Response({"لایک رو برداستی"})
            except MyPost.DoesNotExist:
                obj.user_likes.add(request.user)
                return Response({"لایک کردی"})
                
        else:
            try: 
                user_like=obj.user_likes.all()
                serializer=UserProfileSerializer(user_like,many=True)
                return Response(serializer.data)
            except MyPost.DoesNotExist:
                return Response({'چنین پستی نداریم '})            
            
    def get_permissions(self):
        if self.action == 'list' or self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'PATCH' or 'DELETE':
            permission_classes = [IsAuthenticated,UserIsOwnerPostOrReadOnly]
            
        return [permission() for permission in permission_classes]
        
    