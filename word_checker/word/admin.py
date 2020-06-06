from django.contrib import admin
from .models import Word

from import_export.admin import ImportExportModelAdmin

admin.site.register(Word)
# class WordAdmin(ImportExportModelAdmin):
# 	list_display = ('name')
