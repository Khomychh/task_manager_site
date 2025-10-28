from django.urls import path

from tasks.views import index, TasksListView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TasksListView.as_view(), name="tasks"),
]

app_name = "tasks"
