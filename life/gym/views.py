from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from itertools import groupby
from operator import attrgetter
from life.gym.models import TrainingProgram, ProgramExercise
from life.gym.services import group_exercises_by_group


@login_required
def programs(request):
    user = request.user
    training_programs = TrainingProgram.objects.filter(
        user=user, active=True
    ).prefetch_related('programexercise_set__exercise')

    # Group exercises by 'group' in the view
    group_exercises_by_group(training_programs)

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
        group_exercises_by_group(training_programs)

        # Add the user's programs to the dictionary
        users_training_programs[user] = training_programs

    # Pass the data to the template
    context = {'users_training_programs': users_training_programs}
    return render(request, "gym/clients_programs.html", context)
