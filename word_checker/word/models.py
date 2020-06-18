from django.db import models
import datetime
from django.utils import timezone

class Word(models.Model):
	name = models.CharField(max_length=100)
	definition = models.TextField(default='')
	shortdefinition = models.TextField(default='')
	example = models.TextField(default='')
	pos = models.TextField(default='')
	origin = models.TextField(default='')
	when = models.TextField(default='')
	date = models.DateTimeField(default = datetime.datetime.now)


	def __str__(self):
		return self.name
	

	class Meta:
		verbose_name_plural = 'words'

class Usage(models.Model):
	uploadCount = models.IntegerField()

	def __str__(self):
		return str(self.uploadCount)