""" serializers.py """

from rest_framework import serializers

from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Users


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Projects


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Issues


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Comments
