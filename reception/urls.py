from django.urls import path
from . import views


app_name = 'reception'

urlpatterns = [
    path('reception/', views.reception, name='reception'),
    path('create-student/', views.create_student, name='createStudent'),
    path('edit-student/<int:student_id>/', views.edit_student, name='editStudent'),
    path('delete-student/<int:student_id>/', views.delete_student, name='deleteStudent'),
    path('reception/studentAdd2Group/<int:student_id>/',
         views.transfer_student_to_group,
         name='transferStudent2Group'),
    path('group/ajax/get/', views.get_group, name="get_ajax_group"),
    path('groups/', views.groups, name='groups'),
    path('group-show/<int:group_id>', views.group_show, name='group_show'),
    path('group-edit/<int:group_id>', views.group_edit, name='group_show'),
    path('create-group/', views.create_group, name='createGroup'),

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
