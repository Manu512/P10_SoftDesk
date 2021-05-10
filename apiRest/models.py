""" model.py contient les modèles """
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings


# Create your models here.
class Users(AbstractUser):
    """
    Objet Users
    """
    pass


class CreateTime(models.Model):
    """
    Classe abstraite pour horodater les entrées (DRY Method)
    """
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Project(models.Model):
    """
    Object Projet qui permet de définir un projet.
    """
    BACK_END = 'back-end'
    FRONT_END = 'front-end'
    IOS = 'ios'
    ANDROID = 'android'
    title = models.CharField(max_length=150, blank=False, null=False)
    description = models.CharField(max_length=150, blank=False, null=False)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    projects_type = [(BACK_END, "back-end"), (FRONT_END, "front-end"), (IOS, "iOS"), (ANDROID, "Android")]
    type = models.CharField(max_length=20, choices=projects_type, blank=False, null=False)


class Contributor(models.Model):
    """
    Object Contributor qui permet de définir le niveau de permission et le role de l'utilisateur sur un projet.
    """
    # TODO : La liste des permissions est a revoir
    permissions_list = [
            ("limited", "Contributeur"),
            ("all", "Auteur"),
    ]

    role_list = [
            ("author", "Auteur"),
            ("responsable", "Responsable"),
            ("creator", "Créateur"),
    ]

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='contributor', on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, related_name="contributors", on_delete=models.CASCADE)
    permission = models.CharField(max_length=20, choices=permissions_list, blank=False, null=False, default='limited')
    role = models.CharField(max_length=150, choices=role_list, blank=True, null=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'], name='unique_user'),  # Pour éviter les users en double
        ]


class Issue(CreateTime):
    """
    Object Issue qui permet de définir un problème sur un projet.
    """
    LOW = 'FAIBLE'
    MEDIUM = 'MOYENNE'
    HIGH = 'ELEVEE'
    issue_priority = [(LOW, 'FAIBLE'), (MEDIUM, 'MOYENNE'), (HIGH, 'ELEVEE')]
    BUG = 'BUG'
    AMELIORATION = 'AMELIORATION'
    TACHE = 'TACHE'
    issues_tag = [(BUG, 'BUG'), (AMELIORATION, 'AMÉLIORATION'), (TACHE, 'TÂCHE')]
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='issue', on_delete=models.CASCADE)
    tag = models.CharField(max_length=15, choices=issues_tag, default=TACHE, blank=False, null=False)
    priority = models.CharField(max_length=10, choices=issue_priority, default=MEDIUM, blank=False, null=False)
    project = models.ForeignKey(to=Project, related_name='issue', on_delete=models.CASCADE)
    issue_status = [('a faire', 'À faire'), ('en cours', 'En cours'), ('termine', 'Terminé')]
    status = models.CharField(max_length=20, choices=issue_status, default='af', blank=False, null=False)
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_issue', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False, null=False)
    description = models.CharField(max_length=150, blank=False, null=False)


class Comment(CreateTime):
    """
    Object Commentaire qui permet lier un commentaire a un problème d'un projet.
    """
    description = models.CharField(max_length=150, blank=False, null=False)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='comment', on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, related_name='comment', on_delete=models.CASCADE)
