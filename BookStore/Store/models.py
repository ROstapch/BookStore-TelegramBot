from django.db import models
import os
import datetime


def get_image_path(instance, filename):
	return os.path.join('images', str(instance.__class__.__name__), str(instance.name), filename)

def year_choices():
	return [(year, year) for year in range(0, datetime.date.today().year+1)]



class Author(models.Model):
	name = models.CharField(max_length=200)
	photo = models.ImageField(upload_to=get_image_path, blank=True)
	date_of_birth = models.DateField()

	def __str__(self):
		return str(self.name)



class Publisher(models.Model):
	name = models.CharField(max_length=200)
	notes = models.CharField(max_length=500)

	def __str__(self):
		return str(self.name)



class Book(models.Model):
	name = models.CharField(max_length=200)
	cover = models.ImageField(upload_to=get_image_path, blank = True, null=True)
	author = models.ManyToManyField(Author)
	publisher = models.ManyToManyField(Publisher)
	pages = models.PositiveIntegerField()
	year = models.PositiveIntegerField(choices=year_choices(), default=datetime.date.today().year)

	def __str__(self):
		return str(self.name)

