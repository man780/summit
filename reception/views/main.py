from django.shortcuts import render

from reception.models import Students


def error_500(request):
    return render(request, '500.html')


def error_404(request):
    return render(request, '404.html')


def reception(request):
    students = Students.objects.filter(status=0).all()
    if request.GET:
        students = students.filter()
    return render(request,
                  'reception/index.html',
                  {
                      'students': students
                  })


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
