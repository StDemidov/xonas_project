from django import forms
from django.core.exceptions import ValidationError


class ReportForm(forms.Form): 
    from_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата старта отчета',
    )
    to_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата окончания отчета',
    )
    ip = forms.ChoiceField(
        choices=(('Kochergin', 'Кочергин'), ('Tishka', 'Tishka')),
        label='Выберите ИП',
    )

    def clean(self):
        from_d = self.cleaned_data['from_date']
        to_d = self.cleaned_data['to_date']
        if to_d < from_d:
            raise ValidationError(message='Дата окончания не может быть меньше даты начала.')