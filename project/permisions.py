from rest_framework import status,permissions
from rest_framework.permissions import IsAuthenticated,AllowAny



class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.id == request.user.id
        return True
    
class UserIsOwnerPostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.author == request.user
        return True
    
class UserIsOwnerCommentOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.commenter.username == request.user and obj.post.author == request.user
        return True
    
    

