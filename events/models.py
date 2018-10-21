from django.db import models
from django.contrib.auth.models import User


# class Location (models.Model):
# 	city = models.CharField(max_length = 200)
# 	street = models.CharField(max_length = 200)
# 	building = models.CharField(max_length = 200)

class Event(models.Model):
	name = models.CharField(max_length = 200)
	description = models.TextField()
	organizer = models.ForeignKey(User, default = 1, on_delete = models.CASCADE)
	location = models.CharField(max_length = 200)
	date = models.DateField()
	time = models.TimeField()
	seats = models.IntegerField()

	def __str__(self):
		return self.name



