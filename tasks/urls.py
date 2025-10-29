from django.urls import path

from tasks.views import index, TasksListView, TaskDetailView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TasksListView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
]

app_name = "tasks"
