from django import forms

from tasks.models import Task


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Task Name"}
        )
    )


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "name",
            "priority",
            "deadline",
            "type",
            "project",
            "description",
            "assignees",
        )
        labels = {"name": "", "description": "",}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name*"}),
            "deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
            "assignees": forms.CheckboxSelectMultiple,
        }