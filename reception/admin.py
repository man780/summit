from django.contrib import admin
from .models import (
    Teacher,
    Group,
    Students,
    StudentTransferGroup,
    StudentLessons,
    Lost,
    Room
)
from django.template.response import TemplateResponse


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'created_time', 'level', 'group_type', 'note']
    exclude = ('user', 'created_by')

    def lost(self, request):
        context = dict(
            self.admin_site.each_context(request),
            # key=value,
        )
        return TemplateResponse(request, 'lost.html', context)


@admin.register(StudentTransferGroup)
class StudentTransferGroupAdmin(admin.ModelAdmin):
    list_display = ['student', 'group', 'date', 'status']


@admin.register(StudentLessons)
class StudentLessonsAdmin(admin.ModelAdmin):
    list_display = ['student', 'group', 'date', 'is_first', 'is_second', 'status']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name']
