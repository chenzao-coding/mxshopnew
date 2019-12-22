# FileName: permissions
# Author: Tunny
# @time: 2019-12-22 20:05
# Desc: 
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    是否是自己
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
