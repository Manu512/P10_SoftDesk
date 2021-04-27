from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
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
