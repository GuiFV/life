from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from itertools import groupby
from operator import attrgetter
from life.gym.models import Series, SeriesExercise


@login_required
def series(request):
    user = request.user
    series = Series.objects.filter(
        user=user, active=True
    ).prefetch_related('seriesexercise_set__exercise')

    # Group exercises by 'group' in the view
    for serie in series:
        # Sort the exercises by 'group' and order them (necessary for groupby)
        sorted_exercises = sorted(
            serie.seriesexercise_set.all(), key=lambda ex: (ex.group, ex.order)
        )
        # Group exercises by 'group', converting group to its verbose label
        serie.grouped_exercises = {
            SeriesExercise.GroupChoices(group).label: list(exercises)
            for group, exercises in groupby(sorted_exercises, key=attrgetter('group'))
        }

    context = {'series': series}
    return render(request, 'gym/series.html', context)
