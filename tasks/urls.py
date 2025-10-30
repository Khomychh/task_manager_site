from django.urls import path

from tasks.views import index, TaskListView, TaskDetailView, toggle_completed, TaskCreateView, TaskUpdateView, \
    TaskDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/completed/", toggle_completed, name="toggle-completed"),
]

app_name = "tasks"
