from django.db import models
from reception.models import Students


class Payment(models.Model):
    STATUS = [
        (0, 'Not paid'),
        (1, 'Partial payment'),
        (2, 'Full paid'),
    ]
    AMOUNT_TYPE = [
        (1, 'Plastic'),
        (2, 'Cash')
    ]
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Students,
                                related_name='payment_student',
                                on_delete=models.CASCADE)
    note = models.TextField()
    amount = models.IntegerField(default=0)
    type = models.IntegerField(choices=AMOUNT_TYPE, default=None, blank=True)
    status = models.IntegerField(choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.full_name()

    class Meta:
        ordering = ['created']
