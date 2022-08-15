from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        
         path('', views.PostList.as_view(), name='postlistapi'),
        path('register/', views.SignUp.as_view(), name='register'),
        path('profile/<str:username>', views.Profile.as_view(), name='profile'),
        path('editprofile/<int:pk>', views.EditProfile.as_view(), name='profile'),
        path('editpost/<int:pk>', views.EditPost.as_view(), name='postsingle'),
        path('token/',views.CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/',views.CookieTokenRefreshView.as_view(), name='token_refresh'),
        # path('picpro/<str:user__username>', views.ShowPic.as_view(), name='profile'),
        path('changepassword/<str:username>', views.ChangePass.as_view(), name='changepass'),
        path('postcreate/', views.CreatPost.as_view(), name='postcomment'),
        path('postsingle/<int:pk>', views.SinglePost.as_view(), name='postsingle'),
        path('setprofile/<int:pk>', views.SetImageProfile.as_view(), name='changepass'),
        path('createcomment/<int:pk>', views.CreateComment.as_view(), name='createcomment'),
        path('myprofile/<int:pk>', views.MyProfile.as_view(), name='changepass'),
        # path('logout/', views.LogoutView.as_view()),

        
#     path('postcreate/', views.PostComment.as_view(), name='postcomment'),
    # path('commentretrieve/<int:pk>', views.CommentRetriveApi.as_view(), name='commentretriveapi'),
#     path('register/', views.SignUp.as_view(), name='register'),
#     path('profile/<int:pk>', views.Profile.as_view(), name='profile'),
#     path('changepassword/<int:pk>', views.ChangePass.as_view(), name='changepass'),
#     path('createcomment/<int:pk>', views.CreateComment.as_view(), name='createcomment'),
#     path('like/<str:username>', views.Like.as_view(), name='like'),
    
    
    
    
]