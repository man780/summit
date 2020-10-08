from django.db import models
from django.contrib.auth.models import User
from refs.models import (
    PreferDays,
    PreferTimes,
    Levels,
    Statuses,
    IsOld,
    GroupTypes,
    ComeFrom,
    Sub
)


class Teacher(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    note = models.CharField(max_length=200)
    date_birth = models.DateField()
    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   related_name='teacher_created',
                                   on_delete=models.CASCADE)

    def full_name(self):
        return '%s %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return self.full_name


class Group(models.Model):
    name = models.CharField(max_length=200)
    group_type = models.ForeignKey(GroupTypes,
                                   related_name='group_type',
                                   on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,
                                null=True,
                                default=None,
                                related_name='groups_teacher',
                                on_delete=models.CASCADE)
    status = models.ForeignKey(Statuses,
                               default=1,
                               related_name='groups_status',
                               on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   related_name='group_created',
                                   on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name


class Students(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(User,
                                related_name='student_user',
                                on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    come_from = models.ForeignKey(ComeFrom,
                                  related_name='come_from',
                                  on_delete=models.CASCADE)
    level = models.ForeignKey(Levels,
                              related_name='student_level',
                              on_delete=models.CASCADE)
    prefer_day = models.ManyToManyField(PreferDays,
                                        related_name='prefer_day')
    prefer_time = models.ManyToManyField(PreferTimes,
                                         related_name='prefer_time')
    group = models.ForeignKey(Group,
                              related_name='students_group',
                              null=True,
                              on_delete=models.CASCADE)
    group_type = models.ForeignKey(GroupTypes,
                                   related_name='student_group_type',
                                   null=True,
                                   on_delete=models.CASCADE)
    date_birth = models.DateField()
    note = models.CharField(max_length=200)
    is_old = models.ForeignKey(IsOld,
                               related_name='is_old_student',
                               default=1,
                               on_delete=models.CASCADE)
    sub = models.ForeignKey(Sub,
                            related_name='student_sub',
                            on_delete=models.CASCADE)
    status = models.ForeignKey(Statuses,
                               related_name='student_status',
                               default=1,
                               on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   related_name='students_created',
                                   on_delete=models.CASCADE)

    def full_name(self):
        return '%s %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.full_name
