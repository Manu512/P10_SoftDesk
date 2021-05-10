""" urls.py """
from rest_framework_nested import routers
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

route = routers.SimpleRouter()
route.register(r'projects', views.ProjectViewSet, basename='project')

project_route = routers.NestedSimpleRouter(route, r'projects', lookup='project')
project_route.register(r'users', views.ContributorViewSet, basename='users')
project_route.register(r'issues', views.IssueViewSet, basename='issues')
comments_route = routers.NestedSimpleRouter(project_route, r'issues', lookup='issue')
comments_route.register(r'comments', views.CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(route.urls), name="api"),
    path('', include(project_route.urls), name="project"),
    path('', include(comments_route.urls), name="comment"),
    path('admin/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', views.UserSignup.as_view({'post': 'create'}), name='create_user'),
]
