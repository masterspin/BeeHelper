from django.forms import ModelForm, TextInput
from .models import Word, Usage

class WordForm(ModelForm):
	class Meta:
		model = Word
		fields = ['name']
		widgets = {'name':TextInput(attrs={'class':'input','placeholder' : 'Enter Word'})}

# class UsageForm(ModelForm):
# 	class Meta:
# 		model = Usage
# 		fields = ['uploadCount']