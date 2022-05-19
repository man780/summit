from django.shortcuts import render, redirect, get_object_or_404
from reception.models import Students, Group
from finance.models import Payment
from django.db.models import Count


def index(request):
    students = Students.objects.all()
    payments = Payment.objects.filter(amount__gt=0).all()
    not_paid_students = []
    for student in students:
        try:
            student = Payment.objects.get(student=student, status=0, amount=0)
            # print(student)
        except Payment.DoesNotExist:
            not_paid_students.append(student)
    print(not_paid_students)
    for student in not_paid_students:
        print(student.full_name)

    should_pay = []
    for student in students:
        try:
            student = Payment.objects.filter(student=student, status=1).get()
            should_pay.append(student)
        except Payment.DoesNotExist:
            pass
            # should_pay.append(student)
    return render(request,
                  "finance/index.html",
                  {
                      "students": students,
                      "payments": payments,
                      "not_paid_students": not_paid_students,
                      "should_pay": should_pay
                  })


def not_paid(request):
    students = Students.objects.all()
    not_paid_students = []
    for student in students:
        try:
            student = Payment.objects.get(student=student, status=0, amount=0)
            # print(student)
        except Payment.DoesNotExist:
            not_paid_students.append(student)
    # print(not_paid_students)
    for student in not_paid_students:
        print(student.full_name)

    should_pay = []
    for student in students:
        try:
            student = Payment.objects.filter(student=student, status=1).get()
            should_pay.append(student)
        except Payment.DoesNotExist:
            pass
            # should_pay.append(student)
    return render(request,
                  "finance/not_paid.html",
                  {
                      "not_paid_students": not_paid_students,
                  })


def statistics(request):
    result = (Students.objects
              .values('come_from')
              .annotate(dcount=Count('come_from'))
              .order_by()
              )
    # print(result)
    return render(
        request,
        "finance/statistics.html",
        {
          "result": result
        }
    )
