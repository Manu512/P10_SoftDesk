""" serializers.py """
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from . import models


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            validators=[UniqueValidator(models.Users.objects.all())]
    )

    class Meta:
        model = models.Users
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Methode qui permet de hash le mot de passe dans la base de données. Autrement il est en clair.
        """
        validated_data["password"] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def validate(self, attrs):
        """
        Methode de validation pour forcer le passage par le validator de MDP de Django
        Cela permet de respecté les préconisations OWASP via le paramétrage Django.
        :param attrs: données a valider
        :return: les paramètres validés
        """
        user = models.Users(**attrs)

        password = attrs.get('password')

        errors = dict()
        try:
            validators.validate_password(password=password, user=user)

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


class IssueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author_user = serializers.ReadOnlyField(source='author_user.username')
    assignee = serializers.SlugRelatedField(
            queryset=models.Users.objects.all(),
            slug_field='username',
            default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Issue
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'status', 'author_user', 'assignee', 'created_time']
        read_only_fields = ['author_user', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author_user.username')

    class Meta:
        model = models.Comment
        fields = ['id', 'description', 'author',
                  'issue_id', 'created_time']


class ContributorsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
            queryset=models.Users.objects.all(), slug_field='username')

    class Meta:
        validators = [UniqueTogetherValidator(
                queryset=models.Contributor.objects.all(), fields=['project', 'user']
        )]
        model = models.Contributor
        fields = ['id', 'project', 'user', 'permission', 'role']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    issues = serializers.HyperlinkedIdentityField(view_name='issues-list', lookup_field='pk',
                                                  lookup_url_kwarg='project_pk')
    contributors = serializers.HyperlinkedIdentityField(view_name='users-list', lookup_field='pk',
                                                        lookup_url_kwarg='project_pk')

    class Meta:
        model = models.Project
        fields = ['url', 'title', 'type', 'description', 'issues', 'contributors']
        # exclude = ['project_id' ]
