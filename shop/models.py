from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=9, default="user")
	credit = models.IntegerField(default=0)
	confcode = models.CharField(max_length=200, default=None, null=True)
def __str__(self):
	return u'%s %s' % (self.user.name)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

		post_save.connect(create_user_profile, sender=User)

class Games(models.Model):
	name = models.CharField(max_length = 30, unique=True)
	price = models.IntegerField()
	dev = models.ForeignKey(User, on_delete=models.CASCADE)
	released = models.DateField(auto_now_add=True)
	latest = models.DateField(auto_now=True)
	url = models.URLField(default=None)

class Purchased(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Games, on_delete=models.CASCADE)
	active = models.BooleanField(default=False)
	date = models.DateField(auto_now_add=True)

class Scores(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Games, on_delete=models.CASCADE)
	score = models.PositiveIntegerField()

class Saves(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	game = models.ForeignKey(Games, on_delete=models.CASCADE)
	gamestate = models.CharField(max_length=200)
