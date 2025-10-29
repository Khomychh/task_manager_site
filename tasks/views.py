from django.shortcuts import render
from django.views import generic

from tasks.models import Task, Worker, Project


def index(request):
    tasks_count = Task.objects.count()
    project_count = Project.objects.all()
    worker_count = Worker.objects.all()

    context = {
        "tasks_count": tasks_count,
        "project_count": project_count,
        "worker_count": worker_count,
    }
    return render(request, "index.html", context=context)


class TasksListView(generic.ListView):
    model = Task
    paginate_by = 2

    def get_queryset(self):
        queryset = Task.objects.all().select_related("type")
        return queryset