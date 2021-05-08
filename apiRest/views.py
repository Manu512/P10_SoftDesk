""" views.pu"""
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, permissions, status
from .models import Users, Project, Issue, Comment, Contributor
from .serializers import UserSerializer, ProjectSerializer, CommentSerializer, IssueSerializer, ContributorsSerializer
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser


# Create your views here.
class UserSignup(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created.
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Methode de creation d'utilisateurs.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authentificated users in the project to be viewed or edited.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorsSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Methode qui liste les utilisateurs par rapport a un projet.
        :return: QuerySet Contributeurs a un projet
        """
        return Contributor.objects.filter(project=self.kwargs['project_pk'])

    def list(self, request, *args, **kwargs):
        """
        Methode qui permet l'affichage des contributeurs du projet
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = Contributor.objects.filter(project_id=self.kwargs['project_pk'])
        serializer = ContributorsSerializer(response, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_pk'])



class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authentificated users in the project to view, create or edit issues
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def list(self, request, *args, **kwargs):
        response = self.get_queryset()
        serializer = IssueSerializer(response, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user, project_id=self.kwargs['project_pk'])


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authentificated users in the project to view, create or edit issues
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user, issue_id=self.kwargs['issue_pk'])


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view / Edit / Delete / Create Project
    """
    authentication_classes = [JWTAuthentication]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(author_user=self.request.user.pk) | Project.objects.filter(
            contributor=self.request.user.pk)

    def perform_create(self, serializer):
        creator = self.request.user
        serializer.save(author_user=creator)
        self.add_author_to_contributor(creator)

    def list(self, request, *args, **kwargs):
        """
        Methode qui permet l'affichage des projets selon a condition que l'ont soit l'auteur/contributeur au projet.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = self.get_queryset()
        serializer = ProjectSerializer(response, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def add_author_to_contributor(self, creator):
        """
        Methode qui ajoute automatiquement le créateur du project en tant que contributeur
        """
        Contributor(user_id=creator.id, permission='createur',
                    role='createur', project=Project.objects.latest('id')).save()
