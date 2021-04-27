from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def signup(request):
    return  HttpResponse("Signup")

def login(request):
    return HttpResponse("Login")

def project(request, project_id=None, user_id=None, issue_id=None, comment_id=None):
    return HttpResponse(str(request))