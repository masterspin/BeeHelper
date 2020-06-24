from django.contrib import admin
from .models import Word, Usage, userFeedback

from import_export.admin import ImportExportModelAdmin

admin.site.register(Word)
admin.site.register(Usage)
admin.site.register(userFeedback)
# class WordAdmin(ImportExportModelAdmin):
# 	list_display = ('name')
