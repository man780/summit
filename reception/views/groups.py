from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from reception.models import Students, Group, Room, PreferTimes
from reception.forms import GroupCreateForm


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


def add_group(request):
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

    title = 'Add group'
    action_url = reverse('reception:add_group')
    return render(request,
                  'reception/group_add_edit.html',
                  {
                      'action_url': action_url,
                      'title': title,
                      'form': form
                  })


def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    form = GroupCreateForm(request.POST or None, instance=group)

    if request.method == 'POST':
        # Форма отправлена.
        form = GroupCreateForm(data=request.POST, instance=group)

        if form.is_valid():
            group = form.save()
            group.save()
            messages.success(request, 'Group edit successfully')
            # Перенаправляем пользователя на страницу груп.
            return redirect('reception:groups')

    title = 'Edit group'
    action_url = reverse('reception:group_edit', kwargs={'group_id': group.id})
    data_dict = {
        'action_url': action_url,
        'title': title,
        'form': form
    }

    return render(request,
                  'reception/group_add_edit.html',
                  data_dict)


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
