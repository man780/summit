from django.db import models
from reception.models import Students


class Payment(models.Model):
    STATUS = [
        (0, 'Not paid'),
        (1, 'Should pay'),
        (2, 'Full paid'),
        (3, 'Back money'),
    ]
    AMOUNT_TYPE = [
        (1, 'Plastic'),
        (2, 'Cash'),
        (3, 'MOT'),
    ]
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Students,
                                related_name='payment_student',
                                on_delete=models.CASCADE)
    note = models.TextField()
    amount = models.IntegerField(default=0)
    type = models.IntegerField(choices=AMOUNT_TYPE, default=None, blank=True)
    status = models.IntegerField(choices=STATUS)
    from_date = models.DateField(default=None, blank=True, null=True)
    to_date = models.DateField(default=None, blank=True, null=True)
    want_pay_next_month = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.full_name()

    class Meta:
        ordering = ['created']
