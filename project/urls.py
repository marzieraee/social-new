from django.urls import path
from rest_framework.routers import SimpleRouter
# from .polls import views
from django.conf import settings
from django.conf.urls.static import static
from . import views





urlpatterns = [
          path('register/verifycod/', views.VerifyEmail.as_view(), name='verifyemail'),

        path('', views.Home.as_view(), name='postlistapi'),
        path('register/', views.SignUp.as_view(), name='register'),
        path('profile/<str:username>', views.ShowEditDelProfile.as_view(), name='profile'),
#         path('editprofile/<str:username>', views.EditProfile.as_view(), name='profile'),
        path('post/<int:pk>', views.ShowEditDelPost.as_view(), name='postsingle'),
#         # path('token/',views.CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
#         # path('token/refresh/',views.CookieTokenRefreshView.as_view(), name='token_refresh'),
#         # path('picpro/<str:user__username>', views.ShowPic.as_view(), name='profile'),
#         path('changepassword/<str:username>', views.ChangePass.as_view(), name='changepass'),
        path('postcreate/', views.CreatePost.as_view(), name='postcomment'),
#         path('postsingle/<int:pk>', views.SinglePost.as_view(), name='postsingle'),
#         path('createcomment/<int:pk>', views.CreateComment.as_view(), name='createcomment'),
#         path('myprofile/<str:username>', views.MyProfile.as_view(), name='changepass'),
#         path('mypost/<str:username>', views.Mypost.as_view(), name='changepass'),
        path('postuser/<str:username>', views.PostByUser.as_view(), name='changepass'),
#         path('fallow/', views.FollowingView.as_view(), name='changepass'),
        
        path('follow/<int:pk>/', views.FollowView.as_view({'post': 'follow'})),
        path('unfollow/<int:pk>/', views.FollowView.as_view({'post': 'unfollow'})),
        path('follower/<int:pk>/', views.FollowView.as_view({'get': 'follower'})),


        
# #     path('postcreate/', views.PostComment.as_view(), name='postcomment'),
#     # path('commentretrieve/<int:pk>', views.CommentRetriveApi.as_view(), name='commentretriveapi'),
# #     path('register/', views.SignUp.as_view(), name='register'),
# #     path('profile/<int:pk>', views.Profile.as_view(), name='profile'),
# #     path('changepassword/<int:pk>', views.ChangePass.as_view(), name='changepass'),
# #     path('createcomment/<int:pk>', views.CreateComment.as_view(), name='createcomment'),
# #     path('like/<str:username>', views.Like.as_view(), name='like'),
    
    
    
    
]