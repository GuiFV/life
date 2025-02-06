from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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


@staff_member_required
def clients_programs(request):
    # Fetch all users who have at least one active TrainingProgram
    users_with_programs = User.objects.filter(trainingprogram__active=True).distinct()

    # Prepare a dictionary to store each user's programs with grouped exercises
    users_training_programs = {}

    for user in users_with_programs:
        # Fetch the training programs for the current user
        training_programs = TrainingProgram.objects.filter(
            user=user, active=True
        ).prefetch_related('programexercise_set__exercise')

        # Group exercises by 'group' for each program
        for program in training_programs:
            sorted_exercises = sorted(
                program.programexercise_set.all(), key=lambda ex: (ex.group, ex.order)
            )
            program.grouped_exercises = {
                ProgramExercise.GroupChoices(group).label: list(exercises)
                for group, exercises in groupby(sorted_exercises, key=attrgetter('group'))
            }

        # Add the user's programs to the dictionary
        users_training_programs[user] = training_programs

    # Pass the data to the template
    context = {'users_training_programs': users_training_programs}
    return render(request, "gym/clients_programs.html", context)
