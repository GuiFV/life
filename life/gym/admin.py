from django.contrib import admin
from .models import TrainingProgram, Exercise, ProgramExercise


@admin.register(TrainingProgram)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'name', 'active', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user', 'active')

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_user_full_name.short_description = 'Usuário'


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_url')
    search_fields = ('name', 'video_url')


@admin.register(ProgramExercise)
class SeriesExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'program', 'group', 'order', 'color', 'sets', 'repetitions_or_time', 'unit', 'load', 'created_at')
    list_filter = ('program__user',)
