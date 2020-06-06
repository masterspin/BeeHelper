from django.forms import ModelForm, TextInput
from .models import Word

class WordForm(ModelForm):
	class Meta:
		model = Word
		fields = ['name']
		widgets = {'name':TextInput(attrs={'class':'input','placeholder' : 'Enter Word'})}