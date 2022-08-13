


from .models import *
# Create your views here.
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework import generics
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,CreateAPIView,RetrieveUpdateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
# from .paginations import * 
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            print(attrs['refresh'])
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

class CookieTokenObtainPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True , samesite='None', secure=True)
        del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True  ,samesite='None', secure=True)
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


class ShowPic(RetrieveAPIView):
    serializer_class = MediaSerialzer
    queryset = MediaPeofile.objects.all()
    lookup_field = 'user__username'
   
    
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
    permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
    queryset = MyPost.objects.all()
    serializer_class = PostUpdateSerializer
    
    def get_queryset(self):
        
        qs=super().get_queryset()
        return qs.filter(author=self.request.user)

    
class SetImageProfile(UpdateAPIView):
    
    permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
    queryset = MediaPeofile.objects.all()
    serializer_class = MediaSerialzer
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

