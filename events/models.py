from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Event(models.Model):
	name = models.CharField(max_length = 200)
	description = models.TextField()
	organizer = models.ForeignKey(User, default = 1, on_delete = models.CASCADE)
	location = models.CharField(max_length = 200)
	date = models.DateField()
	time = models.TimeField()
	seats = models.IntegerField()
	slug = models.SlugField(blank=True)

	def __str__(self):
		return self.name

	def seats_left(self):
		bookings = Book.objects.filter(event=self)
		for book in booking:
			seats_left = seats - bookings
		return seats_left


	# event_ibj.seats_left

def create_slug(instance, new_slug=None):
	slug = slugify (instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Event.objects.filter(slug=slug)
	if qs.exists():
		try:
			int (slug[-1])
			if "-" in slug:
				slug_list = slug.split("-")
				new_slug = "%s-%s"%(slug_list[0],int(slug_list[1])+1)
			else:
				new_slug = "%s-1"%(slug)
		except:
			new_slug = "%s-1"%(slug)
		return create_slug(instance, new_slug=new_slug)
	return slug

@receiver(pre_save, sender=Event)
def generate_slug(instance, *args, **kwargs):
	if not instance.slug:
		instance.slug=create_slug(instance)

class Book(models.Model):
	user = models.ForeignKey(User, default = 1, on_delete = models.CASCADE)
	event = models.ForeignKey(Event, default = 1, on_delete = models.CASCADE)
	tickets = models.IntegerField()




