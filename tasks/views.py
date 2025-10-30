from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskSearchForm, TaskCreateForm, TaskUpdateForm
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


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all().select_related("type", "project")
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TaskDetailView(generic.DetailView):
    model = Task
    context_object_name = "task"
    queryset = Task.objects.all().select_related(
        "type", "project").prefetch_related("assignees")

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        if self.object:
            context["assignees"] = self.object.assignees.all()
        return context


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


def toggle_completed(request, pk: int):
    task = Task.objects.get(id=pk)
    if task:
        if task.is_completed:
            task.is_completed = False
        else:
            task.is_completed = True
        task.save()
    next_url = request.POST.get("next") or request.GET.get("next")
    if not next_url:
        next_url = request.META.get("HTTP_REFERER")

    return redirect(next_url)
