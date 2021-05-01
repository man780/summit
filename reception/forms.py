from django import forms
from .models import Students


class StudentsCreateForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ('first_name', 'last_name', 'date_birth',
                  'come_from', 'level', 'prefer_day',
                  'prefer_time', 'group_type', 'is_old', 'note')
        widgets = {
            'note': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }

