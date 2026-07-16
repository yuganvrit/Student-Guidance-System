from rest_framework import permissions
class IsMentor(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        return request.user.role == 'student'
    
        
    def has_object_permission(self, request, view, obj):
        print(type(obj))
        # Instance must have an attribute named `owner`.
        return obj.mentor == request.user