from django import forms

from .models import Application, Direction, Event, Partner, Project


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ("name", "kind", "site", "description")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "kind": forms.TextInput(attrs={"class": "form-control"}),
            "site": forms.URLInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class DirectionSummaryForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = ("summary",)
        widgets = {"summary": forms.TextInput(attrs={"class": "form-control"})}


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("direction", "title", "slug", "summary", "body", "started_on", "is_open")
        widgets = {
            "direction": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "summary": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "started_on": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_open": forms.CheckboxInput(),
        }


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
