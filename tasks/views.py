from django.shortcuts import render
from django.views import generic

from tasks.forms import TaskSearchForm
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

    def get_context_data(self, **kwargs):
        context = super(TasksListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all().select_related("type")
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset