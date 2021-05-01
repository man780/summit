from django.shortcuts import render, redirect
from .models import Students, Group, StudentTransferGroup
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
    import datetime
    student = Students.objects.filter(id=student_id).get()
    if request.method == 'POST':
        formData = request.POST
        group_id = formData.get('group_id')
        student.group_id = group_id
        student.save()
        dateStr = formData.get('date')
        date = datetime.datetime.strptime(dateStr, "%Y-%m-%d").date()
        transfer = StudentTransferGroup(student_id=student_id, group_id=group_id, date=date, sequence=1)
        transfer.save()
        # print(transfer)
        # print(formData.get('date'), formData.get('group_id'))
        # import sys
        # sys.exit()

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