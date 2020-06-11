from django.shortcuts import render
import requests
from .models import Word
from .forms import WordForm
from django.core.files.storage import FileSystemStorage
import glob, os, os.path

# Create your views here.

def index(request):
	url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/{}?key=19a9261a-6c93-4bc2-a179-83d7cc4189df'
	if request.method == 'POST':
		Word.objects.all().delete()
		uploaded_file = request.FILES['document']
		print(uploaded_file.name)
		print(uploaded_file.size)
		fs = FileSystemStorage()
		fs.save(uploaded_file.name, uploaded_file)
		arr = []
		file = open('\\Users\\ritij\\Words\\word_checker\\media\\'+uploaded_file.name)
		f = file.readlines()
		for line in f:
			arr.append(line.strip())
		for i in arr:
			word_instance = Word.objects.create(name = i)
		file.close()
		os.remove('\\Users\\ritij\\Words\\word_checker\\media\\'+uploaded_file.name)
	word_data = []
	words = Word.objects.all()
	for word in words:
		r = requests.get(url.format(word)).json()


# definition_length = len(r[0]['def'][0]['sseq'])
# definition = ""
# for i in range(0,definition_length):
# 	definition = definition + r[0]['def'][0]['sseq'][i][0][1]['dt'][0][1] + "\t"

# definition = definition.replace("{/it}","")
# definition = definition.replace("{it}","")
# definition = definition.replace("{bc}","||| ")


# short_definition=""
# short_definition_length = len(r_data[0]['shortdef'])
# for i in range(0,short_definition_length):
# 	short_definition = short_definition+r_data[0]['shortdef'][i] + "\t"

		yesOrigin = False

		Origin = ""
		if 'et' not in r[0]:
			yesOrigin=False
			print("not in data")
		else:
			yesOrigin=True

		if(yesOrigin==True):
			Origin = r[0]['et'][0][1]
		else:
			Origin = ""

		Origin = Origin.replace("{ds||1|a|}","")
		Origin = Origin.replace("{ds||1||}","")
		Origin = Origin.replace("{it}","")
		Origin = Origin.replace("{/it}","")
		Origin = Origin.replace("{ma}","")
		Origin = Origin.replace("{mat","")
		Origin = Origin.replace("}{/ma}","")
		Origin = Origin.replace("|void:3|","")
		Origin = Origin.replace("{et_link|","")
		Origin = Origin.replace("{","")
		Origin = Origin.replace("}","")
		Origin = Origin.replace("|by:1|, |out:1|","")
		Origin = Origin.replace("|by:1|","")
		Origin = Origin.replace("|out:1|","")

		Date = ""
		if 'date' in r[0]:
			Date = r[0]['date']
		else:
			Date = ""
		Date = Date.replace("{ds||1|a|}","")
		Date = Date.replace("{ds||1||}","")
		Date = Date.replace("{ds||2||}","")
		Date = Date.replace("{ds||7||}","")
		Date = Date.replace("{ds|t|1||}","")
		Date = Date.replace("{ds|t|1|a|}","")
		Date = Date.replace("{ds||2|b|}","")
		Date = Date.replace("{ds|i|3|a|}","")

		example = ""

		if 'dros' in r[0]:
			example = example + r[0]['dros'][0]['drp'] + "; "
		else:
	 		example = ""




		partOfSpeech = ""

		if 'fl' in r[0]:
	 		partOfSpeech = r[0]['fl']


		short_definition = r[0]['shortdef']
		if(short_definition == []):
			short_definition = ""
		else:
			short_definition = r[0]['shortdef'][0] 	

		word_attribute = {
			'word' : word.name,
			# 'definition' : definition,#r_data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1],
			# 'stems' : r_data[meta][stems],
			'short_definition':  short_definition,
			'example':  example, #r_data[0]['def'][0]['sseq'][0][0][1]['dt'][1][1][0]['t']
			'partOfSpeech': partOfSpeech,
			'Origin' : Origin,
			'Date': Date,


		}

		word_data.append(word_attribute)
	print(word_data)
	context = {'word_data' : word_data}	
	return render(request,'word/word.html', context)


