""" Gestion des Permissions """
from rest_framework import permissions

from apiRest.models import Contributor, Project


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the Project.
        return obj.author_user == request.user


class IsProjetContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of an object to view it.
    """

    def has_permission(self, request, view):
        """
        si l'utilisateur est dans la liste des contributeurs au projet => True
        Autorisation accordé
        """
        if 'project_pk' in view.kwargs:
            data_project = view.kwargs['project_pk']
        elif 'pk' in view.kwargs:
            data_project = view.kwargs['pk']
        else:
            return True
        try:
            project = Project.objects.get(pk=data_project)
        except Project.DoesNotExist:
            return False

        try:
            project.contributors.get(user__username=request.user)
            return True
        except Contributor.DoesNotExist:
            return False
