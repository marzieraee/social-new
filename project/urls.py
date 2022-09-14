from django.urls import path
from rest_framework.routers import SimpleRouter
# from .polls import views
from django.conf import settings
from django.conf.urls.static import static
from . import views





urlpatterns = [

        path('', views.Home.as_view(), name='postlistapi'),
        path('post/<int:pk>', views.ShowEditDelPost.as_view(), name='postsingle'),
#         path('changepassword/<str:username>', views.ChangePass.as_view(), name='changepass'),
        path('postcreate/', views.CreatePost.as_view(), name='postcomment'),
        path('postuser/<str:username>', views.PostByUser.as_view(), name='changepass'),
        path('explore/', views.Explore.as_view(), name='changepass'),
# #     path('changepassword/<int:pk>', views.ChangePass.as_view(), name='changepass'),
    path('createcomment/<int:pk>', views.CreateComment.as_view(), name='createcomment'),
    path('deletecomment/<int:pk>', views.DeleteComment.as_view(), name='deletecomment'),
# #     path('like/<str:username>', views.Like.as_view(), name='like'),
    
    
    
    
]