from django.shortcuts import render


def series(request):


    context = {}
    return render(request, 'gym/series.html', context)
