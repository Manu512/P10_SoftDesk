from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('projects/', views.project, name='projets'),
    path('projects/<int:project_id>/', views.project, name='project_details'),
    path('projects/<int:project_id>/users/', views.project, name='project_user'),
    path('projects/<int:project_id>/users/<int:user_id>/', views.project, name='project_user_delete'),
    path('projects/<int:project_id>/issues/', views.project, name='project_issue'),
    path('projects/<int:project_id>/issues/<int:issue_id>', views.project, name='project_issue'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', views.project, name='project_comments'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>', views.project, name='project_comment'),
]
