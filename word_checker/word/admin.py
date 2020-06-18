from django.contrib import admin
from .models import Word, Usage

from import_export.admin import ImportExportModelAdmin

admin.site.register(Word)
admin.site.register(Usage)
# class WordAdmin(ImportExportModelAdmin):
# 	list_display = ('name')
