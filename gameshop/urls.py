"""gameshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from shop import views as shopviews

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', shopviews.index, name='index'),
	url(r'^getScores/$', shopviews.getScores, name='getscores'),
	url(r'^setScores/$', shopviews.setScores, name='setscores'),
	url(r'^saveGame/$', shopviews.saveGame, name='saveGame'),
    url(r'^loadRequest/$', shopviews.loadRequest, name='loadRequest'),
	url(r'^register/$', shopviews.register),
	url(r'^login', shopviews.login, name='login'),
	url(r'^logout/$', shopviews.logout, name='logout'),
	url(r'^confirmation/$', shopviews.confirmation, name='confirmation'),
	url(r'^game/$', shopviews.game, name='mygame'),
	url(r'^developer/$', shopviews.developer, name='developer'),
	url(r'^developer/yourgames/$', shopviews.developergames, name='developergames'),
	url(r'^developer/addgame/$', shopviews.addgame, name='developeradd'),
	url(r'^developer/statistics/$', shopviews.statistics, name='developerstats'),
	url(r'^developer/deletegame/$', shopviews.deletegame, name='deletegame'),
	url(r'^search/$', shopviews.results, name='results'),
	url(r'^shop/$', shopviews.shop, name='shop'),
	url(r'^payment/success?/$', shopviews.paysuccess, name='paysuccess'),
	url(r'^payment/cancel?/$', shopviews.paycancel, name='paycancel'),
	url(r'^payment/fail?/$', shopviews.payfail, name='payfail'),
    url(r'^shop/$', shopviews.shop, name='shop'),
    url(r'^mygames/$', shopviews.mygames, name='mygames')
]
