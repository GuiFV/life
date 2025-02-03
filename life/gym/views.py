from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from itertools import groupby
from operator import attrgetter
from life.gym.models import TrainingProgram, ProgramExercise


@login_required
def series(request):
    user = request.user
    training_programs = TrainingProgram.objects.filter(
        user=user, active=True
    ).prefetch_related('programexercise_set__exercise')

    # Group exercises by 'group' in the view
    for program in training_programs:
        # Sort the exercises by 'group' and order them (necessary for groupby)
        sorted_exercises = sorted(
            program.programexercise_set.all(), key=lambda ex: (ex.group, ex.order)
        )
        # Group exercises by 'group', converting group to its verbose label
        program.grouped_exercises = {
            ProgramExercise.GroupChoices(group).label: list(exercises)
            for group, exercises in groupby(sorted_exercises, key=attrgetter('group'))
        }

    context = {'training_programs': training_programs}
    return render(request, 'gym/series.html', context)
