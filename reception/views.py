from django.shortcuts import render, redirect
from .models import Students, Group, StudentTransferGroup, Room
from refs.models import Phones, PreferDays, PreferTimes
from .forms import StudentsCreateForm, GroupCreateForm
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
            return redirect('reception:reception')

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
    groupMatrix = [['' for x in times] for y in rooms]

    for group in groups:
        groupMatrix[group.room.id-1][group.times.id-1] = group.name
    for room in rooms:
        groupMatrix[room.id-1][0] = room.name
    """for room in range(rooms.count()):
        groupMatrix[room][0] = room
        for time in times:
            groupMatrix[room.id-1][time.id-1] = 0"""
    # for group in groups:
    #     groupMatrix[group.room.id][group.times.id] = group.name
    # print(groupMatrix)
    return render(request,
                  'reception/groups.html',
                  {
                      'rooms': rooms,
                      'groups': groups,
                      'times': times,
                      'groupMatrix': groupMatrix,
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
