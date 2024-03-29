from django.db import models


class PreferDays(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Prefer day'
        verbose_name_plural = 'Prefer days'

    def __str__(self):
        return self.name


class PreferTimes(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']
        verbose_name = 'Prefer time'
        verbose_name_plural = 'Prefer times'

    def __str__(self):
        return self.name


class Phones(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'

    def __str__(self):
        return '%s (%s)' % (self.name, self.number)


class Levels(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'

    def __str__(self):
        return self.name


class Statuses(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.name


class StudentStatus(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Student Status'
        verbose_name_plural = 'Student Statuses'

    def __str__(self):
        return self.name


class IsOld(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Is old student'
        verbose_name_plural = 'Is old students'

    def __str__(self):
        return self.name


class GroupTypes(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Group type'
        verbose_name_plural = 'Group types'

    def __str__(self):
        return self.name


class ComeFrom(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'Come from'
        verbose_name_plural = 'Come from'

    def __str__(self):
        return self.name


class Sub(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

