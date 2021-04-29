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
    BACK_END = 'back-end'
    FRONT_END = 'front-end'
    IOS = 'IOS'
    ANDROID = 'Android'
    projects_type = [(BACK_END, "back-end"), (FRONT_END, "front-end"), (IOS, "iOS"), (ANDROID, "Android")]
    type = models.CharField(max_length=20, choices=projects_type, blank=False)


class Contributors(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    permission = models.Choices
    role = models.CharField(max_length=150, blank=True)


class Issues(Author, Title, Create_time):
    LOW = 'BASSE'
    MEDIUM = 'MOYENNE'
    HIGH = 'HAUTE'
    issues_priority = [(LOW, 'Basse'), (MEDIUM, 'Moyenne'), (HIGH, 'Haute')]
    BUG = 'BUG'
    AMELIORATION = 'AMELIORATION'
    TACHE = 'TACHE'
    issues_tag = [(BUG, 'BUG'), (AMELIORATION, 'AMÉLIORATION'), (TACHE, 'TÂCHE')]

    tag = models.CharField(max_length=15, choices=issues_tag, default=TACHE)
    priority = models.CharField(max_length=10, choices=issues_priority, default=MEDIUM)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    issues_status = [('af', 'À faire'), ('ec', 'En cours'), ('T', 'Terminé')]
    status = models.CharField(max_length=20, choices=issues_status, default='af')
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                         related_name="assignee_id_user")


class Comments(Author, Title, Create_time):
    title = None
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
