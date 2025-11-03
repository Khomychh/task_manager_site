from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskSearchForm, TaskCreateForm, TaskUpdateForm, TaskTypeCreateForm, TaskTypeSearchForm, \
    WorkerSearchForm, WorkerCreationForm, TaskTypeUpdateForm
from tasks.models import Task, Worker, Project, TaskType


def index(request):
    tasks_count = Task.objects.count()
    project_count = Project.objects.all().count()
    worker_count = Worker.objects.all().count()

    context = {
        "tasks_count": tasks_count,
        "project_count": project_count,
        "worker_count": worker_count,
    }
    return render(request, "index.html", context=context)


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 10

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


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    template_name = "tasks/task_type_detail.html"
    context_object_name = "task_type"
    queryset = TaskType.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TaskTypeDetailView, self).get_context_data(**kwargs)
        tasks_count = self.object.tasks.count()
        task_list = self.object.tasks.all()
        context["tasks_count"] = tasks_count
        context["task_list"] = task_list
        return context


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    form_class = TaskTypeUpdateForm
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-detail")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    template_name = "tasks/task_type_confirm_delete.html"
    context_object_name = "task_type"
    success_url = reverse_lazy("tasks:task-type-list")


class WorkerListView(generic.ListView):
    model = Worker
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        full_name = self.request.GET.get("full_name", "")
        context["search_form"] = WorkerSearchForm(
            initial={"full_name": full_name}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.all().select_related("position")
        full_name = self.request.GET.get("full_name", "")
        if full_name:
            queryset = queryset.filter(name__icontains=full_name)
        return queryset


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().select_related("position")

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        projects = self.object.projects.all()
        tasks = self.object.tasks.all()
        teams = self.object.teams.all()
        if projects:
            context["projects"] = projects
        if tasks:
            context["tasks"] = tasks
        if teams:
            context["teams"] = teams
        return context


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:worker-detail")


class WorkerDeleteView(generic.DeleteView):
    model = Worker