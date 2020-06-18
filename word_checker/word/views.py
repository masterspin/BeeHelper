from django.shortcuts import render
import requests
from .models import Word
from .forms import WordForm
from django.core.files.storage import FileSystemStorage
import glob, os, os.path
import xlsxwriter
import csv
from django.http import HttpResponse
from datetime import datetime,timedelta
from django.utils import timezone


# Create your views here.

arr=[]
def index(request):
	url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/{}?key=19a9261a-6c93-4bc2-a179-83d7cc4189df'	
	arrduplicate = []
	global arr
	arr=[]
	words = Word.objects.all()
	if request.method == 'POST':
		Word.objects.all().filter(date__lte=datetime.now()-timedelta(hours=48)).delete()
		# for j in words:
		# 	if(datetime.now()-j.date.replace(tzinfo=None)>timedelta(minutes=1).total_seconds()):
		# 		Word.objects.filter(name=j.name).delete()
		uploaded_file = request.FILES['document']
		fs = FileSystemStorage()
		fs.save(uploaded_file.name, uploaded_file)
		file = open('\\Users\\ritij\\Words\\word_checker\\media\\'+uploaded_file.name)
		f = file.readlines()
		for line in f:
			arr.append(line.strip().capitalize())
			arrduplicate.append(line.strip().capitalize())
		# for i in arr:
		# 	word_instance = Word.objects.create(name = i)
		file.close()
		for i in words:
			if i.name in arrduplicate:
				arrduplicate.remove(i.name)
		os.remove('\\Users\\ritij\\Words\\word_checker\\media\\'+uploaded_file.name)
	word_data = []

	# for i in words:
	# 	if i not in arr:
	# 		print (i)


	for word in arrduplicate:
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

		definition = ""
		if 'def' in r[0]:
			if 'sseq' in r[0]['def'][0]:
				for i in range(len(r[0]['def'][0]['sseq'])):
					if 'dt' in r[0]['def'][0]['sseq'][i][0][1]:
						definition += r[0]['def'][0]['sseq'][i][0][1]['dt'][0][1]+"++"
		# print(definition)
		definition = definition.replace("{bc}","")
		definition = definition.replace("{sx","")
		definition = definition.replace("{d_link","")
		definition = definition.replace("d_link","")
		definition = definition.replace("{/it}","")
		definition = definition.replace("{it}","")
		definition = definition.replace("||2}","")
		definition = definition.replace("{dxt","")
		definition = definition.replace("{dx}","")
		definition = definition.replace("{dx_def}","")
		definition = definition.replace("{/dx_def}","")
		definition = definition.replace(":1||4","")
		definition = definition.replace(":1||3","")
		definition = definition.replace("||3","")
		definition = definition.replace("||4","")
		definition = definition.replace("||8","")
		definition = definition.replace(":1","")
		definition = definition.replace(":2","")
		definition = definition.replace("||7","")
		definition = definition.replace("|3b","")
		definition = definition.replace("{/dx}","")
		definition = definition.replace("||2}","")
		definition = definition.replace("||1}","")
		definition = definition.replace("||5b}","")
		definition = definition.replace("||b}","")
		definition = definition.replace("{a_link","")
		definition = definition.replace("|","")
		definition = definition.replace("}","")
		definition = definition.replace("{","")
		definition = definition.replace("++", "; ")

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
		Origin = Origin.replace(":1","")

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
		Date = Date.replace("{ds","")
		Date = Date.replace("||1","")
		Date = Date.replace("|1","")
		Date = Date.replace("|a|","")
		Date = Date.replace("{","")
		Date = Date.replace("}","")

		example = ""

		if 'dros' in r[0]:
			example = example + r[0]['dros'][0]['drp'] + "; "
		else:
	 		example = ""




		partOfSpeech = ""

		if 'fl' in r[0]:
	 		partOfSpeech = r[0]['fl']


		short_definition=""

		if 'shortdef' in r[0]:
			short_definition = r[0]['shortdef']
			if(short_definition == []):
				short_definition = ""
			else:
				short_definition = r[0]['shortdef'][0]
		else:
			short_definition=""
 	

		# word_attribute = {
		# 	'word' : word.name,
		# 	'definition' : definition,#r_data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1],
		# 	# 'stems' : r_data[meta][stems],
		# 	'short_definition':  short_definition,
		# 	'example':  example, #r_data[0]['def'][0]['sseq'][0][0][1]['dt'][1][1][0]['t']
		# 	'partOfSpeech': partOfSpeech,
		# 	'Origin' : Origin,
		# 	'Date': Date,


		# }
		# print(word_attribute)
		# word_data.append(word_attribute)
		Word.objects.create(name = word, definition = definition, shortdefinition=short_definition, example=example, pos=partOfSpeech, origin = Origin, when = Date)
	# workbook = xlsxwriter.Workbook('C:/Users/ritij/Words/word_checker/media/Excel_File.xlsx')
	# worksheet = workbook.add_worksheet()
	# bold = workbook.add_format({'bold': True})

	# if len(word_data)>0:	
	# 	context = {'word_data' : word_data}
	# else:
	# 	word_data = [{'word': "ERROR. Your file may be empty.Please check again", 'definition':"",'short_definition':"",'example':"",'partOfSpeech':"",'Origin':"",'Date':""}]
	# 	context = {'word_data' : word_data}

	# row = 0
	# col = 0
	# word_categories = ['Word','Definition','Short Definition','Example','Part Of Speech','Origin','Date']
	# for i in word_categories:
	# 	worksheet.write(row,col, i, bold)
	# 	col+=1

	# row = 1
	# col = 0
	# for i in word_data:
	# 	worksheet.write(row,col, i.get('word'))
	# 	worksheet.write(row,col+1, i.get('definition'))
	# 	worksheet.write(row,col+2, i.get('short_definition'))
	# 	worksheet.write(row,col+3, i.get('example'))
	# 	worksheet.write(row,col+4, i.get('partOfSpeech'))
	# 	worksheet.write(row,col+5, i.get('Origin'))
	# 	worksheet.write(row,col+6, i.get('Date'))
	# 	row+=1
	# workbook.close()
	#os.remove('\\Users\\ritij\\Words\\word_checker\\media\\'+'Excel_File.xlsx')
	
	#return response
	words = Word.objects.all()
	for word in words:
		if word.name in arr:
			word_data.append(word)
	context = {'word_data':word_data}
	return render(request,'word/word.html', context)


