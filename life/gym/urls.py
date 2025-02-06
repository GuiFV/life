from django.urls import path
from . import views

urlpatterns = [
    path('', views.series, name='gym'),
    path('/clients_programs', views.clients_programs, name='clients_programs'),
]