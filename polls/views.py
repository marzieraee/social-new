from .models import *
# Create your views here.
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
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



# class CookieTokenRefreshSerializer(TokenRefreshSerializer):
#     refresh = None
#     def validate(self, attrs):
#         attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
#         if attrs['refresh']:
#             print(attrs['refresh'])
#             return super().validate(attrs)
#         else:
#             raise InvalidToken('No valid token found in cookie \'refresh_token\'')

#     def finalize_response(self, request, response, *args, **kwargs):
#         if response.data.get('refresh'):
#             cookie_max_age = 3600 * 24 * 14 # 14 days
#             response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True , samesite='None',secure=True)
#             del response.data['refresh']
# # class CookieTokenObtainPairView(TokenObtainPairView):
    
#     serializer_class = MyTokenObtainPairSerializer
#     def post(self, request, *args, **kwargs):
#         # you need to instantiate the serializer with the request data
#         serializer = self.get_serializer(data=request.data)
#         # you must call .is_valid() before accessing validated_data
#         serializer.is_valid(raise_exception=True)  

#         # get access and refresh tokens to do what you like with
#         access = serializer.validated_data.get("access", None)
#         refresh = serializer.validated_data.get("refresh", None)
#         email = serializer.validated_data.get("email", None)

#         # build your response and set cookie
#         if access is not None:
#             response = Response({"access": access, "refresh": refresh, "email": email}, status=200)
#             response.set_cookie('token', access, httponly=True,samesite='None',secure=True)
#             response.set_cookie('refresh', refresh, httponly=True,samesite='None',secure=True)
#             response.set_cookie('email', email,httponly=True,samesite='None',secure=True)
#             return response

#         return Response({"Error": "Something went wrong"}, status=400)
        
   
#         # return super().finalize_response(request, response, *args, **kwargs)

# class CookieTokenRefreshView(TokenRefreshView):
#     def finalize_response(self, request, response, *args, **kwargs):
#         if response.data.get('refresh'):
#             cookie_max_age = 3600 * 24 * 14 # 14 days
#             response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True  ,samesite='None',secure=True)
#             del response.data['refresh']
#         return super().finalize_response(request, response, *args, **kwargs)
#     serializer_class = CookieTokenRefreshSerializer


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
    
class UserIsOwnerimageOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user.id    

class SignUp(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    


# class Profile(RetrieveAPIView):
#     serializer_class = UserProfileSerializer
#     queryset = User.objects.all()
#     lookup_field = 'username'

# 'use for profile'
class Profile(RetrieveAPIView):
    # permission_classes=(IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    
    
    
class EditProfile(RetrieveUpdateAPIView) :
    queryset = User.objects.all()
    lookup_field = 'username'

    serializer_class = UserEditSerializer
    
    permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
        
        
class Mypost(ListAPIView):
    lookup_field = 'username'
    serializer_class = PostListSerializer
    permission_classes=(IsAuthenticated,)
    queryset = MyPost.objects.all()
    def get_queryset(self):
        qs=super().get_queryset()
        
        return qs.filter(author=self.request.user)


class PostByUser(ListAPIView):
    lookup_field = 'username'
    serializer_class = PostListSerializer
    permission_classes=(IsAuthenticated,)
    queryset = MyPost.objects.all()
    def get_queryset(self,*args, **kwargs):
        qs=super().get_queryset()
        
        return qs.filter(author__username=self.kwargs['username'])        
        
        
        
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
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            
        })


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

class MyProfile(RetrieveUpdateAPIView):
    lookup_field = 'username'
    permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    def get_queryset(self):
        
        qs=super().get_queryset()
        return qs.filter(username=self.request.user)
    
    def get_serializer_class(self):
            if self.request.method=='GET':
                return UserProfileSerializer

            else:
                return UserEditSerializer
        
        
class logout(APIView):
    
    def post(self,request):
        
       response = Response()
    

       response.delete_cookie('refresh')
       response.data={"masage":"yesss"}
       return response
   
   
   
# class fallow(CreateAPIView):
#     serializer_class = FallowSerializer
#     permission_classes=(IsAuthenticated,)
    

    
#     def perform_create(self,serializer,*args, **kwargs):
#         serializer.save(from_user=self.request.user,to_user=kwargs['pk'])
        
        
#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         return Response({
#         'status': 200,
#         })




class FollowingView(ListCreateAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = [IsAuthenticated]