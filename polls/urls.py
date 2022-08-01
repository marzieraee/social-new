from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
         path('', views.PostList.as_view(), name='postlistapi'),
        path('register/', views.SignUp.as_view(), name='register'),
        path('profile/<str:username>', views.Profile.as_view(), name='profile'),
        path('editprofile/<str:username>', views.EditProfile.as_view(), name='profile'),
        path('editpost/<int:pk>', views.EditPost.as_view(), name='postsingle'),

        path('changepassword/<str:username>', views.ChangePass.as_view(), name='changepass'),
        path('postcreate/', views.CreatPost.as_view(), name='postcomment'),
        path('postsingle/<int:pk>', views.SinglePost.as_view(), name='postsingle'),
        path('setprofile/<str:username>', views.SetImageProfile.as_view(), name='changepass'),
        
        
#     path('postcreate/', views.PostComment.as_view(), name='postcomment'),
#     # path('commentretrieve/<int:pk>', views.CommentRetriveApi.as_view(), name='commentretriveapi'),
#     path('register/', views.SignUp.as_view(), name='register'),
#     path('profile/<int:pk>', views.Profile.as_view(), name='profile'),
#     path('changepassword/<int:pk>', views.ChangePass.as_view(), name='changepass'),
#     path('createcomment/<int:pk>', views.CreateComment.as_view(), name='createcomment'),
#     path('like/<str:username>', views.Like.as_view(), name='like'),
#     path('logout/', views.Logout.as_view()),
    
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)