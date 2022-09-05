from .models import *
# # Create your views here.
# from .serializers import *
# from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,CreateAPIView,RetrieveUpdateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
# # from .paginations import * 
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.response import Response
# from rest_framework import status 
# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView 
# from rest_framework_simplejwt.serializers import TokenRefreshSerializer
# from rest_framework_simplejwt.exceptions import InvalidToken



# class SignUp(CreateAPIView):
#     serializer_class = CustomRegisterSerializer
    


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
        
#         }





   
    




# # 'use for profile'
# class Profile(RetrieveAPIView):
#     # permission_classes=(IsAuthenticated,)
#     serializer_class = UserProfileSerializer
#     queryset = User.objects.all()
#     lookup_field = 'username'
    
    
    

        
        
# class Mypost(ListAPIView):
#     lookup_field = 'username'
#     serializer_class = PostListSerializer
#     permission_classes=(IsAuthenticated,)
#     queryset = MyPost.objects.all()
#     def get_queryset(self):
#         qs=super().get_queryset()
        
#         return qs.filter(author=self.request.user)


# class PostByUser(ListAPIView):
#     lookup_field = 'username'
#     serializer_class = PostListSerializer
#     permission_classes=(IsAuthenticated,)
#     queryset = MyPost.objects.all()
#     def get_queryset(self,*args, **kwargs):
#         qs=super().get_queryset()
        
#         return qs.filter(author__username=self.kwargs['username'])        
        
        
        
# class ChangePass(RetrieveUpdateAPIView):
#     lookup_field = 'username'
#     serializer_class = ChangePasswordSerializer
#     permission_classes=(IsAuthenticated,)
    

#     queryset = User.objects.all()
#     def get_queryset(self):
            
#         qs=super().get_queryset()
#         return qs.filter(username=self.request.user)

# class PostList(ListAPIView):
#     serializer_class = PostListSerializer
    
#     queryset = MyPost.objects.all()
    
    
    

# class CreatPost(CreateAPIView):
#     serializer_class = PostCreatSerializer
#     permission_classes=(IsAuthenticated,)

#     queryset = MyPost.objects.all()
    
#     def perform_create(self,serializer):
        
#         serializer.save(author=self.request.user)
        
#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         return Response({
#             'status': 200,
            
#         })


# class SinglePost(RetrieveAPIView):
#     serializer_class = PostListSerializer
    
#     queryset = MyPost.objects.all()
   


# class EditPost(RetrieveUpdateDestroyAPIView):
#     permission_classes=(IsAuthenticated,)
#     queryset = MyPost.objects.all()
#     serializer_class = PostUpdateSerializer
    
#     def get_queryset(self):
        
#         qs=super().get_queryset()
#         return qs.filter(author=self.request.user)

    

    
    
# class CreateComment(CreateAPIView):
#     serializer_class = CommentCreatSerializer
#     permission_classes=(IsAuthenticated,)

#     def get_queryset(self):
#         queryset = Comment.objects.filter(post_id=self.kwargs['pk'])
#         return queryset
#     def perform_create(self,serializer):
#         serializer.save(commenter=self.request.user,post_id=self.kwargs['pk'])
    
# # class ShowComment(ListAPIView):
# #     serializer_class = CommentListSerializer
# #     permission_classes=(IsAuthenticated,)

# #     def get_queryset(self,*args, **kwargs):
        
# #         queryset = Comment.objects.filter(post_id=self.kwargs['pk'])
# #         return queryset

# class MyProfile(RetrieveUpdateAPIView):
#     lookup_field = 'username'
#     permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
#     queryset = User.objects.all()
#     serializer_class = UserEditSerializer
#     def get_queryset(self):
        
#         qs=super().get_queryset()
#         return qs.filter(username=self.request.user)
    
#     def get_serializer_class(self):
#             if self.request.method=='GET':
#                 return UserProfileSerializer

#             else:
#                 return UserEditSerializer
        
        

   
   
# # class fallow(CreateAPIView):
# #     serializer_class = FallowSerializer
# #     permission_classes=(IsAuthenticated,)
    

    
# #     def perform_create(self,serializer,*args, **kwargs):
# #         serializer.save(from_user=self.request.user,to_user=kwargs['pk'])
        
        
# #     def create(self, request, *args, **kwargs):
# #         response = super().create(request, *args, **kwargs)
# #         return Response({
# #         'status': 200,
# #         })




# class FollowingView(ListCreateAPIView):
#     queryset = Following.objects.all()
#     serializer_class = FollowingSerializer
#     permission_classes = [IsAuthenticated]