from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings


# Create your models here.
class Users(AbstractUser):
    pass


class Create_time(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Author(models.Model):
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Title(models.Model):
    title = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=150, blank=True)

    class Meta:
        abstract = True


class Projects(Author, Title):
    type = models.CharField(max_length=150, blank=True)


class Contributors(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    permission = models.Choices
    role = models.CharField(max_length=150, blank=True)


class Issues(Author, Title, Create_time):
    tag = models.CharField(max_length=150, blank=True)
    priority = models.CharField(max_length=150, blank=True)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    status =  models.CharField(max_length=150, blank=True)
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignee_id_user")


class Comments(Author, Title, Create_time):
    title = None
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
