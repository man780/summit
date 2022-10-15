import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from refs.models import Phones
from reception.models import Students, Group, StudentLessons, StudentTransferGroup
from reception.forms import StudentsCreateForm
from finance.models import Payment


def add_student(request):
    form = StudentsCreateForm(data=request.GET)

    if request.method == 'POST':
        # Форма отправлена.
        form = StudentsCreateForm(data=request.POST)

        if form.is_valid():
            new_student = form.save(commit=False)
            new_student.created_by = request.user
            new_student.status = 0
            new_student.save()

            student_data = request.POST
            phone_list = student_data.getlist('phone')
            relation_list = student_data.getlist('relation')
            if len(phone_list) > 1:
                for i in range(len(phone_list)):
                    phone = Phones(name=relation_list[i], number=phone_list[i])
                    phone.save()
                    new_student.phone.add(phone)
                new_student.save()
            else:
                messages.success(request, 'Student is not created')
                # new_student.rollback()
                return redirect('reception:reception')

            messages.success(request, 'Student added successfully')
            return redirect('reception:reception')

    title = 'Add student'
    return render(request, 'reception/student_add_edit.html', {
        'form': form,
        'title': title
    })


def edit_student(request, student_id):

    student = get_object_or_404(Students, id=student_id)
    form = StudentsCreateForm(request.POST or None, instance=student)
    if request.method == 'POST':
        # Форма отправлена.
        form = StudentsCreateForm(data=request.POST, instance=student)
        if form.is_valid():
            student = form.save()
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
    title = 'Edit student'
    return render(request, 'reception/student_add_edit.html', {
        'title': title,
        'form': form
    })


def delete_student(request, student_id):
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


def transfer_student_to_group(request, student_id):

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
