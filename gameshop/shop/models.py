from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=9, default="user")
	credit = models.IntegerField()

class Games(models.Model):
	name = models.CharField(max_length = 30, unique=True)
	price = models.IntegerField()
	dev = models.ForeignKey(User, on_delete=models.CASCADE)

class Purchased(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Games, on_delete=models.CASCADE)
	active = models.BooleanField(default=False)

class Scores(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Games, on_delete=models.CASCADE)
	score = models.PositiveIntegerField()
	

