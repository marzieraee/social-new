
# Create your views here.
from rest_framework.response import Response
from login.serializers import *
from login.utils import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import *
from project.permisions import *
from .models import *
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView, CreateAPIView,RetrieveUpdateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status, viewsets
from . import utils







    
class MyTokenObtainPairView(TokenObtainPairView):
    
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        # you need to instantiate the serializer with the request data
        serializer = self.get_serializer(data=request.data)
        # you must call .is_valid() before accessing validated_data
        serializer.is_valid(raise_exception=True)  

        # get access and refresh tokens to do what you like with
        access = serializer.validated_data.get("access", None)
        refresh = serializer.validated_data.get("refresh", None)

        # build your response and set cookie
        if access is not None:
            response = Response({"token": access}, status=200)
            response.set_cookie('refresh', refresh, httponly=True,samesite='None',secure=True)
            return response

        return Response({"Error": "Something went wrong"}, status=400)



class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer


class logout(APIView):
    
    def post(self,request):
        
       response = Response()
    

       response.delete_cookie('refresh')
       response.data={"masage":"yesss"}
       return response
   
   
class SignUp(CreateAPIView):
    
    
    serializer_class = CustomRegisterSerializer
    



class VerifyEmail(APIView):
    
    serializer_class=CustomRegisterSerializer
    def patch(self,request,*args, **kwargs):
        try:
            user = User.objects.get(username=request.PATCH.get('username'))
        except User.DoesNotExist:
            user = None
                              
        if user.cod == request.PATCH.get('cod'):
            user.is_active=True
            user.save()
            profile=ProfileFallow.objects.create(myprofile=user)
            profile.save()
        else:
            return Response({'کد درست نیست'},status=400)
    
        return Response({'خوش آمدی'},status=200)
    
    
    
    
    
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
    
    
class FollowView(viewsets.ViewSet):
    lookup_field = 'username'
    permission_classes=[IsAuthenticated,]
    def follow(self, request, username):
        to_user = CustomUser.objects.get(username=username)
        try:
            user=ProfileFallow.objects.get(from_user=request.user,to_user=to_user)
            user.delete()
            return Response({'message': 'now you are not following'}, status=status.HTTP_200_OK)
            
        except:
            
            ProfileFallow.objects.create(from_user=request.user,to_user=to_user)
            return Response({'message': 'now you are following'}, status=status.HTTP_200_OK)

    
    
    def following(self, request, username):
        try:
            data=ProfileFallow.objects.filter(from_user__username=username)
            
            print (data)
            listfollowers=FollowingSerializer(data,many=True)
            return Response(listfollowers.data)
        except ProfileFallow.DoesNotExist:
                return Response({'message': 'one thing is wrong'})
      
    
    def follower(self, request, username):
        try:
            data=ProfileFallow.objects.filter(to_user__username=username)
            
            print (data)
            listfollowers=FollowerSerializer(data,many=True)
            return Response(listfollowers.data)
        except ProfileFallow.DoesNotExist:
                return Response({'message': 'one thing is wrong'})