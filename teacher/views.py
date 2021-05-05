from django.shortcuts import render, get_object_or_404, get_list_or_404
from reception.models import Students, Group


def index(request):
    breadcrumbs = [
        {
            'name': 'Главная',
            'url': '/',
            'class': '',
        },
    ]
    bodyclass = 'sidebar-collapse'
    title = 'test'
    return render(request,
                  'teacher/index.html',
                  {title: title,
                   'breadcrumbs': breadcrumbs,
                   'bodyclass': bodyclass})


def student(request, id):
    student = get_object_or_404(Students, id=id)
    data_dict = {
        'student': student
    }
    return render(request,
                  'teacher/student.html',
                  data_dict)


def group_students(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    students = get_list_or_404(Students, group_id=group_id)
    data_dict = {
        'group': group,
        'students': students
    }
    return render(request,
                  'teacher/group_students.html',
                  data_dict)


def dashboard(request):
    return render(request,
                  'teacher/dashboard.html')
