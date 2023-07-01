from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from life.core.forms import GoalForm, UserUpdateForm, GoogleAgendaForm
from life.core.models import Goal, GoogleAgenda


@login_required(login_url="/accounts/login/")
def home(request):
    user = request.user
    google_agenda = GoogleAgenda.objects.filter(user=user)
    goals = Goal.objects.filter(user=user)
    form = GoalForm()

    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            form = GoalForm()

    context = {
        'google_agenda': google_agenda,
        'form': form,
        'goals': goals,
    }

    return render(request, 'index.html', context)


@login_required
def profile(request):
    user = request.user
    google_agenda, created = GoogleAgenda.objects.get_or_create(user=user)

    if request.method == 'POST':
        google_agenda_form = GoogleAgendaForm(request.POST, instance=google_agenda)
        user_form = UserUpdateForm(request.POST, instance=user)
        if google_agenda_form.is_valid() and user_form.is_valid():
            google_agenda_form.save()
            user_form.save()
            return redirect('profile')
    else:
        google_agenda_form = GoogleAgendaForm(instance=google_agenda)
        user_form = UserUpdateForm(instance=user)

    context = {'google_agenda_form': google_agenda_form, 'user_form': user_form}
    return render(request, 'user/profile.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('home')
    else:
        return render(request, 'account/delete_account.html')

@login_required
def edit_goal(request, pk):
    user = request.user
    goal = Goal.objects.get(pk=pk, user=user)

    form = GoalForm(request.POST or None, instance=goal)
    if form.is_valid():
        form.save()
        return redirect('/')

    context = {'pk': pk, 'goal': goal, 'form': form}
    return render(request, 'edit_goal.html', context)


@login_required
def delete_goal(request, pk=None):
    user = request.user
    goal = Goal.objects.get(pk=pk, user=user)
    goal.delete()

    return redirect('home')

