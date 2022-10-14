from django.urls import path
from reception.views import actions, groups, main, students


app_name = 'reception'

urlpatterns = [
    path('reception/', main.reception, name='reception'),
    path('create-student/', students.create_student, name='createStudent'),
    path('edit-student/<int:student_id>/', students.edit_student, name='editStudent'),
    path('delete-student/<int:student_id>/', students.delete_student, name='deleteStudent'),
    path('reception/studentAdd2Group/<int:student_id>/',
         students.transfer_student_to_group,
         name='transferStudent2Group'),
    path('group/ajax/get/', groups.get_group, name="get_ajax_group"),
    path('groups/', groups.groups, name='groups'),
    path('group-show/<int:group_id>', groups.group_show, name='group_show'),
    path('group-edit/<int:group_id>', groups.group_edit, name='group_show'),
    path('create-group/', groups.create_group, name='createGroup'),

    path('new-groups/', groups.new_groups, name='new_groups'),

    path('first-lesson/', main.first_lesson, name='first_lesson'),
    path('second-lesson/', main.second_lesson, name='second_lesson'),
    path('lost/', main.lost, name='lost'),

    path('star/<int:student_id>', actions.send2second_lesson, name='send2second_lesson'),
    path('star-o/<int:student_id>', actions.send2first_lesson, name='send2first_lesson'),
    path('r/<int:student_id>', actions.student_r, name='student_r'),
    path('student_podo/<int:student_id>', actions.student_podo, name='studentPodo'),
    path('student-pay/<int:student_id>', actions.student_pay, name='student_pay'),
    path('student-want2pay/<int:student_id>', actions.student_want2pay, name='student_want2pay'),
]
