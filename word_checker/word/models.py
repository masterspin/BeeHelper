from django.db import models

class Word(models.Model):
	name = models.CharField(max_length = 300)


	def __str__(self):
		return self.name
	

	class Meta:
		verbose_name_plural = 'words'
