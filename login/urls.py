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
    path('api/token/refresh',TokenRefreshSlidingView.as_view()),
]