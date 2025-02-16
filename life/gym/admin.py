from django.contrib import admin
from .models import TrainingProgram, Exercise, ProgramExercise


class ProgramExerciseInline(admin.TabularInline):  # Inline for ProgramExercise
    model = ProgramExercise
    extra = 0  # No extra empty fields
    fields = (
    'exercise', 'group', 'order', 'color', 'sets', 'repetitions_or_time', 'unit', 'load')  # Display desired fields
    readonly_fields = ('created_at',)  # Make fields like `created_at` readonly
    ordering = ('group', 'order')  # Sort exercises by `group` and `order`
    verbose_name = 'Program Exercise'
    verbose_name_plural = 'Program Exercises'


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'name', 'active', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('user', 'active')
    inlines = [ProgramExerciseInline]  # Add the inline class here

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_user_full_name.short_description = 'Usuário'  # Label for the custom method


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_url')
    search_fields = ('name', 'video_url')


@admin.register(ProgramExercise)
class ProgramExerciseAdmin(admin.ModelAdmin):
    list_display = (
    'exercise', 'program', 'group', 'order', 'color', 'sets', 'repetitions_or_time', 'unit', 'load', 'created_at')
    list_filter = ('program__user',)
