from django.contrib import admin
from .models import (
    Teacher,
    Group,
    Students
)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['full_name']
