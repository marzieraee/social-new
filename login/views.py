from os import access
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from login.serializers import *
from login.utils import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.views import APIView



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['name'] = user.username
        # ...
        
       
        
        return token
    
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
        email = serializer.validated_data.get("email", None)

        # build your response and set cookie
        if access is not None:
            response = Response({"token": access}, status=200)
            response.set_cookie('refresh', refresh, httponly=True,samesite='None',secure=True)
            return response

        return Response({"Error": "Something went wrong"}, status=400)



class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            print(attrs['refresh'])
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

    # def finalize_response(self, request, response, *args, **kwargs):
    #     if response.data.get('refresh'):
    #         cookie_max_age = 3600 * 24 * 14 # 14 days
    #         response.set_cookie('refresh', response.data['refresh'], max_age=cookie_max_age, httponly=True , samesite='None')
    #         del response.data['refresh']





class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer


class logout(APIView):
    
    def post(self,request):
        
       response = Response()
    

       response.delete_cookie('refresh')
       response.data={"masage":"yesss"}
       return response
   