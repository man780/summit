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
    path('group/ajax/get/', views.get_group, name="get_ajax_group"),
    path('groups/', views.groups, name='groups'),
    path('group-show/<int:group_id>', views.group_show, name='group_show'),
    path('group-edit/<int:group_id>', views.group_edit, name='group_show'),
    path('create-group/', views.createGroup, name='createGroup'),

    path('lost/', views.lost, name='lost'),
    path('new-groups/', views.new_groups, name='new_groups'),

    path('first-lesson/', views.first_lesson, name='first_lesson'),
    path('star/<int:student_id>', views.send2second_lesson, name='send2second_lesson'),
    path('star-o/<int:student_id>', views.send2first_lesson, name='send2first_lesson'),
    path('r/<int:student_id>', views.student_r, name='student_r'),
    path('student_podo/<int:student_id>', views.student_podo, name='studentPodo'),
    path('student-pay/<int:student_id>', views.student_pay, name='student_pay'),
    path('student-want2pay/<int:student_id>', views.student_want2pay, name='student_want2pay'),

    path('second-lesson/', views.second_lesson, name='second_lesson'),
]
