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
from hashlib import md5

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
			url = 'https://aqueous-brook-23280.herokuapp.com/confirmation/?code=' + key
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
		if game == entry.game:
			owned = True
			break
	for user in users:
		userscore = []
		userscore.append(user.username)
		for score in scores:
			if score.user == user:
				userscore.append(score.score)
		scorelist.append(userscore)
	if len(userscore) > 1:
		scorelist = sorted(scorelist, key=lambda points: points[1], reverse=True)

	pid = "{}:{}".format(currentuser.id, game.id)
	checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, "GameshopAAC", game.price, "c858a84d04755915ded5daba44a3644f")
	m = md5(checksumstr.encode("ascii"))
	checksum = m.hexdigest()

	response = TemplateResponse(request, 'game.html', {'game': game,'highscores': scorelist, 'owned': owned, 'checksum':checksum, 'pid':pid})
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

	return render(request, 'addgame.html', {'form': form})

def deletegame(request):
	gameid = request.POST['gameid']
	game = Games.objects.get(id=gameid)
	game.delete()
	return redirect('developergames')

def developergames(request):
	cur_user = request.user
	games = Games.objects.filter(dev__id = cur_user.id)
	response = TemplateResponse(request, 'developergames.html', {'games':games})
	response.render()
	return response
		

def statistics(request):
	gameid = request.GET['gameid']
	cur_user = request.user
	game = Games.objects.get(id=gameid)
	purchases = Purchased.objects.filter(game_id=gameid)
	total = len(purchases)
	revenue = total*game.price
	response = TemplateResponse(request, 'developerstats.html', {'purchases':purchases,'total':total,'game':game,'revenue':revenue})
	response.render()
	return response

def shop(request):
	order_by_name = request.GET.get('order_by', 'name')
	order_by_price = request.GET.get('order_by', 'price')
	order_by_developer = request.GET.get('order_by', 'developer')
	order_by_released = request.GET.get('order_by', 'released')
	games = Games.objects.all().order_by(order_by_name)
	response = TemplateResponse(request, 'shop.html', {'games': games, 'order_by_name': order_by_name,'order_by_price': order_by_price,'order_by_developer': order_by_developer,'order_by_released': order_by_released})
	response.render()
	return response


def paysuccess(request):
	pid = request.GET['pid']
	ref = request.GET['ref']
	result = request.GET['result']
	checksum = request.GET['checksum']
	
	checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, ref, result, "c858a84d04755915ded5daba44a3644f")
	m = md5(checksumstr.encode("ascii"))
	checksumlocal = m.hexdigest()

	#if checksum == checksumlocal:
	userid,gameid = pid.split(":")
	user = User.objects.get(id=userid)
	purchasedgame = Games.objects.get(id=gameid)
	p = Purchased(owner=user, game=purchasedgame, active=True)
	p.save()
	return redirect('/game/?gameID='+gameid)
	#else:
	#	return HttpResponse("404")
	
def paycancel(request):
	return HttpResponse("404")
	
def payfail(request):
	return HttpResponse("404")
	

def mygames(request):
	currentuser = request.user
	order_by_name = request.GET.get('order_by', 'game__name')
	order_by_developer = request.GET.get('order_by', 'game__developer')
	order_by_released = request.GET.get('order_by', 'game__released')
	owned_games = Purchased.objects.filter(owner__id=currentuser.id).order_by(order_by_name)
	response = TemplateResponse(request, 'mygames.html', {'owned_games': owned_games, 'order_by_name': order_by_name,
													      'order_by_developer': order_by_developer,
													      'order_by_released': order_by_released})
	response.render()
	return response

def newgames(request):
	order_by = request.GET.get('order_by', 'released')
	games = Games.objects.all(released__year=today.year, released__month=today.month).order_by(order_by)
	response = TemplateResponse(request, 'index.html', {'games': games})
	response.render()
	return response

