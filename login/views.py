
# Create your views here.
import jwt
from .models import *
from login.utils import *
from .serializers import *
from login.serializers import *
from project.permisions import *
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView



    



    
class MyTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    and here we try to set refresh tiken in the cookie
    """
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)
        if access is not None:
            response = Response({"token": access}, status=200)
            response.set_cookie('refresh', refresh, httponly=True,samesite='None',secure=True)
            return response

        return Response({"Error": "Something went wrong"}, status=400)



class CookieTokenRefreshView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = CookieTokenRefreshSerializer


class logout(APIView):
    '''log out means clear refresh token from cookie'''
    def post(self,request):
       response = Response()
       response.delete_cookie('refresh')
       response.data={"masage":"yesss"}
       return response
   
   
class SignUp(CreateAPIView):
    '''from serilizer takes username and email and password then make a user and send 
    email them to verify their email '''
    serializer_class = UserProfileSerializer
    



class VerifyEmail(APIView):
    
    '''when user requests get, is_active feature get true , this is considered ,if token got expired and
    or invalid token'''
    serializer_class=UserProfileSerializer
    def get(self,request,*args, **kwargs):
        if request.method=='GET':
            token = request.GET.get('token')

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
                user = User.objects.filter(id=payload['user_id']).first()
                
                if user.is_active:
                    return Response({'detail':'قبلا تایید شد لاگین کنین'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.is_active = True
                    user.save()
                    return Response({'detail':'خوش آمدی'}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
            
                return Response({'detail':'توکن شمامنقضی شد'},status=status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.DecodeError:
                return Response({'detail':'توکن درست نیست'}, status=status.HTTP_400_BAD_REQUEST)
            

    
    
    
class ShowEditDelProfile(RetrieveUpdateDestroyAPIView) :
    '''the name of class shows every things'''
    queryset = User.objects.all()
    lookup_field = 'username'

    serializer_class = UserProfileSerializer
    
    permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
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
    
    
class FollowView(viewsets.ViewSet):
    '''in this class "follow/user" return following or unfollowing  the user,and "following" and "follower"/user
    return the user followings and followers'''
    lookup_field = 'username'
    permission_classes=[IsAuthenticated,]
    def follow(self, request, username):
        to_user = CustomUser.objects.get(username=username)
        try:
            user=ProfileFallow.objects.get(from_user=request.user,to_user=to_user)
            user.delete()
            return Response({'detail': 'now you are not following'}, status=status.HTTP_200_OK)
            
        except:
            
            ProfileFallow.objects.create(from_user=request.user,to_user=to_user)
            return Response({'detail': 'now you are following'}, status=status.HTTP_200_OK)

    
    
    def following(self, request, username):
        try:
            data=ProfileFallow.objects.filter(from_user__username=username)
            listfollowers=FollowingSerializer(data,many=True)
            return Response(listfollowers.data)
        except ProfileFallow.DoesNotExist:
                return Response({'detail': 'one thing is wrong'})
      
    
    def follower(self, request, username):
        try:
            data=ProfileFallow.objects.filter(to_user__username=username)
            listfollowers=FollowerSerializer(data,many=True)
            return Response(listfollowers.data)
        except ProfileFallow.DoesNotExist:
                return Response({'detail': 'one thing is wrong'})