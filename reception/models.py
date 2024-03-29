from django.db import models
from django.contrib.auth.models import User

from refs.models import (
    PreferDays,
    PreferTimes,
    Phones,
    Levels,
    Statuses,
    StudentStatus,
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
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
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
        return self.full_name()


class Room(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return self.name


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
    room = models.ForeignKey(Room,
                             null=True,
                             blank=True,
                             related_name='group_rooms',
                             on_delete=models.SET_NULL)
    level = models.ForeignKey(Levels,
                              related_name='group_level',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True
                              )
    days = models.ForeignKey(PreferDays,
                             related_name='group_days',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,)
    times = models.ForeignKey(PreferTimes,
                              related_name='group_times',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,)
    status = models.ForeignKey(Statuses,
                               default=1,
                               related_name='groups_status',
                               on_delete=models.CASCADE)
    place_count = models.PositiveIntegerField(default=0)
    sub = models.ForeignKey(Sub,
                            related_name='group_sub',
                            default=None,
                            null=True,
                            blank=True,
                            on_delete=models.CASCADE
                            )
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   related_name='group_created',
                                   on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def get_current_student_count(self):
        return StudentTransferGroup.objects.filter(group_id=self.id, status=True).count()

    def __str__(self):
        return self.name


class Students(models.Model):
    STATUS = [
        (0, 'New'),
        (1, 'First Lesson'),
        (2, 'Second Lesson'),  # Star bosganda shu statusga otadi
        # (3, 'P'),  # Darsga keladi (Regularda kerak emas)
        # (20, 'R'),  # Telefonni olmayapti (Regularda kerak)
        # (20, 'PODO'),  # PODO
        (30, 'Delete'),  # Lostga tushadi
        (40, 'Regular'),  # Pul tolashni boshladi
    ]
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(User,
                                related_name='student_user',
                                null=True,
                                default=None,
                                on_delete=models.CASCADE)
    phone = models.ManyToManyField(Phones,
                                   related_name='phone')
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
    is_podo = models.BooleanField(default=False)
    group = models.ForeignKey(Group,
                              related_name='students_group',
                              null=True,
                              on_delete=models.CASCADE,
                              blank=True,
                              default=None)
    group_type = models.ForeignKey(GroupTypes,
                                   related_name='student_group_type',
                                   null=True,
                                   on_delete=models.CASCADE,
                                   default=None)
    date_birth = models.DateField()
    note = models.CharField(max_length=200,
                            null=None,
                            default=None,
                            blank=True)
    is_old = models.ForeignKey(IsOld,
                               related_name='is_old_student',
                               default=1,
                               on_delete=models.CASCADE)
    sub = models.ForeignKey(Sub,
                            related_name='student_sub',
                            on_delete=models.CASCADE,
                            default=None,
                            null=True,
                            blank=True)
    status = models.PositiveSmallIntegerField(verbose_name='Student status',
                                              choices=STATUS,
                                              default=None,
                                              null=True)
    status_p = models.BooleanField(verbose_name='Probejka', default=False)
    status_r = models.BooleanField(verbose_name='Call', default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   related_name='students_created',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True
                                   )

    def full_name(self):
        return '%s %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.full_name()


class StudentTransferGroup(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='transfer_student')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='transfer_group')
    sequence = models.PositiveIntegerField(default=1)
    date = models.DateField(default=None, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=None, blank=True, null=True)


class StudentLessons(models.Model):
    STATUS = [
        (0, 'UpSent'),
        (1, 'Homework'),
        # (2, 'First Lesson'),
        # (3, 'Second Lesson'),
    ]
    student = models.ForeignKey(Students,
                                on_delete=models.CASCADE,
                                related_name='student_lesson')
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='group_lesson')
    date = models.DateField(default=None)
    is_first = models.BooleanField(default=None, blank=True, null=True)
    is_second = models.BooleanField(default=None, blank=True, null=True)
    status = models.PositiveIntegerField(choices=STATUS, blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'StudentLesson'
        verbose_name_plural = 'StudentLessons'


class Lost(models.Model):
    STATUS = [
        (1, 'First Lesson'),
        (2, 'Second Lesson'),
        (3, 'From reception'),
        (4, 'Regular'),
    ]
    student = models.ForeignKey(Students,
                                on_delete=models.CASCADE,
                                related_name='student_lost')
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='group_lost')
    status = models.PositiveIntegerField(choices=STATUS,
                                         default=None,
                                         blank=True,
                                         null=True)
    reason = models.TextField(default=None, blank=True)
