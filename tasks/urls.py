from django.urls import path

from tasks.views import index, TasksListView, TaskDetailView, toggle_completed, TasksCreateView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TasksListView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TasksCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/completed/", toggle_completed, name="toggle-completed"),
]

app_name = "tasks"
