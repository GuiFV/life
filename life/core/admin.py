from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from life.core.models import Goal, GoogleAgenda, Notes


class GoalModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'effort', 'area', 'completed']


class NotesAdmin(SummernoteModelAdmin):
    summernote_fields = ('my_notes',)


admin.site.register(Goal, GoalModelAdmin)
admin.site.register(GoogleAgenda)
admin.site.register(Notes, NotesAdmin)
