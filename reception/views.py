from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.db.models import Prefetch
from django.core import serializers
from django.http import JsonResponse, HttpResponse

from refs.models import Phones, PreferDays, PreferTimes
from finance.models import Payment, WantPay
from .forms import StudentsCreateForm, GroupCreateForm
from .models import Students, Group, StudentTransferGroup, Room, StudentLessons, Lost

import datetime


def reception(request):
    students = Students.objects.filter(status=None).all()
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
            new_student.status = 0
            new_student.save(commit=False)

            student_data = request.POST
            phone_list = student_data.getlist('phone')
            relation_list = student_data.getlist('relation')
            if len(phone_list) > 1:
                for i in range(len(phone_list)):
                    phone = Phones(name=relation_list[i], number=phone_list[i])
                    phone.save()
                    new_student.phone.add(phone)
                new_student.save(commit=True)
            else:
                messages.success(request, 'Student is not created')
                # new_student.rollback()
                return redirect('reception:reception')

            messages.success(request, 'Student added successfully')
            return redirect('reception:reception')

    return render(request, 'reception/createStudent.html', {'form': form})


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
        if student.status == 30:
            student.delete()
        else:
            student.status = 30
            student.save()
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
        student.status = 1
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


def get_group(request):
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        group_id = request.GET.get("group_id", None)
        group = Group.objects.get(pk=group_id)
        # print(group.name)
        if group:
            group_dict = {
                "name": group.name,
                "teacher": group.teacher.full_name(),
                "level": group.level.name,
                "place_count": group.place_count,
            }
            return JsonResponse(group_dict, status=200)
        else:
            return JsonResponse({}, status=404)
    return JsonResponse({}, status=400)


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
                'times': [{'class': 'button'} for x in times]
            }
        )

    for group in groups:
        scheduleList[group.room.id-1]['times'][group.times.id-1] = {
            'id': group.id,
            'name': group.name,
            'class': 'full',
        }

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


def new_groups(request):
    groups = Group.objects.all().order_by('-id')
    return render(request,
                  'reception/new_groups.html',
                  {
                      'groups': groups
                  })


def group_show(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    students = Students.objects.filter(group_id=group_id).all()
    data_dict = {
        'group': group,
        'students': students
    }
    return render(request,
                  'teacher/group_students_table.html',
                  data_dict)


def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    data_dict = {
        'group': group,
    }
    return render(request,
                  'reception/group_edit.html',
                  data_dict)


def lost(request):
    students = Students.objects.all()
    return render(request,
                  'reception/lost.html',
                  {
                      'students': students
                  })


def first_lesson(request):
    # student_lesson_qs = StudentLessons.objects.filter(is_first=True).all()
    students = Students.objects.filter(status=1).all()

    return render(request,
                  'reception/first_second.html',
                  {
                      'lesson': 1,
                      'students': students,
                      'title': 'First Lesson Statistics',
                  })


def send2second_lesson(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    student.status = 2
    student.status_p = False
    student.status_r = False
    student.save()

    s = datetime.date
    today = str(s.today())
    sl = StudentLessons(
        student=student,
        group=student.group,
        is_first=True,
        is_second=False,
        date=today
    )
    sl.save()
    return redirect('reception:second_lesson')


def send2first_lesson(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    student.status = 1
    student.status_p = False
    student.status_r = False
    student.save()
    # TODO: delete StudentLesson
    sl = StudentLessons.objects.filter(
        student=student,
        group=student.group,
        is_first=False,
        is_second=True)
    sl.delete()
    # END-TODO---------
    return redirect('reception:first_lesson')


def student_r(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    student.status_r = True
    student.save()
    return redirect('reception:second_lesson')


def student_p(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    student.status_p = True
    student.save()
    return redirect('reception:second_lesson')


# PODO button clicked
def student_podo(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    if student.is_podo:
        student.is_podo = False
    else:
        student.is_podo = True
    print(student.is_podo)
    student.save()
    return redirect('/main/first-lesson')


import calendar


def next_month_date(d):
    _year = d.year+(d.month//12)
    _month =  1 if (d.month//12) else d.month + 1
    next_month_len = calendar.monthrange(_year,_month)[1]
    next_month = d
    if d.day > next_month_len:
        next_month = next_month.replace(day=next_month_len)
    next_month = next_month.replace(year=_year, month=_month)
    return next_month


def student_pay(request, student_id):
    if request.method == 'POST':
        formData = request.POST
        student = get_object_or_404(Students, id=student_id)
        student.status = 40
        student.save()

        amount = formData['amount']
        payment_status = formData['payment_status']
        payment_type = formData['payment_type']
        date = formData['date']
        from_date = formData['date']
        d = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        to_date = next_month_date(d)
        payment = Payment(
            student=student,
            date=date,
            amount=amount,
            type=payment_type,
            status=payment_status,
            from_date=from_date,
            to_date=to_date,
            want_pay_next_month=False,
        )
        print(payment)
        payment.save()

    return redirect('reception:reception')


def student_want2pay(request, student_id):
    if request.method == 'POST':
        formData = request.POST
        student = get_object_or_404(Students, id=student_id)

        date = formData['date']
        w2p = WantPay(
            student=student,
            date=date,
        )
        # print(payment)
        w2p.save()

    return redirect('reception:reception')


def second_lesson(request):
    # student_lesson_qs = StudentLessons.objects.filter(is_second=True).all()
    students = Students.objects.filter(status=2).all()

    return render(request,
                  'reception/first_second.html',
                  {
                      'lesson': 2,
                      'students': students,
                      'title': 'Second Lesson Statistics',
                  })



