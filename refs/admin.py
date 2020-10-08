from django.contrib import admin
from .models import (
    PreferDays,
    PreferTimes,
    Levels,
    Statuses,
    IsOld,
    GroupTypes,
    ComeFrom,
    Sub
)


@admin.register(PreferDays)
class PreferDaysAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(PreferTimes)
class PreferTimesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Levels)
class LevelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Statuses)
class StatusesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(IsOld)
class IsOldAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(GroupTypes)
class GroupTypesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(ComeFrom)
class ComeFromAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Sub)
class SubAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
