from django.urls import path
from . import views


app_name = 'reception'

urlpatterns = [
    path('reception/', views.reception, name='reception'),
    path('create-student/', views.createStudent, name='createStudent'),
    path('reception/studentAdd2Group/<int:student_id>',
         views.receptionAddStudent2Group,
         name='receptionAddStudent2Group'),
    path('groups/', views.groups, name='groups'),
    path('create-group/', views.createGroup, name='createGroup'),

    path('lost/', views.lost, name='lost'),
    path('new-groups/', views.new_groups, name='new_groups'),
    path('first-lesson/', views.first_lesson, name='first_lesson'),
    path('second-lesson/', views.second_lesson, name='second_lesson'),
]
