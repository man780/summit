from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from reception.models import Group, Students


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={'model__in':
                                                           ('text',
                                                            'video',
                                                            'image',
                                                            'file')
                                                       },
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
            self._meta.model_name), {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()


class Exams(models.Model):
    group = models.ForeignKey(Group,
                              related_name='exam_group',
                              on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date", auto_now_add=True)
    title = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.date.strftime('%d/%m/%Y')

    class Meta:
        ordering = ['created']


class Lesson(models.Model):
    group = models.ForeignKey(Group,
                              related_name='lesson_group',
                              on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date", auto_now_add=True)
    title = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.date.strftime('%d/%m/%Y')

    class Meta:
        ordering = ['created']


class Homework(models.Model):
    group = models.ForeignKey(Group,
                              related_name='homework_group',
                              on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,
                               related_name='homework_lesson',
                               on_delete=models.CASCADE,
                               default=None,
                               blank=True)
    date = models.DateField(verbose_name="Date", auto_now_add=True)
    title = models.TextField(verbose_name="Homework title")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' - ' + self.date.strftime('%d/%m/%Y')

    class Meta:
        ordering = ['created']


class Attendance(models.Model):
    TYPES = [
        (1, 'Д/З НЕ выполнено'),
        (2, 'Д/З выполнено'),
        (3, 'Assignment НЕ выполнено'),
        (4, 'Assignment выполнено'),
        (5, 'Словарь НЕ сдан'),
        (6, 'Словарь сдан'),
        (7, 'Пропуск'),
        (8, 'Пропуск отработан'),
    ]
    group = models.ForeignKey(Group,
                              related_name='attendance_group',
                              on_delete=models.CASCADE)
    student = models.ForeignKey(Students,
                                related_name='attendance_student',
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)
    lesson = models.ForeignKey(Lesson,
                               related_name='lesson_attendance',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               default=None)
    date = models.DateField(verbose_name="Date",
                            auto_now_add=True)
    is_first = models.BooleanField(default=False)
    is_second = models.BooleanField(default=False)
    attendance_type = models.SmallIntegerField(choices=TYPES)
    reason = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date.strftime('%d/%m/%Y')

    class Meta:
        ordering = ['created']
