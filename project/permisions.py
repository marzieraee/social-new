from rest_framework import status,permissions
from rest_framework.permissions import IsAuthenticated,AllowAny



class UserIsOwnerOrReadOnly(permissions.BasePermission):
    '''when a user as user ,get checked'''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.id == request.user.id
        return True
    
class UserIsOwnerPostOrReadOnly(permissions.BasePermission):
    '''for who comment on post it get them access'''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.author == request.user
        return True
    
class UserIsOwnerCommentOrReadOnly(permissions.BasePermission):
    '''for who comments on post, it get them access'''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.commenter.username == request.user and obj.post.author == request.user
        return True
    
    

