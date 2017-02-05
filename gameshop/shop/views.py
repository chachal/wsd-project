from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.template.response import TemplateResponse
from django.template import RequestContext
from shop.models import UserProfile, Games, Purchased, Scores

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

"""Tarkistetaan onko admin"""
def list_users(request):
	order_by = request.GET.get('order_by', 'user')
	users = UserProfile.objects.all().order_by(order_by)
	response = TemplateResponse(request, 'admin_userlist.html', {'users': users})
	response.render()
	return reponse

def list_games(request):
	order_by = request.GET.get('order_by', 'name')
	games = Games.objects.all().order_by(order_by)
	response = TemplateResponse(request, 'gamelist.html', {'games': games})
	response.render()
	return response

"""Tarkistetaan onko kirjautunut"""
def list_purchased(request, userID="1"):
	order_by = request.GET.get('order_by', 'game')
	purchased = Purchased.objects.filter(owner__id=userID).order_by(order_by)
	response = TemplateResponse(request, 'purchaselist.html', {'purchased': purchased})
	response.render()
	return response


def list_scores(request, gameID="1"):
	order_by = request.GET.get('order_by', 'score')
	scores = Scores.objects.filter(game__id=gameID).order_by(order_by)
	response = TemplateResponse(request, 'scores.html', {'scores': scores})
	response.render()
	return response
