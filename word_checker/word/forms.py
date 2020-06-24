from django.forms import ModelForm, TextInput
from .models import Word, Usage, userFeedback

class WordForm(ModelForm):
	class Meta:
		model = Word
		fields = ['name']
		widgets = {'name':TextInput(attrs={'class':'input','placeholder' : 'Enter Word'})}

class FeedbackForm(ModelForm):
	class Meta:
		model = userFeedback
		fields = ('firstName','lastName','email','comment')
		widgets = {'firstName':TextInput(attrs={'class':'input','placeholder' : 'Enter First Name'}),
					'lastName':TextInput(attrs={'class':'input','placeholder' : 'Enter Last Name'}),
					'email':TextInput(attrs={'class':'input','placeholder' : 'Enter Email'}),
					'comment':TextInput(attrs={'class':'input','placeholder' : 'Enter Feedback'}),






		}
		
