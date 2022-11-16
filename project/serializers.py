from .models import *
from login.models import *
from login.serializers import *
from rest_framework import serializers
from rest_framework.response import Response






class CommentSerializer(serializers.ModelSerializer):
    commenter=UserProfileSerializer(read_only=True)
    class Meta:
        
        model=Comment
        fields=('body','commenter','post','id',)
        read_only_fields = ('commenter','post','id',)
        
    def create(self, validated_data):
        comment=Comment.objects.create(
            body=validated_data['body'],
            post_id=self.context['pk'],
            commenter=self.context['request'].user
        )
        comment.save()
        return comment

         

    
class PostSerializer(serializers.ModelSerializer):
    author=UserProfileSerializer(read_only=True)
    comment=CommentSerializer(many=True,read_only=True)
    youliked=serializers.SerializerMethodField()
    myimage=serializers.SerializerMethodField()
    
    
    def get_youliked(self,obj):
         try: 
            MyPost.objects.get(user_likes=self.context['request'].user,id=obj.id)
            
            return True
         except MyPost.DoesNotExist:
            return False
        
    def get_myimage(self, obj):
        try:
            return self.context["request"].build_absolute_uri("/").strip("/")+str(obj.image.url)
        except Exception as E:
            print(E)
            return str("")
    
    
    class Meta:
        
        model= MyPost
        
        fields=('title','content','user_likes','author','comment','image','myimage','created_date','id','youliked')
        read_only_fields = ('last_login','posts','created_date','user_likes','youliked')
        extra_kwargs = {
            "username": {
                "validators": [],
            },
            "email": {
                "validators": [],
                },
            "bio": {
                "validators": [],
                },
            "image":{
                "validators": [],
                },
            "password":{
                "validators": [],
                }
        }  
    
    def create(self, validated_data):
        post=MyPost.objects.create(
            title=validated_data['title'],
            content=validated_data['content'],
            image=validated_data['image'],
            author=self.context['request'].user
        )   
        if post:      
            post.save()
            return post
        else:
            return Response({"فیلدها اوکی نیست"})

