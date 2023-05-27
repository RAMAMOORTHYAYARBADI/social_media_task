from rest_framework import permissions
from apps.user.models import *

class Is_SuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        groups = Profile.objects.filter(id = request.user.id).last()
        groupname = Role.objects.filter(id = groups).values_list("name",flat=True)
        return "User" not in groupname or "SuperAdmin" in groupname
    
class Is_User(permissions.BasePermission):
    def has_permission(self, request, view):
        groups = Profile.objects.filter(id = request.user.id).last()
        groupname = Role.objects.filter(id = groups.role_id).values_list("role_name",flat=True)
        return "User"  in groupname or "SuperAdmin" not in groupname

