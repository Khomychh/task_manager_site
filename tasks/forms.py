from django import forms

from tasks.models import Task, TaskType


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Name"}
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


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Name"}
        )
    )

class TaskUpdateForm(TaskCreateForm, forms.ModelForm):
    class Meta(TaskCreateForm.Meta):
        fields = ("is_completed",) + TaskCreateForm.Meta.fields


class TaskTypeCreateForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ("name", "description")
        labels = {"name": "", "description": ""}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name*"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
        }