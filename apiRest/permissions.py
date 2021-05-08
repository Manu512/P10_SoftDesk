""" Gestion des Permissions """
from rest_framework import permissions

from apiRest.models import Contributor


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        user = request.user.id

        if request.method in permissions.SAFE_METHODS:
            authorised_user = Contributor.objects.filter(project_id=obj.id, user_id=user)
            if authorised_user:
                return True
            else:
                return False

        # Write permissions are only allowed to the author of the Project.
        return obj.author_user == request.user
