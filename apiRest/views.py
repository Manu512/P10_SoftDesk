""" views.pu"""
from rest_framework import viewsets, permissions, status
from .models import Users, Project, Issue, Comment, Contributor
from .serializers import (
    UserSerializer, ProjectSerializer, CommentSerializer,
    IssueSerializer, ContributorsSerializer
)
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly, IsProjetContributor


# Create your views here.
class UserSignup(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created.
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

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
    serializer_class = ContributorsSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsProjetContributor]

    def get_queryset(self):
        """
        Methode qui liste les utilisateurs par rapport a un projet.
        :return: QuerySet Contributeurs a un projet
        """
        return Contributor.objects.filter(project=self.kwargs['project_pk'])

    def list(self, request, *args, **kwargs):
        """
        Methode qui permet d'afficher les contributeurs du projet
        """
        response = Contributor.objects.filter(project_id=self.kwargs['project_pk'])
        serializer = ContributorsSerializer(response, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Methode qui sauvegarde le contributeur en lien avec le projet
        """
        serializer.save(project_id=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        """
        Methode qui permet de créer un contributeur sans le besoin de specifier le projet.
        """

        informations = request.data.copy()  # Copie du queryset qui le rend "mutable"
        informations.__setitem__('project', self.kwargs['project_pk'])  # insertion de la valeur project (récupérer
        # via l'objet request).
        serializer = self.get_serializer(data=informations)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authentificated users in the project to view, create or edit issues
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsProjetContributor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if self.check_assignee(self.request.data['assignee']):
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            error_messages = 'Assignation non autorisé, utilisateur ne contribue pas au projet'
            return Response(data=error_messages, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if self.check_assignee(self.request.data['assignee_username']):
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            error_messages = 'Assignation non autorisé, utilisateur ne contribue pas au projet'
            return Response(data=error_messages, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user, project_id=self.kwargs['project_pk'])

    def check_assignee(self, assignee_username):
        """
        Methode permettant de contrôler que la personne assignée est bien contributrice au projet.
        :param assignee_username: username de la personne assigné au problème du projet.
        :return: True si la personne est bien contributrice du projet.
        """
        project = Project.objects.get(pk=self.kwargs['project_pk'])

        try:
            project.contributors.get(user__username=assignee_username)
            return True
        except Contributor.DoesNotExist:
            return False


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authentificated users in the project to view, create or edit issues
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsProjetContributor]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user, issue_id=self.kwargs['issue_pk'])


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view / Edit / Delete / Create Project
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsProjetContributor]

    def get_queryset(self):
        return Project.objects.filter(contributors__user_id=self.request.user.id)

    def perform_create(self, serializer):
        creator = self.request.user
        serializer.save(author_user=creator)
        self.add_author_to_contributor(creator)

    def add_author_to_contributor(self, creator):
        """
        Methode qui ajoute automatiquement le créateur du project en tant que contributeur
        """
        Contributor(user_id=creator.id, permission='all',
                    role='creator', project=Project.objects.latest('id')).save()
