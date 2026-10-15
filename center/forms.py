from django import forms

from .models import Application, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("direction", "title", "slug", "place", "starts_at", "summary", "body", "seats", "is_open")
        widgets = {
            "direction": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "place": forms.TextInput(attrs={"class": "form-control"}),
            "starts_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "summary": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "seats": forms.NumberInput(attrs={"class": "form-control"}),
            "is_open": forms.CheckboxInput(),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("comment", "attachment")
        labels = {"comment": "Комментарий", "attachment": "Файл (необязательно)"}
        widgets = {
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
