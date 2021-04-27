from django.urls import path
from . import views


app_name = 'reception'

urlpatterns = [
    path('reception/', views.reception, name='reception'),
    path('groups/', views.groups, name='groups'),
]
