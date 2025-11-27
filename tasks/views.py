from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import (
    TaskSearchForm,
    TaskCreateForm,
    TaskUpdateForm,
    TaskTypeCreateForm,
    TaskTypeSearchForm,
    WorkerSearchForm,
    WorkerCreationForm,
    TaskTypeUpdateForm,
    WorkerUpdateForm,
    PositionSearchForm,
    PositionCreateForm,
    TeamSearchForm,
    TeamCreateForm,
    TeamUpdateForm,
    ProjectSearchForm,
    ProjectCreateForm,
    ProjectUpdateForm,
    TaskAssignForm,
)
from tasks.models import Task, Worker, Project, TaskType, Position, Team


@login_required
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


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})
        context["show_only_my"] = self.request.GET.get("my") == "1"
        context["status"] = self.request.GET.get("status", "all")
        context["name"] = name
        context["ordering"] = self.request.GET.get("ordering", "-deadline")
        return context

    def get_queryset(self):
        queryset = Task.objects.all().select_related("type", "project")
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)

        if self.request.GET.get("my") == "1":
            queryset = queryset.filter(assignees__in=[self.request.user])

        status = self.request.GET.get("status", None)
        if status == "completed":
            queryset = queryset.filter(is_completed=True)
        if status == "uncompleted":
            queryset = queryset.filter(is_completed=False)

        ordering = self.request.GET.get("ordering", None)
        if ordering:
            allowed_orderings = {
                "deadline",
                "-deadline",
            }
            if ordering in allowed_orderings:
                queryset = queryset.order_by(ordering)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = (
        Task.objects.all()
        .select_related("type", "project")
        .prefetch_related("assignees")
    )

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        if self.object:
            context["assignees"] = self.object.assignees.all()
        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


@login_required
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


@login_required
def task_assign(request, pk: int):
    task = get_object_or_404(Task, pk=pk)

    # якщо у завдання є проект, то беремо працівників з команди проекту
    # інакше показуємо всіх працівників
    if task.project:
        if task.project.team_id and task.project.leader_id:
            team = task.project.team
            assignees_qs = Worker.objects.filter(
                Q(teams=team) | Q(pk=task.project.leader_id)
            ).distinct()
        elif task.project.leader_id:
            assignees_qs = Worker.objects.filter(Q(pk=task.project.leader_id))
        elif task.project.team_id:
            team = task.project.team
            assignees_qs = Worker.objects.filter(Q(teams=team))
    else:
        assignees_qs = Worker.objects.all()

    if request.method == "POST":
        form = TaskAssignForm(
            request.POST, instance=task, assignees_queryset=assignees_qs
        )
        if form.is_valid():
            form.save()
            return redirect(task.get_absolute_url())
    else:
        form = TaskAssignForm(instance=task, assignees_queryset=assignees_qs)

    return render(
        request,
        "tasks/task_assign.html",
        {"form": form, "task": task}
    )


@login_required()
def task_take(request, pk: int):
    task = get_object_or_404(Task, pk=pk)
    worker = Worker.objects.get(id=request.user.id)
    if task.assignees.filter(id=worker.id).exists():
        return redirect(task.get_absolute_url())
    task.assignees.add(worker)
    return redirect(task.get_absolute_url())

@login_required()
def task_remove_from_me(request, pk: int):
    task = get_object_or_404(Task, pk=pk)
    worker = Worker.objects.get(id=request.user.id)
    if task.assignees.filter(id=worker.id).exists():
        task.assignees.remove(worker)
    return redirect(task.get_absolute_url())


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(TaskTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = TaskType.objects.all()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    template_name = "tasks/task_type_detail.html"
    context_object_name = "task_type"
    queryset = TaskType.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TaskTypeDetailView, self).get_context_data(**kwargs)
        tasks_count = self.object.tasks.count()
        context["tasks_count"] = tasks_count
        return context


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeCreateForm
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeUpdateForm
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-detail")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "tasks/task_type_confirm_delete.html"
    context_object_name = "task_type"
    success_url = reverse_lazy("tasks:task-type-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

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
            queryset = queryset.filter(full_name__icontains=full_name)
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = (
        Worker.objects.all()
        .select_related("position")
        .prefetch_related("projects", "tasks", "teams")
    )

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        tasks = self.object.tasks.all()
        teams = self.object.teams.all()
        projects = self.object.projects.all()
        if tasks:
            context["tasks"] = tasks
        if teams:
            context["teams"] = teams
        if projects:
            context["projects"] = projects
        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "tasks:worker-detail",
            kwargs={"pk": self.object.pk}
        )


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Position.objects.all()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker_count = self.object.workers.count()
        context["worker_count"] = worker_count
        return context


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionCreateForm
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = ("name", "description")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TeamSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Team.objects.all()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    context_object_name = "team"

    def get_queryset(self):
        return Team.objects.all().prefetch_related("workers", "projects")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "workers": self.object.workers.all(),
                "projects": self.object.projects.all(),
                "has_workers": self.object.workers.exists(),
                "has_projects": self.object.projects.exists(),
            }
        )
        return context


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreateForm
    success_url = reverse_lazy("tasks:team-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamUpdateForm

    def get_success_url(self):
        return reverse_lazy("tasks:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("tasks:team-list")


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ProjectSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Project.objects.all()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    context_object_name = "project"

    def get_queryset(self):
        return (
            Project.objects.all()
            .select_related("team")
            .prefetch_related(
                "tasks",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "has_tasks": self.object.tasks.exists(),
                "tasks": self.object.tasks.all(),
            }
        )
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreateForm

    def get_success_url(self):
        return reverse_lazy(
            "tasks:project-detail",
            kwargs={"pk": self.object.pk}
        )


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "tasks:project-detail",
            kwargs={"pk": self.object.pk}
        )


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:project-list")


@login_required
def project_toggle_completed(request, pk: int):
    project = Project.objects.get(pk=pk)
    if project.is_completed:
        project.is_completed = False
        project.save()
    else:
        try:
            project.is_completed = True
            project.save()
        except ValidationError:
            messages.error(
                request,
                "Cannot complete project with uncompleted tasks."
            )
            return redirect(project.get_absolute_url())
    next_url = request.POST.get("next") or request.GET.get("next")
    if not next_url:
        next_url = request.META.get("HTTP_REFERER")

    return redirect(next_url)
