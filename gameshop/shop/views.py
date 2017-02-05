from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.template import RequestContext

# Create your views here.

def index(request):
	response = TemplateResponse(request, 'index.html', {})
	response.render()
	return response

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
	else:
		print('Invalid username or password!')

def logout(request):
	logout(request)
