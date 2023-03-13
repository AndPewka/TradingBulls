from django.db import models


class User(models.Model):
	ui = models.IntegerField()
	name = models.CharField(max_length=50)
	first_ip = models.CharField(max_length=16)
	requests = models.IntegerField(default=0)
	ans_added = models.IntegerField(default=0)
	ans_got = models.IntegerField(default=0)
	subsription_lvl = models.CharField(max_length=20, default="blank")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "%d" % self.ui

class Rsi(models.Model):
	symbol = models.CharField(max_length=25)
	interval = models.CharField(max_length=5)
	period = models.IntegerField(default=3)
	infelicity = models.IntegerField(default=1)
	value = models.IntegerField(default=0)
	last_value = models.IntegerField(default=0)
	price = models.IntegerField(default=0)
	side = models.CharField(max_length=10, default="")
	created = models.DateTimeField(auto_now_add=True)
