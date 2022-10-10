from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)


from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('api/token/',MyTokenObtainPairView.as_view()),
    path('api/token/refresh',CookieTokenRefreshView.as_view()),
    path('logout/', logout.as_view()),
    path('register/verifycod/', VerifyEmail.as_view(), name='verifyemail'),

    path('register/',SignUp.as_view(), name='register'),
    path('profile/<str:username>', ShowEditDelProfile.as_view(), name='profile'),
#         path('changepassword/<str:username>', views.ChangePass.as_view(), name='changepass'),
    path('follow/<str:username>/',FollowView.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/',FollowView.as_view({'post': 'unfollow'})),
    path('profilefollow/<str:username>/',FollowView.as_view({'get': 'retrieve'})),
    path('follwer/<str:username>/',FollowView.as_view({'get': 'follower'})),


]