# def index(request):
# 	url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/{}?key=19a9261a-6c93-4bc2-a179-83d7cc4189df'

# 	if request.method == 'POST':
# 		form = WordForm(request.POST)
# 		form.save()

# 	form = WordForm()


# 	word_data = []

# 	words = Word.objects.all()
# 	for word in words:
# 		r = requests.get(url.format(word)).json()

	
# 	# definition_length = len(r[0]['def'][0]['sseq'])
# 	# definition = ""
# 	# for i in range(0,definition_length):
# 	# 	definition = definition + r[0]['def'][0]['sseq'][i][0][1]['dt'][0][1] + "\t"

# 	# definition = definition.replace("{/it}","")
# 	# definition = definition.replace("{it}","")
# 	# definition = definition.replace("{bc}","||| ")


# 	# short_definition=""
# 	# short_definition_length = len(r_data[0]['shortdef'])
# 	# for i in range(0,short_definition_length):
# 	# 	short_definition = short_definition+r_data[0]['shortdef'][i] + "\t"

# 		yesOrigin = False

# 		Origin = ""
# 		if 'et' not in r[0]:
# 			yesOrigin=False
# 			print("not in data")
# 		else:
# 			yesOrigin=True

# 		if(yesOrigin==True):
# 			Origin = r[0]['et'][0][1]
# 		else:
# 			Origin = ""

# 		Origin = Origin.replace("{ds||1|a|}","")
# 		Origin = Origin.replace("{ds||1||}","")
# 		Origin = Origin.replace("{it}","")
# 		Origin = Origin.replace("{/it}","")
# 		Origin = Origin.replace("{ma}","")
# 		Origin = Origin.replace("{mat","")
# 		Origin = Origin.replace("}{/ma}","")
# 		Origin = Origin.replace("|void:3|","")
# 		Origin = Origin.replace("{et_link|","")
# 		Origin = Origin.replace("{","")
# 		Origin = Origin.replace("}","")
# 		Origin = Origin.replace("|by:1|, |out:1|","")
# 		Origin = Origin.replace("|by:1|","")
# 		Origin = Origin.replace("|out:1|","")

# 		Date = ""
# 		if 'date' in r[0]:
# 			Date = r[0]['date']
# 		else:
# 			Date = ""
# 		Date = Date.replace("{ds||1|a|}","")
# 		Date = Date.replace("{ds||1||}","")
# 		Date = Date.replace("{ds||2||}","")
# 		Date = Date.replace("{ds||7||}","")
# 		Date = Date.replace("{ds|t|1||}","")
# 		Date = Date.replace("{ds|t|1|a|}","")
# 		Date = Date.replace("{ds||2|b|}","")
# 		Date = Date.replace("{ds|i|3|a|}","")

# 		example = ""

# 		if 'dros' in r[0]:
# 			example = example + r[0]['dros'][0]['drp'] + "; "
# 		else:
# 	 		example = ""




# 		partOfSpeech = ""

# 		if 'fl' in r[0]:
# 	 		partOfSpeech = r[0]['fl']


# 		short_definition = r[0]['shortdef']
# 		if(short_definition == []):
# 			short_definition = ""
# 		else:
# 			short_definition = r[0]['shortdef'][0] 	

# 		word_attribute = {
# 			'word' : word.name,
# 			# 'definition' : definition,#r_data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1],
# 			# 'stems' : r_data[meta][stems],
# 			'short_definition':  short_definition,
# 			'example':  example, #r_data[0]['def'][0]['sseq'][0][0][1]['dt'][1][1][0]['t']
# 			'partOfSpeech': partOfSpeech,
# 			'Origin' : Origin,
# 			'Date': Date,


# 		}

# 		word_data.append(word_attribute)

# 	print(word_data)

# 	context = {'word_data' : word_data, 'form':form}

# 	return render(request, 'word/word.html',context)