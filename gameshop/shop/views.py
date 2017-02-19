from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.template.response import TemplateResponse
from django.template import RequestContext
from shop.models import UserProfile, Games, Purchased, Scores
from shop.forms import AddUserForm, LoginForm
from django.contrib.auth.models import User

# Create your views here.

def index(request):
	order_by = request.GET.get('order_by', 'released')
	games = Games.objects.all().order_by(order_by)[:16]
	response = TemplateResponse(request, 'index.html', {'games': games})
	response.render()
	return response

def mygames(request):
	order_by = request.GET.get('order_by', 'released')
	games = Games.objects.all().order_by(order_by)[:16]
	response = TemplateResponse(request, 'gamelist.html', {'games': games})
	response.render()
	return response

def shop(request):
	order_by = request.GET.get('order_by', 'released')
	games = Games.objects.all().order_by(order_by)[:16]
	response = TemplateResponse(request, 'shop.html', {'games': games})
	response.render()
	return response

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect(index)
		else:
			return redirect(login)
	else:
    		login_form = LoginForm()
	return render(request,'login.html', {'form': login_form })

def register(request):
	if request.method == 'POST':
		user_form = AddUserForm(data=request.POST)
		if user_form.is_valid():
			user = user_form.save()

			return redirect('index')
	else:
    		user_form = AddUserForm()

	return render(request,'register.html', {'form': user_form })

def logout(request):
	auth_logout(request)
	return redirect('index')

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

def game(request):
	gameID = request.GET['gameID']
	owned = False
	currentuser = request.user
	purchased = Purchased.objects.filter(owner__id=currentuser.id)
	game = Games.objects.get(id=gameID)
	scores = Scores.objects.filter(game__id=gameID)
	users = User.objects.all()
	scorelist = []
	for entry in purchased:
		if game == purchased.game:
			owned = True
			break
	for user in users:
		userscore = []
		userscore.append(user.username)
		for score in scores:
			if score.user == user:
				userscore.append(score.score)
		scorelist.append(userscores)
	scorelist = sorted(scorelist, key=lambda points: points[1], reverse=True)
	response = TemplateResponse(request, 'game.html', {'game': game,'highscores': scorelist, 'owned': owned})
	response.render()
	return response
