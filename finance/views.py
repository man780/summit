from django.shortcuts import render, redirect, get_object_or_404
from reception.models import Students, Group


def index(request):
    students = Students.objects.all()
    return render(request,
                  'finance/index.html',
                  {
                      'students': students
                  })
