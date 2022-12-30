from . import views
from django.urls import include, path
from rest_framework.routers import SimpleRouter


router=SimpleRouter()
router.register('',views.PostView,basename='posts')
commentrouter=SimpleRouter()
commentrouter.register('comment',views.CommentView)


urlpatterns = [

        path('postuser/<str:username>', views.PostByUser.as_view(), name='changepass'),
    path('<int:pk>/', include(commentrouter.urls), name='createcomment'),      
    
]+router.urls