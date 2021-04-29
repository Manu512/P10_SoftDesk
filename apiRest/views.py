""" views.pu"""

from django.http import HttpResponse
from rest_framework import permissions, viewsets

from .models import Users, Projects, Issues, Comments
from .serializers import UserSerializer, ProjectSerializer, CommentSerializer, IssueSerializer


# Create your views here.
def signup(request):
    return HttpResponse("Signup")


def login(request):
    """

    :param request:
    :return:
    """
    return HttpResponse("Login")


def project(request, project_id=None, user_id=None, issue_id=None, comment_id=None):
    return HttpResponse(str(request))


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Users.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view / Edit / Delete / Create Project
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
