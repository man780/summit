from django.urls import path
from . import views


app_name = 'reception'

urlpatterns = [
    path('reception/', views.reception, name='reception'),
    path('createStudent/', views.createStudent, name='createStudent'),
    path('reception/studentAdd2Group/<int:student_id>',
         views.receptionAddStudent2Group,
         name='receptionAddStudent2Group'),
    path('groups/', views.groups, name='groups'),
    path('createGroup/', views.createGroup, name='createGroup'),
]
