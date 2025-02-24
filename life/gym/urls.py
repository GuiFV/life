from django.urls import path
from . import views

urlpatterns = [
    path('', views.programs, name='gym'),
    path('clients_programs/', views.clients_programs, name='clients_programs'),
]