import datetime
import calendar

from django.shortcuts import redirect, get_object_or_404

from finance.models import Payment, WantPay
from reception.models import Students, StudentLessons


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


def next_month_date(d):
    _year = d.year+(d.month//12)
    _month =  1 if (d.month//12) else d.month + 1
    next_month_len = calendar.monthrange(_year, _month)[1]
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
