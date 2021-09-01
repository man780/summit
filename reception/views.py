from django.shortcuts import render, redirect, get_object_or_404
from .models import Students, Group, StudentTransferGroup, Room, StudentLessons, Lost
from refs.models import Phones, PreferDays, PreferTimes
from finance.models import Payment
from .forms import StudentsCreateForm, GroupCreateForm
from django.contrib import messages
from django.db.models import Prefetch
import datetime


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
            new_student = form.save(commit=False)
            new_student.created_by = request.user
            new_student.save()

            studentData = request.POST
            phoneList = studentData.getlist('phone')
            relationList = studentData.getlist('relation')
            for i in range(len(phoneList)):
                phone = Phones(name=relationList[i], number=phoneList[i])
                phone.save()
                new_student.phone.add(phone)

            messages.success(request, 'Student added successfully')
            return redirect('reception:reception')

    return render(request,
              'reception/createStudent.html',
              {
                  'form': form
              })


def editStudent(request, student_id):

    student = get_object_or_404(Students, id=student_id)
    form = StudentsCreateForm(request.POST or None, instance=student)
    if request.method == 'POST':
        # Форма отправлена.
        form = StudentsCreateForm(data=request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()

            studentData = request.POST
            phoneList = studentData.getlist('phone')
            relationList = studentData.getlist('relation')
            for i in range(len(phoneList)):
                if relationList[i] != '' or phoneList[i] != '':
                    phone = Phones(name=relationList[i], number=phoneList[i])
                    phone.save()
                    student.phone.add(phone)

            messages.success(request, 'Student added successfully')
            return redirect('reception:reception')

    return render(request,
              'reception/createStudent.html',
              {
                  'form': form
              })


def deleteStudent(request, student_id):
    student = get_object_or_404(Students, id=student_id)

    if request.method == "POST":
        # delete object
        student.delete()
        messages.error(request, 'Student successfully deleted')
        return redirect("reception:reception")

    return render(request, "reception/studentDelete.html", {
        'student': student
    })


def transferStudent2Group(request, student_id):

    student = Students.objects.filter(id=student_id).get()
    if request.method == 'POST':
        formData = request.POST
        group_id = formData.get('group_id')
        student.group_id = group_id
        student.save()
        dateStr = formData.get('date')
        date = datetime.datetime.strptime(dateStr, "%Y-%m-%d").date()

        transfer = StudentTransferGroup.objects.filter(student_id=student_id, status=True).first()
        if transfer:
            transfer.status = False
            transfer.save()

        group = Group.objects.get(id=group_id)
        sequence = group.get_current_student_count()

        StudentTransferGroup.objects.create(
            student_id=student_id,
            group_id=group_id,
            date=date,
            sequence=sequence+1,
            status=True
        )
        StudentLessons.objects.create(
            student=student,
            group=group,
            date=date,
            is_first=True
        )
        # next_month = datetime.datetime.strptime(dateStr, "%Y-%m-%d").date()
        next_month = datetime.datetime(date.year + int(date.month / 12), ((date.month % 12) + 1), 1)
        Payment.objects.create(
            date=date,
            student=student,
            status=0,
            from_date=date,
            to_date=next_month,
        )

    groups = Group.objects.all()

    return render(request,
                  'reception/student2Group.html',
                  {
                      'student': student,
                      'groups': groups
                  })


def groups(request):
    groups = Group.objects.all()
    rooms = Room.objects.all()
    times = PreferTimes.objects.all()

    scheduleList = []
    for room in rooms:
        scheduleList.insert(
            room.id,
            {
                'id': room.id,
                'name': room.name,
                'times': [{'class': 'button', 'name': ''} for x in times]
            }
        )

    for group in groups:
        scheduleList[group.room.id-1]['times'][group.times.id-1] = {'class': 'full', 'name': group.name}

    return render(request,
                  'reception/groups.html',
                  {
                      'rooms': rooms,
                      'groups': groups,
                      'times': times,
                      'schedule': scheduleList,
                  })


def createGroup(request):
    form = GroupCreateForm(data=request.GET)

    if request.method == 'POST':
        # Форма отправлена.
        form = GroupCreateForm(data=request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            messages.success(request, 'Group added successfully')
            # Перенаправляем пользователя на страницу груп.
            return redirect('reception:groups')

    return render(request,
                  'reception/createGroup.html',
                  {
                      'form': form
                  })


def lost(request):
    students = Students.objects.all()
    return render(request,
                  'reception/lost.html',
                  {
                      'students': students
                  })


def new_groups(request):
    groups = Group.objects.all().order_by('-id')
    return render(request,
                  'reception/new_groups.html',
                  {
                      'groups': groups
                  })


def first_lesson(request):
    student_lesson_qs = StudentLessons.objects.filter(is_first=True).all()
    students = Students.objects.filter(student_lesson__is_first=True)\
        .prefetch_related(Prefetch('student_lesson', queryset=student_lesson_qs))\
        .all()

    return render(request,
                  'reception/first_second.html',
                  {
                      'students': students,
                      'title': 'First Lesson Statistics',
                  })


def second_lesson(request):
    student_lesson_qs = StudentLessons.objects.filter(is_second=True).all()
    students = Students.objects.filter(student_lesson__is_second=True)\
        .prefetch_related(Prefetch('student_lesson', queryset=student_lesson_qs))\
        .all()

    return render(request,
                  'reception/first_second.html',
                  {
                      'students': students,
                      'title': 'Second Lesson Statistics',
                  })