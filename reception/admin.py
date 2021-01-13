from django.contrib import admin
from .models import (
    Teacher,
    Group,
    Students
)
from django.template.response import TemplateResponse
from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render_to_response


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    exclude = ('user', 'created_time', 'created_by')

    def lost(self, request):
        context = dict(
            self.admin_site.each_context(request),
            # key=value,
        )
        return TemplateResponse(request, 'lost.html', context)


# @staff_member_required
# def student_list_view(request):
    #show list of all objects
    #. . . create objects of MyModel . . .
    #. . . call their processing methods . . .
    #. . . store in context variable . . .
    # context = {'te': 'ttest'}
    # r = render_to_response('admin/myapp/my_model_list.html', context, RequestContext(request))
    # return HttpResponse(r)