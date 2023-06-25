from django.contrib import admin
from life.core.models import Goal, GoogleAgenda


class GoalModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'effort', 'area', 'completed']


admin.site.register(Goal, GoalModelAdmin)
admin.site.register(GoogleAgenda)
