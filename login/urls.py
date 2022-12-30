from .views import *
from django.urls import path





urlpatterns = [
    
    path('api/token/',MyTokenObtainPairView.as_view()),
    path('api/token/refresh',CookieTokenRefreshView.as_view()),
    path('logout/', logout.as_view()),
    path('register/verifycod/', VerifyEmail.as_view(), name='verifyemail'),
    path('register/',SignUp.as_view(), name='register'),
    path('profile/<str:username>', ShowEditDelProfile.as_view(), name='profile'),
    path('follow/<str:username>/',FollowView.as_view({'post': 'follow'})),
    path('following/<str:username>/',FollowView.as_view({'get': 'following'})),
    path('follower/<str:username>/',FollowView.as_view({'get': 'follower'})),


]