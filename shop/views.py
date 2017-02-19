from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Count, Sum
from django.template.response import TemplateResponse
from django.template import RequestContext
from shop.models import UserProfile, Games, Purchased, Scores
from shop.forms import AddUserForm, LoginForm, Addgameform
from django.core import mail
from django.core.signing import Signer
from shop.util import check_developer, check_admin

from django.contrib.auth.models import User


# Create your views here.

def index(request):
	order_by = request.GET.get('order_by', 'released')
	games = Games.objects.all().order_by(order_by)[:16]
	response = TemplateResponse(request, 'index.html', {'games': games})
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
			signer = Signer()
			signed_value = signer.sign(user_form.cleaned_data['username'])
			key = ''.join(signed_value.split(':')[1:])
			url = 'http://127.0.0.1:8000/confirmation/?code=' + key
			with mail.get_connection() as connection:
				mail.EmailMessage('Registration confirmation', url, to=[user_form.cleaned_data['email']]).send()
			user = user_form.save(key, user_form.cleaned_data['role'])
			return redirect('index')


	else:
    		user_form = AddUserForm()

	return render(request,'register.html', {'form': user_form })

def confirmation(request):
	code = request.GET['code']
	user = UserProfile.objects.get(confcode = code)
	if user.user.is_active:
		return httpresponse('User is already activated')
	else:
		user.user.is_active = 1
		user.user.save()
		return redirect('index')

def logout(request):
	auth_logout(request)
	return redirect('index')

@user_passes_test(check_admin)
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

@login_required
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

def results(request):
	searchterms = request.GET.get('q')
	terms = searchterms.split()
	games = Games.objects.all()
	results = []
	for game in games:
		for term in terms:
			if term in game.name:
				results.append(game)
				break
	response = TemplateResponse(request, 'results.html', {'results': results})
	response.render()
	return response

def developer(request):
	response = TemplateResponse(request, 'admin_base.html')
	response.render()
	return response

def addgame(request):
	if request.method == 'POST':
		form = Addgameform(request.POST, user=request.user)
		if form.is_valid():
			form.save()
			return redirect(developergames)
	else:
		form = Addgameform(user=request.user)

	return render(request, 'addgame.html', {'form': form,})

def developergames(request):
	cur_user = request.user
	games = Games.objects.filter(dev__id = cur_user.id)
	response = TemplateResponse(request, 'developergames.html', {'games':games})
	response.render()
	return response

def statistics(request):
	cur_user = request.user
	games = Games.objects.filter(dev__id = cur_user.id)
	response = TemplateResponse(request, 'admin_base.html', {'games':games})
	response.render()
	return response
