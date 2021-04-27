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


def groups(request):
    groups = Group.objects.all()
    if request.GET:
        groups = groups.filter()
    return render(request,
                  'reception/groups.html',
                  {
                      'groups': groups
                  })