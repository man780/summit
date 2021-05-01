from django.shortcuts import render, redirect
from .models import Students, Group
from refs.models import Phones
from .forms import StudentsCreateForm
from django.contrib import messages


def reception(request):
    students = Students.objects.all()
    if request.GET:
        students = students.filter()
    return render(request,
                  'reception/index.html',
                  {
                      'students': students
                  })


def createStudent(request):
    form = StudentsCreateForm(data=request.GET)

    if request.method == 'POST':
        # Форма отправлена.
        form = StudentsCreateForm(data=request.POST)

        if form.is_valid():
            new_item = form.save()

            studentData = request.POST
            phoneList = studentData.getlist('phone')
            relationList = studentData.getlist('relation')
            for i in range(len(phoneList)):
                phone = Phones(name=relationList[i], number=phoneList[i])
                phone.save()
                new_item.phone.add(phone)

            messages.success(request, 'Student added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения.
            return redirect('/')

    return render(request,
              'reception/createStudent.html',
              {
                  'form': form
              })


def receptionAddStudent2Group(request, student_id):

    student = Students.objects.filter(id=student_id).get()
    if request.method == 'POST':
        pass
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