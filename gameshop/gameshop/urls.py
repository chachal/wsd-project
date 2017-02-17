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
	url(r'^scores/$', shopviews.list_scores, name='scores'),
	url(r'^mygames/$', shopviews.mygames, name='mygames'),
	url(r'^shop/$', shopviews.shop, name='shop'),
	url(r'^register/$', shopviews.register),
	url(r'^login', shopviews.login, name='login'),
	url(r'^logout/$', shopviews.logout, name='logout'),

]
