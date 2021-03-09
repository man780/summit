from django.contrib import admin
from .models import Subject, Course, Module, Exams, Lesson, Homework, Attendance


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(Exams)
class ExamsAdmin(admin.ModelAdmin):
    list_display = ['group', 'date', 'title', 'created']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['group', 'date', 'title', 'created']


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['group', 'lesson', 'date', 'title', 'created']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['group', 'student', 'date', 'attendance_type', 'reason', 'created']
