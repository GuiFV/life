from django.contrib import admin
from django.db import models
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

    def save_related(self, request, form, formsets, change):
        """
        Override save_related to ensure ProgramExercises linked to a TrainingProgram
        are saved in the desired order (by `group` and `order`).
        """
        super().save_related(request, form, formsets, change)

        # Ensure `ProgramExercise` is ordered by `group` -> `order`
        program = form.instance  # Get the TrainingProgram instance
        group_order = [
            ProgramExercise.GroupChoices.RELEASE,
            ProgramExercise.GroupChoices.STRETCHING,
            ProgramExercise.GroupChoices.MOBILITY,
            ProgramExercise.GroupChoices.MOTOR_CONTROL,
            ProgramExercise.GroupChoices.STABILITY,
            ProgramExercise.GroupChoices.POWER,
            ProgramExercise.GroupChoices.STRENGTH,
        ]
        program_exercises = ProgramExercise.objects.filter(program=program)

        # Reorder according to `group_order` and save back to database
        for index, exercise in enumerate(
                program_exercises.order_by(
                    models.Case(
                        *(models.When(group=group, then=models.Value(i)) for i, group in enumerate(group_order)),
                        default=models.Value(len(group_order)),
                        output_field=models.IntegerField()
                    ),
                    'order'
                )
        ):
            exercise.order = index + 1  # Optionally, reset the "order" field incrementally
            exercise.save()


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'video_url')
    search_fields = ('name', 'video_url')


@admin.register(ProgramExercise)
class ProgramExerciseAdmin(admin.ModelAdmin):
    list_display = (
    'exercise', 'program', 'group', 'order', 'color', 'sets', 'repetitions_or_time', 'unit', 'load', 'created_at')
    list_filter = ('program__user',)
