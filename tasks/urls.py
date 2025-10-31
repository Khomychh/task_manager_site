from django.urls import path

from tasks.views import index, TaskListView, TaskDetailView, toggle_completed, TaskCreateView, TaskUpdateView, \
    TaskDeleteView, TaskTypeListView, TaskTypeDetailView, TaskTypeCreateView, TaskTypeUpdateView, TaskTypeDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/completed/", toggle_completed, name="toggle-completed"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/<int:pk>/", TaskTypeDetailView.as_view(), name="task-type-detail"),
    path("tasks-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("tasks-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
]

app_name = "tasks"
