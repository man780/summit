from django.urls import path
from . import views


app_name = 'reception'

urlpatterns = [
    path('reception/', views.reception, name='reception'),
    path('create-student/', views.createStudent, name='createStudent'),
    path('edit-student/<int:student_id>/', views.editStudent, name='editStudent'),
    path('delete-student/<int:student_id>/', views.deleteStudent, name='deleteStudent'),
    path('reception/studentAdd2Group/<int:student_id>/',
         views.transferStudent2Group,
         name='transferStudent2Group'),
    path('groups/', views.groups, name='groups'),
    path('create-group/', views.createGroup, name='createGroup'),

    path('lost/', views.lost, name='lost'),
    path('new-groups/', views.new_groups, name='new_groups'),
    path('first-lesson/', views.first_lesson, name='first_lesson'),
    path('second-lesson/', views.second_lesson, name='second_lesson'),
]
