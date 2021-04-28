from django.shortcuts import render
from .models import Students, Group


def reception(request):
    students = Students.objects.all()
    if request.GET:
        students = students.filter()
    return render(request,
                  'reception/index.html',
                  {
                      'students': students
                  })


def receptionAddStudent2Group(request, student_id):
    student = Students.objects.filter(id=student_id).get()
    groups = Group.objects.all()

    return render(request,
                  'reception/student2Group.html',
                  {
                      'student': student,
                      'groups': groups
                  })


def groups(request):
    groups = Group.objects.all()
    if request.GET:
        groups = groups.filter()
    return render(request,
                  'reception/groups.html',
                  {
                      'groups': groups
                  })