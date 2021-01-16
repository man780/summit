from django.shortcuts import render

# Create your views here.


def index(request):

    breadcrumbs = [
        {
            'name': 'Главная',
            'url': '/',
            'class': '',
        },
    ]
    bodyclass = 'sidebar-collapse'
    title = 'test'
    return render(request,
                  'teacher/index.html',
                  {title: title,
                   'breadcrumbs': breadcrumbs,
                   'bodyclass': bodyclass})
