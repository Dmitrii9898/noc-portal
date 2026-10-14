from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("comment", "attachment")
        labels = {"comment": "Комментарий", "attachment": "Файл (необязательно)"}
        widgets = {
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
