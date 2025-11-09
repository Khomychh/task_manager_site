from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from tasks.models import Task, TaskType, Worker, Position


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


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "is_completed",
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


class TaskTypeCreateForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ("name", "description")
        labels = {"name": "", "description": ""}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name*"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
        }


class TaskTypeUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ("name", "description")
        labels = {"name": "", "description": ""}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name*"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
        }


class WorkerSearchForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Full name"}
        )
    )


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "last_name",
            "first_name",
            "email",
            "position",
            "biography",
        )
        labels = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "biography": ""
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username*"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name*"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name*"}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
            "biography": forms.Textarea(attrs={"placeholder": "Biography"}),
        }


class WorkerUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "last_name",
            "first_name",
            "email",
            "position",
            "biography",
        )


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Name"}
        )
    )


class PositionCreateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ("name", "description")
        labels = {"name": "", "description": ""}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Name*"}),
            "description": forms.Textarea(attrs={"placeholder": "Description"}),
        }
