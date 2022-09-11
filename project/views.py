import profile

from rest_framework.response import Response
from .serializers import *
from .permisions import *
from .models import *
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,CreateAPIView,RetrieveUpdateAPIView,ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status, viewsets






class SignUp(CreateAPIView):
    
    
    serializer_class = CustomRegisterSerializer
    




class VerifyEmail(APIView):
    
    serializer_class=CustomRegisterSerializer
    def patch(self,request,*args, **kwargs):
        try:
            user = User.objects.get(email=request.GET.get('email'))
        except User.DoesNotExist:
            user = None
                              
        if user.cod == request.GET.get('cod'):
            user.is_active=True
            user.save()
        else:
            return Response({'isnot mach'},status=400)
    
        return Response({'chek your email'},status=200)
    
    
    
    
    
class Profile(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    
    
    
    
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
    
    
    
    
    
class ShowEditDelPost(RetrieveUpdateDestroyAPIView) :
    queryset = User.objects.all()

    serializer_class = PostSerializer
    
    # permission_classes=(IsAuthenticated,UserIsOwnerOrReadOnly)
    def get_queryset(self):
        super().get_queryset()
        if self.request.method=='GET':
               queryset = MyPost.objects.all()
        else:
               queryset = MyPost.objects.filter(author=self.request.user)
 
        return queryset
    
    def get_permissions(self):
        
        if self.request.method in permissions.SAFE_METHODS:
             return (permissions.AllowAny(),)
        return (IsAuthenticated(), UserIsOwnerPostOrReadOnly(),)
    
    
    
class CreatePost(CreateAPIView):
    serializer_class=PostSerializer
    permission_classes=(IsAuthenticated,)
    



class PostByUser(ListAPIView):
    lookup_field='username'
    queryset = User.objects.all()

    serializer_class = PostSerializer
    def get_queryset(self):
        super().get_queryset()
        username=self.kwargs['username']
        
        queryset = MyPost.objects.filter(author__username=username)
 
        return queryset
     
     
class Home(ListAPIView):
    
    
    
    serializer_class = PostSerializer
    
    def get_queryset(self):
        
        own_profile = self.request.user.myprofile.first()
        myfollowing=own_profile.following.all()
        
        return MyPost.objects.filter(author__in=myfollowing)
    
    
class Explore(ListAPIView):
    
    

    serializer_class = PostSerializer
    
        
    MyPost.objects.all()
   
    

class FollowView(viewsets.ViewSet):
    queryset = ProfileFallow.objects.all()

    def follow(self, request, pk):
        own_profile = ProfileFallow.objects.get(myprofile=request.user)
        following_profile =CustomUser.objects.get(id=pk)
        own_profile.following.add(following_profile)        
        return Response({'message': 'now you are following'}, status=status.HTTP_200_OK)

    def unfollow(self, request, pk):
        own_profile = request.user.myprofile.first()
        following_profile = CustomUser.objects.get(id=pk)
        own_profile.following.remove(following_profile)
        return Response({'message': 'you are no longer following him'}, status=status.HTTP_200_OK)
    
    def follower(self, request,pk):
        user = CustomUser.objects.get(id=pk)
        count=ProfileFallow.objects.get(myprofile=user).following.count()
        print(count,'aaaaaaaaaaaaaaaaaaaaaaaaaaa')
        return Response({count},status=status.HTTP_200_OK)
        
        
        