def download(request):
	# url = 'https://dictionaryapi.com/api/v3/references/collegiate/json/{}?key=19a9261a-6c93-4bc2-a179-83d7cc4189df'
	words = Word.objects.all()
	# word_data=[]
	# print(words)
	# for word in words:
	# 	r = requests.get(url.format(word)).json()


	# 	definition = ""
	# 	if 'def' in r[0]:
	# 		if 'sseq' in r[0]['def'][0]:
	# 			for i in range(len(r[0]['def'][0]['sseq'])):
	# 				if 'dt' in r[0]['def'][0]['sseq'][i][0][1]:
	# 					definition += r[0]['def'][0]['sseq'][i][0][1]['dt'][0][1]+"++"
	# 	# print(definition)
	# 	definition = definition.replace("{bc}","")
	# 	definition = definition.replace("{sx","")
	# 	definition = definition.replace("{d_link","")
	# 	definition = definition.replace("d_link","")
	# 	definition = definition.replace("{/it}","")
	# 	definition = definition.replace("{it}","")
	# 	definition = definition.replace("||2}","")
	# 	definition = definition.replace("{dxt","")
	# 	definition = definition.replace("{dx}","")
	# 	definition = definition.replace("{dx_def}","")
	# 	definition = definition.replace("{/dx_def}","")
	# 	definition = definition.replace(":1||4","")
	# 	definition = definition.replace(":1||3","")
	# 	definition = definition.replace("||3","")
	# 	definition = definition.replace("||4","")
	# 	definition = definition.replace("||8","")
	# 	definition = definition.replace(":1","")
	# 	definition = definition.replace(":2","")
	# 	definition = definition.replace("||7","")
	# 	definition = definition.replace("|3b","")
	# 	definition = definition.replace("{/dx}","")
	# 	definition = definition.replace("||2}","")
	# 	definition = definition.replace("||1}","")
	# 	definition = definition.replace("||5b}","")
	# 	definition = definition.replace("||b}","")
	# 	definition = definition.replace("{a_link","")
	# 	definition = definition.replace("|","")
	# 	definition = definition.replace("}","")
	# 	definition = definition.replace("{","")
	# 	definition = definition.replace("++", "; ")

	# 	yesOrigin = False

	# 	Origin = ""
	# 	if 'et' not in r[0]:
	# 		yesOrigin=False
	# 		print("not in data")
	# 	else:
	# 		yesOrigin=True

	# 	if(yesOrigin==True):
	# 		Origin = r[0]['et'][0][1]
	# 	else:
	# 		Origin = ""

	# 	Origin = Origin.replace("{ds||1|a|}","")
	# 	Origin = Origin.replace("{ds||1||}","")
	# 	Origin = Origin.replace("{it}","")
	# 	Origin = Origin.replace("{/it}","")
	# 	Origin = Origin.replace("{ma}","")
	# 	Origin = Origin.replace("{mat","")
	# 	Origin = Origin.replace("}{/ma}","")
	# 	Origin = Origin.replace("|void:3|","")
	# 	Origin = Origin.replace("{et_link|","")
	# 	Origin = Origin.replace("{","")
	# 	Origin = Origin.replace("}","")
	# 	Origin = Origin.replace("|by:1|, |out:1|","")
	# 	Origin = Origin.replace("|by:1|","")
	# 	Origin = Origin.replace("|out:1|","")
	# 	Origin = Origin.replace(":1","")

	# 	Date = ""
	# 	if 'date' in r[0]:
	# 		Date = r[0]['date']
	# 	else:
	# 		Date = ""
	# 	Date = Date.replace("{ds||1|a|}","")
	# 	Date = Date.replace("{ds||1||}","")
	# 	Date = Date.replace("{ds||2||}","")
	# 	Date = Date.replace("{ds||7||}","")
	# 	Date = Date.replace("{ds|t|1||}","")
	# 	Date = Date.replace("{ds|t|1|a|}","")
	# 	Date = Date.replace("{ds||2|b|}","")
	# 	Date = Date.replace("{ds|i|3|a|}","")
	# 	Date = Date.replace("{ds","")
	# 	Date = Date.replace("||1","")
	# 	Date = Date.replace("|1","")
	# 	Date = Date.replace("|a|","")
	# 	Date = Date.replace("{","")
	# 	Date = Date.replace("}","")

	# 	example = ""

	# 	if 'dros' in r[0]:
	# 		example = example + r[0]['dros'][0]['drp'] + "; "
	# 	else:
	#  		example = ""




	# 	partOfSpeech = ""

	# 	if 'fl' in r[0]:
	#  		partOfSpeech = r[0]['fl']


	# 	short_definition=""

	# 	if 'shortdef' in r[0]:
	# 		short_definition = r[0]['shortdef']
	# 		if(short_definition == []):
	# 			short_definition = ""
	# 		else:
	# 			short_definition = r[0]['shortdef'][0]
	# 	else:
	# 		short_definition=""
 	

	# 	word_attribute = {
	# 		'word' : word.name,
	# 		'definition' : definition,#r_data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1],
	# 		# 'stems' : r_data[meta][stems],
	# 		'short_definition':  short_definition,
	# 		'example':  example, #r_data[0]['def'][0]['sseq'][0][0][1]['dt'][1][1][0]['t']
	# 		'partOfSpeech': partOfSpeech,
	# 		'Origin' : Origin,
	# 		'Date': Date,


	# 	}
	# 	# print(word_attribute)
	# 	word_data.append(word_attribute)

	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)
	writer.writerow(['Word','Definition','Short Definition','Example','Part Of Speech','Origin','Date'])
	global arr
	for i in words:
		if i.name in arr:
			writer.writerow([i.name,i.definition,i.shortdefinition,i.example,i.pos,i.origin,i.when])
	response['Content-Disposition'] = 'attachment;filename="WordAttributeFile.csv"'
	return response



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