from django import forms
from .models import Activity, JobApplication


class DateInput(forms.DateInput):
    input_type = "date"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            "title", "company", "vacancy_url", "source", "status", "priority",
            "location", "work_mode", "salary_min", "salary_max", "currency",
            "salary_period", "applied_on", "next_step_on", "responsibilities",
            "requirements", "notes",
        ]
        widgets = {
            "applied_on": DateInput(), "next_step_on": DateInput(),
            "responsibilities": forms.Textarea(attrs={"rows": 5}),
            "requirements": forms.Textarea(attrs={"rows": 5}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["kind", "title", "details", "scheduled_for", "completed"]
        widgets = {"scheduled_for": DateTimeInput(format="%Y-%m-%dT%H:%M"), "details": forms.Textarea(attrs={"rows": 3})}
